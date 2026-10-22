const SVG_URL = "/energy_flow_dashboard/frontend/energy-flow-dashboard.svg?v=22";

class EnergyFlowDashboard extends HTMLElement {
    constructor() {
        super();
        this.attachShadow({ mode: "open" });
        this._config = {};
        this._hass = null;
        this._svgDoc = null;
        this._svgRoot = null;
        this._fields = {};
        this._devices = {};
        this._devices_present = [];
        this._mapping = {};
        this._loaded = false;

         // Animacja wentylatorów
        this._fanAngle = 0;
        this._fanLastTime = 0;
        this._fanRunning = false;

        this._froniusFanAngle = 0;
        this._froniusFanLastTime = 0;
        this._froniusFanRunning = false;
    }

    setConfig(config) {
        this._config = config || {};
        this.render();
    }

    set hass(hass) {
        this._hass = hass;
        if (!this._loaded) {
            this._loadConfig();
        } else {
            this._applyValues();
        }
    }

    async _loadConfig() {
        try {
            const resp = await this._hass.callWS({
                type: "energy_flow_dashboard/get_config",
            });
            this._fields = resp.fields || {};
            this._devices = resp.devices || {};
            this._devices_present = resp.devices_present || [];
            this._mapping = resp.mapping || {};
            this._loaded = true;
            await this._loadSvg();
            this._applyValues();
        } catch (e) {
            console.warn("EnergyFlowDashboard: get_config failed", e);
        }
    }

    async _loadSvg() {
        if (this._svgDoc) return this._svgDoc;
        try {
            const resp = await fetch(SVG_URL);
            const text = await resp.text();
            const parser = new DOMParser();
            this._svgDoc = parser.parseFromString(text, "image/svg+xml");
            return this._svgDoc;
        } catch (e) {
            console.error("EnergyFlowDashboard: SVG load error", e);
            return null;
        }
    }

    _formatEntityValue(meta, stateObj) {
        const raw = stateObj.state;
        if (raw === "unknown" || raw === "unavailable") return null;

        const prefix = meta.prefix || "";
        const unitFromEntity = stateObj.attributes.unit_of_measurement;
        const unitFromConfig = meta.unit;
        const unit = unitFromEntity || unitFromConfig || "";

        let displayValue = raw;
        if (raw === "on") displayValue = "Yes";
        else if (raw === "off") displayValue = "No";

        return `${prefix}${displayValue}${unit ? " " + unit : ""}`;
    }

    _findBaseDataField(labelFieldId) {
        const meta = this._fields[labelFieldId];
        if (meta && meta.depends_on) return meta.depends_on;

        if (labelFieldId.endsWith("-label")) {
            const base = labelFieldId.slice(0, -6);
            const candidate = base + "-data";
            if (this._fields[candidate]) return candidate;
            if (this._fields[base]) return base;
        }
        if (labelFieldId.endsWith("_label")) {
            const base = labelFieldId.slice(0, -6);
            const candidate = base + "-data";
            if (this._fields[candidate]) return candidate;
            if (this._fields[base]) return base;
        }
        return null;
    }

    _setVisible(el, visible) {
        if (!el) return;
        if (visible) {
            if (el.style.display === "none") {
                el.style.display = "";
            }
        } else {
            el.style.display = "none";
        }
    }

    async _applyValues() {
        if (!this._svgDoc || !this._hass) return;

        if (!this._svgRoot) {
            const clone = this._svgDoc.documentElement.cloneNode(true);
            clone.setAttribute("width", "100%");
            clone.setAttribute("height", "auto");
            this._svgRoot = clone;
            const container = this.shadowRoot.querySelector(".svg-container");
            if (container) {
                container.replaceChildren(clone);
            }
        }

        const q = (id) => this._svgRoot.querySelector(`[id="${id}"]`);

        // ============================================================
        // PRIORYTET 1: Grupy urządzeń — na podstawie devices_present
        // ============================================================
        const present = new Set(this._devices_present || []);

        // Mapa: device_id → lista ID grup SVG, które należą do urządzenia
        const DEVICE_GROUPS = {
            "inverter_1": ["inverter_1", "wire_inverter1"],
            "inverter_2": ["inverter_2", "wire_inverter2"],
            "battery": ["EnergyStorage", "DC Wires"],
            "heat_pump": ["g38", "wire_Heat_pump"],
            "subboard_1": ["AC_SubBoard1", "WIre-subboard_1-2"],
            "subboard_2": ["AC_Subboard2", "grid_wires"],
            "home": ["house", "home_wires"],
            "grid": ["Grid", "full-backup"],
        };

        for (const [device_id, group_ids] of Object.entries(DEVICE_GROUPS)) {
            const isPresent = present.has(device_id);
            for (const gid of group_ids) {
                this._setVisible(q(gid), isPresent);
            }
        }

        // ============================================================
        // PRIORYTET 2: Grupy MPPT (choice → hides_map)
        // ============================================================
        for (const [fieldId, meta] of Object.entries(this._fields)) {
            if (meta.input_type !== "choice") continue;
            if (!meta.hides_map) continue;

            for (const mapVal of Object.values(meta.hides_map)) {
                for (const id of mapVal) {
                    this._setVisible(q(id), true);
                }
            }

            const value = this._mapping[fieldId] ?? meta.default;
            const hideList = meta.hides_map[value] || [];
            for (const hideId of hideList) {
                this._setVisible(q(hideId), false);
            }
        }

        // ============================================================
        // PRIORYTET 3: Grupy opcjonalne (_visible z hides)
        // (pomijamy device_* — obsłużone w P1 przez devices_present)
        // ============================================================
        for (const [fieldId, meta] of Object.entries(this._fields)) {
            if (meta.input_type !== "boolean") continue;
            if (fieldId.startsWith("device_")) continue;
            if (!meta.hides) continue;

            const raw = this._mapping[fieldId];
            const checked = raw !== undefined
                ? raw === true || raw === "true" || raw === "on"
                : (meta.default !== undefined ? meta.default : true);

            for (const hideId of meta.hides) {
                this._setVisible(q(hideId), checked);
            }
        }

        // ============================================================
        // PRIORYTET 4+5+6: Pary data+label, etykiety, teksty, wartości
        // ============================================================
        for (const [fieldId, meta] of Object.entries(this._fields)) {
            const inputType = meta.input_type || "entity";

            // --- CONTACT --- (nie wymaga el — steruje wieloma stykami)
            if (inputType === "contact") {
                let angle = 0;

                const backupEnabled = this._mapping["inv1_backup_enabled"] === true;
                if (backupEnabled) {
                    const entityId = this._mapping["inv1_Backup_Mode-data"];
                    const stateObj = (entityId && entityId !== null)
                        ? this._hass.states[entityId]
                        : null;
                    if (stateObj && stateObj.state === "on") {
                        angle = -20;
                    }
                }

                const contacts = [
                    { id: "moving-contact-L1", cx: 440, cy: 180 },
                    { id: "moving-contact-L2", cx: 440, cy: 270 },
                    { id: "moving-contact-L3", cx: 440, cy: 360 },
                    { id: "moving-contact-N",  cx: 440, cy: 450 },
                ];
                for (const c of contacts) {
                    const contact = q(c.id);
                    if (contact) {
                        contact.setAttribute(
                            "transform",
                            angle !== 0 ? `rotate(${angle} ${c.cx} ${c.cy})` : ""
                        );
                    }
                }
                continue;
            }

            const el = q(fieldId);
            if (!el) continue;

            // --- ENTITY ---
            if (inputType === "entity") {
                const entityId = this._mapping[fieldId];
                const stateObj = entityId ? this._hass.states[entityId] : null;

                if (!stateObj) {
                    this._setVisible(el, false);
                    const labelId = fieldId.replace("-data", "-label");
                    this._setVisible(q(labelId), false);
                    continue;
                }

                const text = this._formatEntityValue(meta, stateObj);
                if (text === null) {
                    this._setVisible(el, false);
                    continue;
                }
                el.textContent = text;
                continue;
            }

            // --- LABEL ---
            if (inputType === "label") {
                if (el.style.display === "none") continue;

                if (meta.always_show) {
                    el.textContent = meta.label || fieldId;
                    continue;
                }

                let hasAny = false;
                if (meta.depends_on_any) {
                    hasAny = meta.depends_on_any.some((fId) => !!this._mapping[fId]);
                } else if (meta.depends_on) {
                    hasAny = !!this._mapping[meta.depends_on];
                } else {
                    const baseId = this._findBaseDataField(fieldId);
                    if (baseId) hasAny = !!this._mapping[baseId];
                }

                if (!hasAny) {
                    this._setVisible(el, false);
                    continue;
                }

                el.textContent = meta.label || fieldId;
                continue;
            }

            // --- TEXT ---
            if (inputType === "text") {
                const userText = this._mapping[fieldId];
                if (userText) {
                    el.textContent = userText;
                } else {
                    this._setVisible(el, false);
                }
                continue;
            }

            // --- TEXT_WITH_DEFAULT ---
            if (inputType === "text_with_default") {
                const userText = this._mapping[fieldId];
                const value = userText || meta.default || fieldId;
                el.textContent = value;
                continue;
            }

            // --- BOOLEAN / CHOICE ---
            if (inputType === "boolean" || inputType === "choice") continue;
        }

        // --- ANIMACJA WENTYLATORÓW ---
        this._updateFanAnimation();
        this._updateFroniusFanAnimation();
        this._updateFroniusErrorState();
        this._updateInv2Status();
    }

 _updateFanAnimation() {
        if (!this._svgRoot) return;
        
        const fanEnabled = this._mapping["heat_pump_fan_enabled"] === true;
        if (!fanEnabled) {
            this._fanRunning = false;
            return;
        }

        // Prędkości z encji
        const fan1Id = this._mapping["HeatPump-fan1-speed-data"];
        const fan2Id = this._mapping["HeatPump-fan2-speed-data"];

        const fan1 = (fan1Id && this._hass.states[fan1Id]) 
            ? parseFloat(this._hass.states[fan1Id].state) : 0;
        const fan2 = (fan2Id && this._hass.states[fan2Id]) 
            ? parseFloat(this._hass.states[fan2Id].state) : 0;

        const speed = Math.max(fan1, fan2);

        if (isNaN(speed) || speed < 10) {
            this._fanRunning = false;
            return;
        }

        // Animuj
        this._fanRunning = true;
        const rpm = Math.min(speed, 600);
        const period = 3.0 - (rpm / 600) * 2.0;  // 3s dla 0 RPM, 1s dla 600 RPM

        const now = performance.now();
        if (this._fanLastTime === 0) {
            this._fanLastTime = now;
            requestAnimationFrame((t) => this._animateFanFrame(t, period));
        }
    }

    _updateFroniusFanAnimation() {
        if (!this._svgRoot) return;

        const fanEnabled = this._mapping["inv1_fan_enabled"] === true;
        if (!fanEnabled) {
            this._froniusFanRunning = false;
            return;
        }

        const statusId = this._mapping["inv1_status_message-data"];
        const statusObj = (statusId && this._hass.states[statusId])
            ? this._hass.states[statusId]
            : null;

        if (!statusObj) {
            this._froniusFanRunning = false;
            return;
        }

        const isRunning = statusObj.state.toLowerCase() === "running";

        if (!isRunning) {
            this._froniusFanRunning = false;
            return;
        }

        if (!this._froniusFanRunning) {
            this._froniusFanRunning = true;
            this._froniusFanLastTime = performance.now();
            requestAnimationFrame((t) => this._animateFroniusFanFrame(t));
        }
    }

    _animateFroniusFanFrame(now) {
        if (!this._froniusFanRunning || !this._svgRoot) {
            this._froniusFanLastTime = 0;
            return;
        }

        const dt = (now - this._froniusFanLastTime) / 1000;
        this._froniusFanLastTime = now;

        const deltaAngle = 180 * dt;
        this._froniusFanAngle = (this._froniusFanAngle + deltaAngle) % 360;

        const fan = this._svgRoot.querySelector('[id="cooling-fan"]');
        if (fan) {
            fan.setAttribute("transform", `rotate(${this._froniusFanAngle} 264.5 207)`);
        }

        requestAnimationFrame((t) => this._animateFroniusFanFrame(t));
    }

    _updateFroniusErrorState() {
        if (!this._svgRoot) return;

        const statusId = this._mapping["inv1_status_message-data"];
        if (!statusId) return;

        const statusObj = this._hass.states[statusId];
        if (!statusObj) return;

        const isError = statusObj.state.toLowerCase() === "error";

        const body = this._svgRoot.querySelector('[id="inv1-body"]');
        if (!body) return;

        if (isError) {
            body.setAttribute("stroke", "#ff2222");
            body.setAttribute("stroke-width", "6");
        } else {
            body.setAttribute("stroke", "none");
            body.setAttribute("stroke-width", "0");
        }
    }
    _updateInv2Status() {
        if (!this._svgRoot) return;

        const statusId = this._mapping["inv2_status-data"];
        if (!statusId) return;

        const statusObj = this._hass.states[statusId];
        if (!statusObj) return;

        // SMA: Ok → zielona. Cokolwiek innego (Warning, Error, Fault, Off) → czerwona.
        const isOk = statusObj.state.startsWith("Ok");

        // Dioda LED falownika 2
        const led = this._svgRoot.querySelector('[id="led-green"]');
        if (led) {
            led.setAttribute("fill", isOk ? "#55ee67" : "#ff2222");
        }

        // Obudowa falownika 2
        const body = this._svgRoot.querySelector('[id="inv2-body"]');
        if (body) {
            if (isOk) {
                body.setAttribute("stroke", "#d0d2d4");
                body.setAttribute("stroke-width", "1.5");
            } else {
                body.setAttribute("stroke", "#ff2222");
                body.setAttribute("stroke-width", "6");
            }
        }
    }

    _animateFanFrame(now, period) {
        if (!this._fanRunning || !this._svgRoot) {
            this._fanLastTime = 0;
            return;
        }

        const dt = (now - this._fanLastTime) / 1000;
        this._fanLastTime = now;

        // Prędkość kątowa: 360° / period
        const deltaAngle = (360 / period) * dt;
        this._fanAngle = (this._fanAngle + deltaAngle) % 360;

        const q = (id) => this._svgRoot.querySelector(`[id="${id}"]`);
        const use1 = q("use28");
        const use2 = q("use29");

        if (use1) use1.setAttribute("transform", `rotate(${this._fanAngle} 400 315)`);
        if (use2) use2.setAttribute("transform", `rotate(${this._fanAngle} 400 635)`);

        requestAnimationFrame((t) => this._animateFanFrame(t, period));
    }

    render() {
        if (!this.shadowRoot) return;

        if (!this.shadowRoot.querySelector(".svg-container")) {
            this.shadowRoot.innerHTML = `
                <style>
                    :host { display: block; }
                    ha-card { overflow: hidden; }
                    .svg-container { width: 100%; }
                    .svg-container svg { display: block; width: 100%; height: auto; }
                </style>
                <ha-card>
                    <div class="svg-container">
                        <div style="padding:16px;color:#888;">Loading EnergyFlowDashboard...</div>
                    </div>
                </ha-card>
            `;
        }

        if (this._loaded) {
            this._applyValues();
        }
    }

    getCardSize() {
        return 12;
    }
}

window.customCards = window.customCards || [];
window.customCards.push({
    type: "energy-flow-dashboard",
    name: "Energy Flow Dashboard",
    description: "Energy flow visualization",
});

customElements.define("energy-flow-dashboard", EnergyFlowDashboard);