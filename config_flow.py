"""Config flow for EnergyFlowDashboard."""

import logging

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.data_entry_flow import section
from homeassistant.helpers import selector

from .const import DOMAIN, NAME, SVG_FIELDS, DEVICES

_LOGGER = logging.getLogger(__name__)


# ============================================================
# TEXTS — JEDYNE MIEJSCE DO ZMIANY JĘZYKA W KONFIGURATORZE
# ============================================================
# Zmieniasz wartości w tym słowniku → zmieniasz język etykiet pól.
# Klucze MUSZĄ zostać takie same (to ID pól z const.py).
#
# Uwaga: lista urządzeń w kroku "user" NIE korzysta z tego słownika —
# ona czyta z translations/<lang>.json (sekcja "device").
# ============================================================

TEXTS = {
    # --- Inverter 1 ---
    "inv1_name": "Nazwa inwertera 1",
    "inv1_mppt_count": "Liczba MPPT",
    "inv1_mppt1_name": "Nazwa MPPT 1",
    "inv1_mppt2_name": "Nazwa MPPT 2",
    "inv1_mppt3_name": "Nazwa MPPT 3",
    "inv1_name_visible": "Pokaż nazwę inwertera",
    "inv1_mppt_labels_visible": "Pokaż etykiety MPPT",
    "inv1_pdc-data": "Pdc (moc DC)",
    "inv1_pac-data": "Pac (moc AC)",
    "inv1_Backup_Mode-data": "Tryb Backup",
    "inv1_mppt1_vdc": "MPPT1 – napięcie",
    "inv1_mppt1_adc": "MPPT1 – prąd",
    "inv1_mppt1_pdc": "MPPT1 – moc",
    "inv1_mppt2_vdc": "MPPT2 – napięcie",
    "inv1_mppt2_adc": "MPPT2 – prąd",
    "inv1_mppt2_pdc": "MPPT2 – moc",
    "inv1_mppt3_vdc": "MPPT3 – napięcie",
    "inv1_mppt3_adc": "MPPT3 – prąd",
    "inv1_mppt3_pdc": "MPPT3 – moc",
    "inv1_backup_enabled": "Tryb full backup",
    "full_backup_state": "Stycznik (wizualizacja)",
    "inv1_fan_enabled": "Animacja wentylatora",
    "inv1_status_message-data": "Status falownika (running)",

    # --- Inverter 2 ---
    "inv2_name": "Nazwa inwertera 2",
    "inv2_mppt_count": "Liczba MPPT",
    "inv2_mppt1_name": "Nazwa MPPT 1",
    "inv2_mppt2_name": "Nazwa MPPT 2",
    "inv2_mppt3_name": "Nazwa MPPT 3",
    "inv2_mppt_labels_visible": "Pokaż etykiety MPPT",
    "inv2_pdc-data": "Pdc (moc DC)",
    "inv2_pac-data": "Pac (moc AC)",
    "inv2_Backup_Mode-data": "Tryb Backup",
    "inv2_mppt1_vdc": "MPPT1 – napięcie",
    "inv2_mppt1_adc": "MPPT1 – prąd",
    "inv2_mppt1_pdc": "MPPT1 – moc",
    "inv2_mppt2_vdc": "MPPT2 – napięcie",
    "inv2_mppt2_adc": "MPPT2 – prąd",
    "inv2_mppt2_pdc": "MPPT2 – moc",
    "inv2_mppt3_vdc": "MPPT3 – napięcie",
    "inv2_mppt3_adc": "MPPT3 – prąd",
    "inv2_mppt3_pdc": "MPPT3 – moc",
    "inv2_status-data": "Status falownika 2 (Ok)",

    # --- Bateria ---
    "EnergyStorageName": "Nazwa magazynu",
    "battery_name_visible": "Pokaż nazwę magazynu",
    "EnergyStorageCapacity": "Pojemność",
    "EnergyStorageSOC": "SOC (stan naładowania)",
    "EnergyStoragePower": "Moc",
    "EnergyStorageStateChargeDischarge": "Stan (ładowanie/rozładowanie)",

    # --- Pompa ciepła ---
    "heat_pump_labels_visible": "Pokaż etykiety",
    "HeatPump-current-L1-data": "Prąd L1",
    "HeatPump-current-L2-data": "Prąd L2",
    "HeatPump-current-L3-data": "Prąd L3",
    "HeatPump-power-L1-data": "Moc L1",
    "HeatPump-power-L2-data": "Moc L2",
    "HeatPump-power-L3-data": "Moc L3",
    "HeatPump-power-total-data": "Moc całkowita",
    "heat_pump_fan_enabled": "Animacja wentylatorów",
    "HeatPump-fan1-speed-data": "Wentylator 1 — prędkość",
    "HeatPump-fan2-speed-data": "Wentylator 2 — prędkość",

    # --- Rozdzielnica 1 ---
    "AC_SubBoard1_label": "Nazwa rozdzielnicy",
    "subboard_1_name_visible": "Pokaż nazwę",
    "subboard_1_voltage_labels_visible": "Pokaż etykietę napięcia",
    "subboard_1_current_labels_visible": "Pokaż etykietę prądu",
    "subboard_1_power_label_visible": "Pokaż etykietę mocy",
    "subboard_1_energy_label_visible": "Pokaż etykietę energii",
    "AC_subboard1_Voltage_label": "Etykieta napięcia",
    "AC_subboard1_": "Etykieta prądu",
    "AC_subboard1_VAC_L1": "Napięcie L1",
    "AC_subboard1_VAC_L2": "Napięcie L2",
    "AC_subboard1_VAC_L3": "Napięcie L3",
    "AC_subboard1_Curr_L1": "Prąd L1",
    "AC_subboard1_Curr_L2": "Prąd L2",
    "AC_subboard1_Curr_L3": "Prąd L3",
    "AC_subboard1_Power_Total_data": "Moc całkowita",
    "AC_subboard1_Energy_Produced-data": "Energia dziś",

    # --- Rozdzielnica 2 ---
    "AC_SubBoard2_label": "Nazwa rozdzielnicy",
    "AC_SubBoard2_power_supply": "Rodzaj zasilania (tekst)",
    "AC_SubBoard2_power_supply-grid": "GRID (tekst)",
    "AC_SubBoard2_power_supply-backup": "Backup (tekst)",
    "subboard_2_name_visible": "Pokaż nazwę",
    "subboard_2_power_supply_label_visible": "Pokaż etykietę zasilania",
    "subboard_2_battery_label_visible": "Pokaż etykietę baterii",
    "AC_SubBoard2_battery_SOC-data": "Bateria SOC",

    # --- Dom ---
    "home_phase_labels_visible": "Pokaż etykiety faz",
    "home_current_labels_visible": "Pokaż etykiety prądu",
    "home_power_labels_visible": "Pokaż etykiety mocy",
    "home-current-l1-data": "Prąd L1",
    "home-current-l2-data": "Prąd L2",
    "home-current-l3-data": "Prąd L3",
    "home-power-l1-data": "Moc L1",
    "home-power-l2-data": "Moc L2",
    "home-power-l3-data": "Moc L3",
    "total-power-data": "Moc łączna",

    # --- Sieć / OSD ---
    "grid_phase_labels_visible": "Pokaż etykiety faz",
    "grid_voltage_labels_visible": "Pokaż etykiety napięcia",
    "grid_current_labels_visible": "Pokaż etykiety prądu",
    "grid_meter_labels_visible": "Pokaż etykiety licznika",
    "grid-voltage-l1-data": "Napięcie L1",
    "grid-voltage-l2-data": "Napięcie L2",
    "grid-voltage-l3-data": "Napięcie L3",
    "grid-current-l1-data": "Prąd L1",
    "grid-current-l2-data": "Prąd L2",
    "grid-current-l3-data": "Prąd L3",
    "meter-power-data": "Moc licznika",
    "meter-power-produced_day-data": "Energia dziś",
}


# ============================================================
# DEFINICJE SEKCJI — per urządzenie
# ============================================================

DEVICE_SECTIONS = {
    "inverter_1": [
        {"id": "name",       "fields": ["inv1_name"]},
        {"id": "mppt_conf",  "fields": ["inv1_mppt_count"]},
        {"id": "mppt_name",  "fields": ["inv1_mppt1_name", "inv1_mppt2_name", "inv1_mppt3_name"]},
        {"id": "visibility", "fields": ["inv1_name_visible", "inv1_mppt_labels_visible"]},
        {"id": "data",       "fields": [
            "inv1_pdc-data", "inv1_pac-data", "inv1_Backup_Mode-data",
            "inv1_mppt1_vdc", "inv1_mppt1_adc", "inv1_mppt1_pdc",
            "inv1_mppt2_vdc", "inv1_mppt2_adc", "inv1_mppt2_pdc",
            "inv1_mppt3_vdc", "inv1_mppt3_adc", "inv1_mppt3_pdc",
        ]},
        {"id": "backup", "fields": ["inv1_backup_enabled"]},
        {"id": "animation", "fields": [
            "inv1_fan_enabled",
            "inv1_status_message-data",
        ]},
    ],
    "inverter_2": [
        {"id": "name",       "fields": ["inv2_name"]},
        {"id": "mppt_conf",  "fields": ["inv2_mppt_count"]},
        {"id": "mppt_name",  "fields": ["inv2_mppt1_name", "inv2_mppt2_name", "inv2_mppt3_name"]},
        {"id": "visibility", "fields": ["inv2_mppt_labels_visible"]},
        {"id": "data",       "fields": [
            "inv2_pdc-data", "inv2_pac-data", "inv2_Backup_Mode-data",
            "inv2_mppt1_vdc", "inv2_mppt1_adc", "inv2_mppt1_pdc",
            "inv2_mppt2_vdc", "inv2_mppt2_adc", "inv2_mppt2_pdc",
            "inv2_mppt3_vdc", "inv2_mppt3_adc", "inv2_mppt3_pdc",
        ]},
        {"id": "animation", "fields": ["inv2_status-data"]},
        
    ],
    "battery": [
        {"id": "name",       "fields": ["EnergyStorageName"]},
        {"id": "visibility", "fields": ["battery_name_visible","battery_SOC-label_visible","battery_Temp-label_visible","battery_Voltage-label_visible","battery_Current-label_visible","battery_Power-label_visible",]},
        {"id": "data",       "fields": [
            "EnergyStorageCapacity", "EnergyStorageSOC-data",
            "EnergyStoragePower-data", "EnergyStorageStateChargeDischarge",
            "EnergyStorageTemp-data","Battery_Current-data","Battery_Vdc-data",
        ]},
    ],
    "heat_pump": [
        {"id": "visibility", "fields": ["heat_pump_labels_visible"]},
        {"id": "data",       "fields": [
            "HeatPump-current-L1-data", "HeatPump-current-L2-data", "HeatPump-current-L3-data",
            "HeatPump-power-L1-data", "HeatPump-power-L2-data", "HeatPump-power-L3-data",
            "HeatPump-power-total-data",
        ]},
        {"id": "animation",  "fields": [
            "heat_pump_fan_enabled",
            "HeatPump-fan1-speed-data",
            "HeatPump-fan2-speed-data",
        ]},
    ],
    "subboard_1": [
        {"id": "name",       "fields": ["AC_SubBoard1_label","AC_subboard1_Voltage_label","AC_subboard1_Current-label",]},
        {"id": "visibility", "fields": [
            "subboard_1_name_visible", "subboard_1_voltage_labels_visible",
            "subboard_1_current_labels_visible", "subboard_1_power_label_visible",
            "subboard_1_energy_label_visible",
        ]},
        {"id": "data",       "fields": [
            "AC_subboard1_VAC_L1", "AC_subboard1_VAC_L2", "AC_subboard1_VAC_L3",
            "AC_subboard1_Curr_L1", "AC_subboard1_Curr_L2", "AC_subboard1_Curr_L3",
            "AC_subboard1_Power_Total_data", "AC_subboard1_Energy_Produced-data",
        ]},
    ],
    "subboard_2": [
        {"id": "name",       "fields": ["AC_SubBoard2_label"]},
        {"id": "texts",      "fields": [
            "AC_SubBoard2_power_supply", "AC_SubBoard2_power_supply-grid",
            "AC_SubBoard2_power_supply-backup",
        ]},
        {"id": "visibility", "fields": [
            "subboard_2_name_visible", "subboard_2_power_supply_label_visible",
            "subboard_2_battery_label_visible",
        ]},
        {"id": "data",       "fields": ["AC_SubBoard2_battery_SOC-data"]},
    ],
    "home": [
        {"id": "visibility", "fields": [
            "home_phase_labels_visible", "home_current_labels_visible",
            "home_power_labels_visible",
        ]},
        {"id": "data",       "fields": [
            "home-current-l1-data", "home-current-l2-data", "home-current-l3-data",
            "home-power-l1-data", "home-power-l2-data", "home-power-l3-data",
            "total-power-data",
        ]},
    ],
    "grid": [
        {"id": "visibility", "fields": [
            "grid_phase_labels_visible", "grid_voltage_labels_visible",
            "grid_current_labels_visible", "grid_meter_labels_visible",
        ]},
        {"id": "data",       "fields": [
            "grid-voltage-l1-data", "grid-voltage-l2-data", "grid-voltage-l3-data",
            "grid-current-l1-data", "grid-current-l2-data", "grid-current-l3-data",
            "meter-power-data", "meter-power-produced_day-data",
            "full_backup_state",
        ]},
    ],
}


# ============================================================
# BUDOWANIE POJEDYNCZEGO POLA
# ============================================================
def _build_field(field_id: str, current: dict):
    """Zbuduj pojedyncze pole — zwraca (selector, kwargs).

    Dla każdego typu przekazujemy aktualną wartość (z 'current'),
    żeby formularz pokazywał zapisane dane po ponownym otwarciu.
    """
    meta = SVG_FIELDS.get(field_id, {})
    input_type = meta.get("input_type", "entity")
    suggested = current.get(field_id)

    # --- BOOLEAN ---
    if input_type == "boolean":
        default = current.get(field_id, meta.get("default", True))
        return selector.BooleanSelector(), {"default": default}

    # --- CHOICE ---
    if input_type == "choice":
        options = meta.get("options", [])
        default = current.get(
            field_id,
            meta.get("default", options[0] if options else ""),
        )
        return (
            selector.SelectSelector(
                selector.SelectSelectorConfig(
                    options=options,
                    mode=selector.SelectSelectorMode.DROPDOWN,
                )
            ),
            {"default": default},
        )

    # --- TEXT ---
    if input_type == "text":
        kwargs = {}
        if suggested:
            kwargs["default"] = suggested
        return selector.TextSelector(), kwargs

    # --- TEXT_WITH_DEFAULT ---
    if input_type == "text_with_default":
        default_val = meta.get("default", "")
        suggestion = suggested if suggested else default_val
        kwargs = {}
        if suggestion:
            kwargs["description"] = {"suggested_value": suggestion}
        return selector.TextSelector(), kwargs

    # --- ENTITY ---
    kwargs = {}
    if suggested:
        # dla EntitySelector wartość przekazujemy przez `default`
        kwargs["description"] = {"suggested_value": suggested}
    return (
        selector.EntitySelector(
            selector.EntitySelectorConfig(
                domain=[
                    "sensor",
                    "binary_sensor",
                    "input_number",
                    "input_boolean",
                    "switch",
                ]
            )
        ),
        kwargs,
    )

# ============================================================
# BUDOWANIE SCHEMATU DLA URZĄDZENIA (Z SEKCJAMI)
# ============================================================
def _build_schema_for_device(device_id: str, current: dict) -> dict:
    """Zbuduj schemat z sekcjami dla pól konkretnego urządzenia.

    Etykiety pól pochodzą ze słownika TEXTS.
    Aktualne wartości (z 'current') są przekazywane przez 'default'
    w vol.Optional — dzięki temu po ponownym otwarciu formularza
    pola pokazują zapisane dane.
    """
    schema = {}
    device_sections = DEVICE_SECTIONS.get(device_id, [])

    for sec in device_sections:
        section_id = sec["id"]
        section_fields = {}

        for field_id in sec["fields"]:
            meta = SVG_FIELDS.get(field_id)
            if not meta:
                continue
            input_type = meta.get("input_type", "entity")
            if input_type == "label":
                continue

            field_selector, kwargs = _build_field(field_id, current)

            # NIE nadpisujemy description — bo dla text_with_default
            # już tam jest suggested_value. Etykieta pola i tak pochodzi
            # z translations/<lang>.json (config_subentries...data).
            # Ale zachowujemy etykietę z TEXTS jako fallback dla pól,
            # które nie mają tłumaczenia w pl.json.
            if "description" not in kwargs:
                kwargs["description"] = {"suggested_value": None}
                kwargs["description"] = TEXTS.get(field_id, field_id)

            section_fields[vol.Optional(field_id, **kwargs)] = field_selector

        if not section_fields:
            continue

        schema[vol.Optional(section_id)] = section(
            vol.Schema(section_fields),
            {"collapsed": True},
        )

    return schema

# ============================================================
# CZYSZCZENIE DANYCH WPROWADZONYCH
# ============================================================
def _clean_input(user_input: dict) -> dict:
    """Wyczyść dane wejściowe — spłaszcz sekcje.

    Puste pola zapisujemy jako None — dzięki temu HA NADPISZE
    starą wartość i można USUNĄĆ encję z konfiguracji.
    """
    cleaned = {}

    def _process_field(key: str, value):
        meta = SVG_FIELDS.get(key, {})
        input_type = meta.get("input_type", "entity")
        if input_type == "boolean":
            cleaned[key] = bool(value)
        else:
            # Puste → None (nadpisze starą wartość)
            cleaned[key] = value if value not in (None, "") else None

    for key, value in user_input.items():
        if isinstance(value, dict):
            # dane z sekcji
            for sub_key, sub_value in value.items():
                _process_field(sub_key, sub_value)
        else:
            _process_field(key, value)

    return cleaned


# ============================================================
# GŁÓWNY CONFIG FLOW
# ============================================================
class EnergyFlowDashboardConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for EnergyFlowDashboard."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")
        if user_input is not None:
            return self.async_create_entry(title=NAME, data=user_input)
        return self.async_show_form(step_id="user", data_schema=vol.Schema({}))

    @staticmethod
    def async_get_options_flow(config_entry):
        return EnergyFlowDashboardOptionsFlow()

    @classmethod
    def async_get_supported_subentry_types(cls, config_entry):
        return {"device": EnergyFlowDashboardSubentryFlow}


# ============================================================
# OPTIONS FLOW (puste — globalne)
# ============================================================
class EnergyFlowDashboardOptionsFlow(config_entries.OptionsFlow):
    """Options flow — ustawienia globalne (na razie puste)."""

    async def async_step_init(self, user_input=None):
        return self.async_create_entry(title="", data={})


# ============================================================
# SUBENTRY FLOW (per urządzenie)
# ============================================================
class EnergyFlowDashboardSubentryFlow(config_entries.ConfigSubentryFlow):
    """Handle subentry flow — konfiguracja pojedynczego urządzenia."""

    async def async_step_user(self, user_input=None):
        """Krok 1: wybór urządzenia do dodania."""
        if user_input is not None:
            device_id = user_input["device_id"]
            self._selected_device_id = device_id
            return await self.async_step_configure()

        # Lista urządzeń — tłumaczenia z translations/<lang>.json (sekcja "device")
        from .websocket_api import _load_translations
        _, device_labels = await _load_translations(self.hass)

        entry = self._get_entry()
        existing = [
            sub.data.get("device_id")
            for sub in entry.subentries.values()
        ]

        options = []
        for dev_id in DEVICES.keys():
            if dev_id in existing:
                continue
            label_key = DEVICES[dev_id].get("label_key", dev_id)
            default_label = DEVICES[dev_id].get("default_label", dev_id)
            # Priorytet: pl.json → default_label (z const.py)
            label = device_labels.get(label_key) or default_label
            options.append({"value": dev_id, "label": label})

        if not options:
            return self.async_abort(reason="all_devices_configured")

        schema = vol.Schema({
            vol.Required("device_id"): selector.SelectSelector(
                selector.SelectSelectorConfig(
                    options=options,
                    mode=selector.SelectSelectorMode.LIST,
                )
            ),
        })

        return self.async_show_form(step_id="user", data_schema=schema)

    async def async_step_configure(self, user_input=None):
        """Krok 2: konfiguracja pól urządzenia (z sekcjami)."""
        device_id = self._selected_device_id
        device_meta = DEVICES.get(device_id, {})

        # Tytuł subentry — z default_label (na sztywno), bo HA nie tłumaczy tytułów
        device_title = device_meta.get("default_label", device_id)

        if user_input is not None:
            cleaned = _clean_input(user_input)
            cleaned["device_id"] = device_id
            return self.async_create_entry(
                title=device_title,
                data=cleaned,
            )

        current = {}
        schema_dict = _build_schema_for_device(device_id, current)
        schema = vol.Schema(schema_dict)

        return self.async_show_form(
            step_id="configure",
            data_schema=schema,
        )

    async def async_step_reconfigure(self, user_input=None):
        """Rekonfiguracja istniejącego urządzenia."""
        entry = self._get_entry()
        subentry = self._get_reconfigure_subentry()
        device_id = subentry.data.get("device_id")

        if device_id is None:
            return self.async_abort(reason="device_id_missing")

        self._selected_device_id = device_id
        device_meta = DEVICES.get(device_id, {})
        device_title = device_meta.get("default_label", device_id)

        if user_input is not None:
            cleaned = _clean_input(user_input)
            cleaned["device_id"] = device_id
            return self.async_update_reload_and_abort(
                entry,
                subentry,
                title=device_title,
                data=cleaned,
            )

        current = dict(subentry.data or {})
        schema_dict = _build_schema_for_device(device_id, current)
        schema = vol.Schema(schema_dict)

        return self.async_show_form(
            step_id="reconfigure",
            data_schema=schema,
        )