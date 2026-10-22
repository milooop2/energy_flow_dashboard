"""Constants for EnergyFlowDashboard."""

DOMAIN = "energy_flow_dashboard"
NAME = "EnergyFlowDashboard"
VERSION = "0.4.4"

# ============================================================
# DEFINICJE URZĄDZEŃ
# ============================================================
# always_present: True  → subentry tworzone automatycznie
# always_present: False → użytkownik dodaje ręcznie (przycisk +)
#
# default_label — używane jako fallback, gdy brak tłumaczenia w pl.json
# label_key     — klucz w translations/<lang>.json → sekcja "device"

DEVICES = {
    "inverter_1": {"label_key": "device_inverter_1", "default_label": "Falownik 1 (Fronius)",       "icon": "mdi:solar-power-variant",         "always_present": True},
    "inverter_2": {"label_key": "device_inverter_2", "default_label": "Falownik 2 (SMA)",           "icon": "mdi:solar-power-variant-outline", "always_present": False},
    "battery":    {"label_key": "device_battery",    "default_label": "Bateria",                    "icon": "mdi:battery-high",                "always_present": False},
    "heat_pump":  {"label_key": "device_heat_pump",  "default_label": "Pompa ciepła",               "icon": "mdi:heat-pump",                   "always_present": False},
    "subboard_1": {"label_key": "device_subboard_1", "default_label": "Rozdzielnica 1 (gospodarcza)","icon": "mdi:home-lightning-bolt",         "always_present": True},
    "subboard_2": {"label_key": "device_subboard_2", "default_label": "Rozdzielnica 2 (kotłownia)", "icon": "mdi:water-boiler",                "always_present": True},
    "home":       {"label_key": "device_home",       "default_label": "Dom",                        "icon": "mdi:home",                        "always_present": True},
    "grid":       {"label_key": "device_grid",       "default_label": "Sieć / OSD",                 "icon": "mdi:transmission-tower",          "always_present": True},
}

# ============================================================
# DEFINICJE PÓL (SVG)
# ============================================================
# input_type:
#   "entity"              → wartość z encji HA
#   "label"               → friendly_name z encji bazowej
#   "text"                → tekst wpisany ręcznie
#   "text_with_default"   → tekst wpisany ręcznie LUB wartość z "default"
#   "boolean"             → przełącznik on/off (checkbox)
#   "choice"              → wybór z opcji (dropdown)
#
# device: do jakiego urządzenia należy pole
# hides: lista ID elementów SVG, które ukrywa checkbox
# hides_map: mapa wartości → lista ID (choice)
# depends_on / depends_on_any: pole bazowe dla "label"
# default: wartość domyślna
# always_show: true = etykieta zawsze widoczna (nawet bez danych)

SVG_FIELDS = {
    # ============================================================
    # INVERTER 1 (Fronius)
    # ============================================================
    "inv1_name_visible":        {"input_type": "boolean", "device": "inverter_1", "label_key": "inv1_name_visible",        "default": True, "hides": ["inv1_name"]},
    "inv1_mppt_labels_visible": {"input_type": "boolean", "device": "inverter_1", "label_key": "inv1_mppt_labels_visible", "default": True, "hides": ["inv1_mppt1_name", "inv1_mppt2_name", "inv1_mppt3_name"]},
    "inv1_backup_enabled"   :   {"input_type": "boolean", "device": "inverter_1", "label_key": "inv1_backup_enabled",       "default": False,    },
    "inv1_fan_enabled":         {"input_type": "boolean", "device": "inverter_1", "label_key": "inv1_fan_enabled",       "default": False},
    "inv1_status_message-data": {"input_type": "entity",  "device": "inverter_1", "label_key": "inv1_status_message",  "prefix": "", "device_class": None},

    "inv1_mppt_count": {
        "input_type": "choice",
        "device": "inverter_1",
        "label_key": "inv1_mppt_count",
        "options": ["1", "2", "3"],
        "default": "3",
        "hides_map": {"1": ["inv1_mppt2", "inv1_mppt3"], "2": ["inv1_mppt3"], "3": []},
    },

    "inv1_name": {"input_type": "text", "device": "inverter_1", "label_key": "inv1_name"},

    "inv1_mppt1_name": {"input_type": "text_with_default", "device": "inverter_1", "label_key": "inv1_mppt1_name", "default": "MPPT 1"},
    "inv1_mppt2_name": {"input_type": "text_with_default", "device": "inverter_1", "label_key": "inv1_mppt2_name", "default": "MPPT 2"},
    "inv1_mppt3_name": {"input_type": "text_with_default", "device": "inverter_1", "label_key": "inv1_mppt3_name", "default": "MPPT 3"},

    "inv1_pdc-data":          {"input_type": "entity", "device": "inverter_1", "label_key": "inv1_pdc",               "prefix": "", "device_class": "power"},
    "inv1_pdc-label":         {"input_type": "label",  "device": "inverter_1", "label_key": "inv1_pdc_label",         "depends_on": "inv1_pdc-data"},
    "inv1_pac-data":          {"input_type": "entity", "device": "inverter_1", "label_key": "inv1_pac",               "prefix": "", "device_class": "power"},
    "inv1_pac-label":         {"input_type": "label",  "device": "inverter_1", "label_key": "inv1_pac_label",         "depends_on": "inv1_pac-data"},
    "inv1_Backup_Mode-data":  {"input_type": "entity", "device": "inverter_1", "label_key": "inv1_backup_mode",       "prefix": "", "device_class": None},
    "inv1_Backup_Mode-label": {"input_type": "label",  "device": "inverter_1", "label_key": "inv1_backup_mode_label", "depends_on": "inv1_Backup_Mode-data"},

    "inv1_mppt1_vdc": {"input_type": "entity", "device": "inverter_1", "label_key": "inv1_mppt1_vdc", "prefix": "", "device_class": "voltage"},
    "inv1_mppt1_adc": {"input_type": "entity", "device": "inverter_1", "label_key": "inv1_mppt1_adc", "prefix": "", "device_class": "current"},
    "inv1_mppt1_pdc": {"input_type": "entity", "device": "inverter_1", "label_key": "inv1_mppt1_pdc", "prefix": "", "device_class": "power"},
    "inv1_mppt2_vdc": {"input_type": "entity", "device": "inverter_1", "label_key": "inv1_mppt2_vdc", "prefix": "", "device_class": "voltage"},
    "inv1_mppt2_adc": {"input_type": "entity", "device": "inverter_1", "label_key": "inv1_mppt2_adc", "prefix": "", "device_class": "current"},
    "inv1_mppt2_pdc": {"input_type": "entity", "device": "inverter_1", "label_key": "inv1_mppt2_pdc", "prefix": "", "device_class": "power"},
    "inv1_mppt3_vdc": {"input_type": "entity", "device": "inverter_1", "label_key": "inv1_mppt3_vdc", "prefix": "", "device_class": "voltage"},
    "inv1_mppt3_adc": {"input_type": "entity", "device": "inverter_1", "label_key": "inv1_mppt3_adc", "prefix": "", "device_class": "current"},
    "inv1_mppt3_pdc": {"input_type": "entity", "device": "inverter_1", "label_key": "inv1_mppt3_pdc", "prefix": "", "device_class": "power"},

    # ============================================================
    # INVERTER 2 (SMA)
    # ============================================================
    "inv2_mppt_labels_visible": {"input_type": "boolean", "device": "inverter_2", "label_key": "inv2_mppt_labels_visible", "default": True, "hides": ["inv2_mppt1_name", "inv2_mppt2_name", "inv2_mppt3_name"]},

    "inv2_mppt_count": {
        "input_type": "choice",
        "device": "inverter_2",
        "label_key": "inv2_mppt_count",
        "options": ["1", "2", "3"],
        "default": "3",
        "hides_map": {"1": ["inv2_mppt2", "inv2_mppt3"], "2": ["inv2_mppt3"], "3": []},
    },

    "inv2_name": {"input_type": "text", "device": "inverter_2", "label_key": "inv2_name"},
    "inv2_status-data": {"input_type": "entity", "device": "inverter_2", "label_key": "inv2_status", "prefix": "", "device_class": None},
    

    "inv2_mppt1_name": {"input_type": "text_with_default", "device": "inverter_2", "label_key": "inv2_mppt1_name", "default": "MPPT 1"},
    "inv2_mppt2_name": {"input_type": "text_with_default", "device": "inverter_2", "label_key": "inv2_mppt2_name", "default": "MPPT 2"},
    "inv2_mppt3_name": {"input_type": "text_with_default", "device": "inverter_2", "label_key": "inv2_mppt3_name", "default": "MPPT 3"},

    "inv2_pdc-data":          {"input_type": "entity", "device": "inverter_2", "label_key": "inv2_pdc",               "prefix": "", "device_class": "power"},
    "inv2_pdc-label":         {"input_type": "label",  "device": "inverter_2", "label_key": "inv2_pdc_label",         "depends_on": "inv2_pdc-data"},
    "inv2_pac-data":          {"input_type": "entity", "device": "inverter_2", "label_key": "inv2_pac",               "prefix": "", "device_class": "power"},
    "inv2_pac-label":         {"input_type": "label",  "device": "inverter_2", "label_key": "inv2_pac_label",         "depends_on": "inv2_pac-data"},
    "inv2_Backup_Mode-data":  {"input_type": "entity", "device": "inverter_2", "label_key": "inv2_backup_mode",       "prefix": "", "device_class": None},
    "inv2_Backup_Mode-label": {"input_type": "label",  "device": "inverter_2", "label_key": "inv2_backup_mode_label", "depends_on": "inv2_Backup_Mode-data"},

    "inv2_mppt1_vdc": {"input_type": "entity", "device": "inverter_2", "label_key": "inv2_mppt1_vdc", "prefix": "", "device_class": "voltage"},
    "inv2_mppt1_adc": {"input_type": "entity", "device": "inverter_2", "label_key": "inv2_mppt1_adc", "prefix": "", "device_class": "current"},
    "inv2_mppt1_pdc": {"input_type": "entity", "device": "inverter_2", "label_key": "inv2_mppt1_pdc", "prefix": "", "device_class": "power"},
    "inv2_mppt2_vdc": {"input_type": "entity", "device": "inverter_2", "label_key": "inv2_mppt2_vdc", "prefix": "", "device_class": "voltage"},
    "inv2_mppt2_adc": {"input_type": "entity", "device": "inverter_2", "label_key": "inv2_mppt2_adc", "prefix": "", "device_class": "current"},
    "inv2_mppt2_pdc": {"input_type": "entity", "device": "inverter_2", "label_key": "inv2_mppt2_pdc", "prefix": "", "device_class": "power"},
    "inv2_mppt3_vdc": {"input_type": "entity", "device": "inverter_2", "label_key": "inv2_mppt3_vdc", "prefix": "", "device_class": "voltage"},
    "inv2_mppt3_adc": {"input_type": "entity", "device": "inverter_2", "label_key": "inv2_mppt3_adc", "prefix": "", "device_class": "current"},
    "inv2_mppt3_pdc": {"input_type": "entity", "device": "inverter_2", "label_key": "inv2_mppt3_pdc", "prefix": "", "device_class": "power"},

    # ============================================================
    # BATERIA
    # ============================================================
    "battery_name_visible": {"input_type": "boolean", "device": "battery", "label_key": "battery_name_visible", "default": True, "hides": ["EnergyStorageName"]},
    "battery_SOC-label_visible": {"input_type": "boolean", "device": "battery", "label_key": "storage_soc-label", "default": True, "hides": ["EnergyStorageSOC-label"]},
    "battery_Temp-label_visible": {"input_type": "boolean", "device": "battery", "label_key": "storage_temp-label", "default": True, "hides": ["EnergyStorageTemp-label"]},
    "battery_Voltage-label_visible": {"input_type": "boolean", "device": "battery", "label_key": "storage_voltage-label", "default": True, "hides": ["Battery_Vdc-label"]},
    "battery_Current-label_visible": {"input_type": "boolean", "device": "battery", "label_key": "storage_current-label", "default": True, "hides": ["Battery_Current-label"]},
    "battery_Power-label_visible": {"input_type": "boolean", "device": "battery", "label_key": "storage_power-label", "default": True, "hides": ["EnergyStoragePower-label"]},
    
    "EnergyStorageName": {"input_type": "text", "device": "battery", "label_key": "storage_name"},

    "EnergyStorageCapacity":             {"input_type": "entity", "device": "battery", "label_key": "storage_capacity", "prefix": "", "device_class": "energy_storage"},
    "EnergyStorageSOC-label":            {"input_type": "label", "device": "battery", "label_key": "storage_soc-label",      "depends_on": "EnergyStorageSOC-data"},
    "EnergyStorageSOC-data":             {"input_type": "entity", "device": "battery", "label_key": "storage_soc-data",      "prefix": "", "device_class": "battery"},
    "EnergyStorageTemp-label":           {"input_type": "label", "device": "battery", "label_key": "storage_temp-label",      "depends_on": "EnergyStorageTemp-data"},
    "EnergyStorageTemp-data":            {"input_type": "entity", "device": "battery", "label_key": "storage_temp-data",      "prefix": "", "device_class": "temperature"},
    "EnergyStoragePower-label":          {"input_type": "label", "device": "battery", "label_key": "storage_power-label",    "depends_on": "EnergyStoragePower-data"},
    "EnergyStoragePower-data":           {"input_type": "entity", "device": "battery", "label_key": "storage_power-data",    "prefix": "", "device_class": "power"},
    "Battery_Current-label":             {"input_type": "label", "device": "battery", "label_key": "storage_current-label",    "depends_on": "Battery_Current-data"},
    "Battery_Current-data":              {"input_type": "entity", "device": "battery", "label_key": "storage_current-data",    "prefix": "", "device_class": "current"},
    "Battery_Vdc-label":                 {"input_type": "label", "device": "battery", "label_key": "storage_voltage-label",    "depends_on": "Battery_Vdc-data"},
    "Battery_Vdc-data":                  {"input_type": "entity", "device": "battery", "label_key": "storage_voltage-data",    "prefix": "", "device_class": "voltage"},
    "EnergyStorageStateChargeDischarge": {"input_type": "entity", "device": "battery", "label_key": "storage_state",    "prefix": "State: ", "device_class": None},

    # ============================================================
    # POMPA CIEPŁA
    # ============================================================
    "heat_pump_labels_visible": {"input_type": "boolean", "device": "heat_pump", "label_key": "heat_pump_labels_visible", "default": True, "hides": ["HeatPump-power-label", "HeatPump-current-label", "HeatPump-power-total-label"]},

    "HeatPump-power-label":       {"input_type": "label", "device": "heat_pump", "label_key": "hp_power_label",       "depends_on_any": ["HeatPump-power-L1-data", "HeatPump-power-L2-data", "HeatPump-power-L3-data"]},
    "HeatPump-current-label":     {"input_type": "label", "device": "heat_pump", "label_key": "hp_current_label",     "depends_on_any": ["HeatPump-current-L1-data", "HeatPump-current-L2-data", "HeatPump-current-L3-data"]},
    "HeatPump-power-total-label": {"input_type": "label", "device": "heat_pump", "label_key": "hp_power_total_label", "depends_on": "HeatPump-power-total-data"},

    "HeatPump-current-L1-data":  {"input_type": "entity", "device": "heat_pump", "label_key": "hp_current_l1",  "prefix": "", "device_class": "current"},
    "HeatPump-current-L2-data":  {"input_type": "entity", "device": "heat_pump", "label_key": "hp_current_l2",  "prefix": "", "device_class": "current"},
    "HeatPump-current-L3-data":  {"input_type": "entity", "device": "heat_pump", "label_key": "hp_current_l3",  "prefix": "", "device_class": "current"},
    "HeatPump-power-L1-data":    {"input_type": "entity", "device": "heat_pump", "label_key": "hp_power_l1",    "prefix": "", "device_class": "power"},
    "HeatPump-power-L2-data":    {"input_type": "entity", "device": "heat_pump", "label_key": "hp_power_l2",    "prefix": "", "device_class": "power"},
    "HeatPump-power-L3-data":    {"input_type": "entity", "device": "heat_pump", "label_key": "hp_power_l3",    "prefix": "", "device_class": "power"},
    "HeatPump-power-total-data": {"input_type": "entity", "device": "heat_pump", "label_key": "hp_power_total", "prefix": "", "device_class": "power"},

    # --- Animacja wentylatorów ---
    "heat_pump_fan_enabled": {"input_type": "boolean", "device": "heat_pump", "label_key": "heat_pump_fan_enabled", "default": False},
    "HeatPump-fan1-speed-data": {"input_type": "entity", "device": "heat_pump", "label_key": "hp_fan1_speed", "prefix": "", "device_class": None},
    "HeatPump-fan2-speed-data": {"input_type": "entity", "device": "heat_pump", "label_key": "hp_fan2_speed", "prefix": "", "device_class": None},

    # ============================================================
    # ROZDZIELNICA 1 (gospodarcza)
    # ============================================================
    "subboard_1_name_visible":            {"input_type": "boolean", "device": "subboard_1", "label_key": "subboard_1_name_visible",            "default": True, "hides": ["AC_SubBoard1_label"]},
    "subboard_1_voltage_labels_visible":  {"input_type": "boolean", "device": "subboard_1", "label_key": "subboard_1_voltage_labels_visible",  "default": True, "hides": ["AC_subboard1_Voltage_label"]},
    "subboard_1_current_labels_visible":  {"input_type": "boolean", "device": "subboard_1", "label_key": "subboard_1_current_labels_visible",  "default": True, "hides": ["AC_subboard1_Current-label"]},
    "subboard_1_power_label_visible":     {"input_type": "boolean", "device": "subboard_1", "label_key": "subboard_1_power_label_visible",     "default": True, "hides": ["AC_subboard1_Power_Total_label"]},
    "subboard_1_energy_label_visible":    {"input_type": "boolean", "device": "subboard_1", "label_key": "subboard_1_energy_label_visible",    "default": True, "hides": ["AC_subboard1_Energy_label"]},

    "AC_SubBoard1_label":             {"input_type": "text_with_default",   "device": "subboard_1", "label_key": "sub1_name_label",     "default": "Gospodarczy",},    
    "AC_subboard1_Voltage_label":     {"input_type": "text_with_default",   "device": "subboard_1", "label_key": "sub1_voltage_label",  "default": "Napiecie",},
    "AC_subboard1_Current-label":     {"input_type": "text_with_default",   "device": "subboard_1", "label_key": "sub1_current_label",  "default": "Prąd",},
    
    "AC_subboard1_Power_Total_label": {"input_type": "label", "device": "subboard_1", "label_key": "sub1_power_label",   "depends_on": "AC_subboard1_Power_Total_data"},
    "AC_subboard1_Energy_label":      {"input_type": "label", "device": "subboard_1", "label_key": "sub1_energy_label",  "depends_on": "AC_subboard1_Energy_Produced-data"},

    "AC_subboard1_VAC_L1":               {"input_type": "entity", "device": "subboard_1", "label_key": "sub1_v_l1",         "prefix": "", "device_class": "voltage"},
    "AC_subboard1_VAC_L2":               {"input_type": "entity", "device": "subboard_1", "label_key": "sub1_v_l2",         "prefix": "", "device_class": "voltage"},
    "AC_subboard1_VAC_L3":               {"input_type": "entity", "device": "subboard_1", "label_key": "sub1_v_l3",         "prefix": "", "device_class": "voltage"},
    "AC_subboard1_Curr_L1":              {"input_type": "entity", "device": "subboard_1", "label_key": "sub1_i_l1",         "prefix": "", "device_class": "current"},
    "AC_subboard1_Curr_L2":              {"input_type": "entity", "device": "subboard_1", "label_key": "sub1_i_l2",         "prefix": "", "device_class": "current"},
    "AC_subboard1_Curr_L3":              {"input_type": "entity", "device": "subboard_1", "label_key": "sub1_i_l3",         "prefix": "", "device_class": "current"},
    "AC_subboard1_Power_Total_data":     {"input_type": "entity", "device": "subboard_1", "label_key": "sub1_power",        "prefix": "", "device_class": "power"},
    "AC_subboard1_Energy_Produced-data": {"input_type": "entity", "device": "subboard_1", "label_key": "sub1_energy_today", "prefix": "", "device_class": "energy"},

    # ============================================================
    # ROZDZIELNICA 2 (kotłownia)
    # ============================================================
    "subboard_2_name_visible":               {"input_type": "boolean", "device": "subboard_2", "label_key": "subboard_2_name_visible",               "default": True, "hides": ["AC_SubBoard2_label"]},
    "subboard_2_power_supply_label_visible": {"input_type": "boolean", "device": "subboard_2", "label_key": "subboard_2_power_supply_label_visible", "default": True, "hides": ["AC_SubBoard2_power_supply-label"]},
    "subboard_2_battery_label_visible":      {"input_type": "boolean", "device": "subboard_2", "label_key": "subboard_2_battery_label_visible",      "default": True, "hides": ["AC_SubBoard2_battery_SOC-label"]},

    "AC_SubBoard2_label": {
        "input_type": "text_with_default",
        "device": "subboard_2",
        "label_key": "boiler_name_label",
        "default": "Kotłownia",
    },
    "AC_SubBoard2_power_supply-label": {"input_type": "label", "device": "subboard_2", "label_key": "boiler_power_supply_label"},
    "AC_SubBoard2_battery_SOC-label":  {"input_type": "label", "device": "subboard_2", "label_key": "boiler_battery_soc_label", "depends_on": "AC_SubBoard2_battery_SOC-data"},

    "AC_SubBoard2_power_supply":        {"input_type": "text", "device": "subboard_2", "label_key": "boiler_power_supply"},
    "AC_SubBoard2_power_supply-grid":   {"input_type": "text", "device": "subboard_2", "label_key": "boiler_grid"},
    "AC_SubBoard2_power_supply-backup": {"input_type": "text", "device": "subboard_2", "label_key": "boiler_backup"},

    "AC_SubBoard2_battery_SOC-data": {"input_type": "entity", "device": "subboard_2", "label_key": "boiler_battery_soc", "prefix": "", "device_class": "battery"},

    # ============================================================
    # DOM
    # ============================================================
    "home_phase_labels_visible":   {"input_type": "boolean", "device": "home", "label_key": "home_phase_labels_visible",   "default": True, "hides": ["Phase-L1-label", "Phase-L2-label", "Phase-L3-label"]},
    "home_current_labels_visible": {"input_type": "boolean", "device": "home", "label_key": "home_current_labels_visible", "default": True, "hides": ["home-current-l1-label", "home-current-l2-label", "home-current-l3-label"]},
    "home_power_labels_visible":   {"input_type": "boolean", "device": "home", "label_key": "home_power_labels_visible",   "default": True, "hides": ["home-power-l1-label", "home-power-l2-label", "home-power-l3-label", "total-power-label"]},

    "Phase-L1-label": {"input_type": "label", "device": "home", "label_key": "phase_l1", "always_show": True},
    "Phase-L2-label": {"input_type": "label", "device": "home", "label_key": "phase_l2", "always_show": True},
    "Phase-L3-label": {"input_type": "label", "device": "home", "label_key": "phase_l3", "always_show": True},

    "home-current-l1-label": {"input_type": "label", "device": "home", "label_key": "home_current_l1_label", "depends_on": "home-current-l1-data"},
    "home-current-l2-label": {"input_type": "label", "device": "home", "label_key": "home_current_l2_label", "depends_on": "home-current-l2-data"},
    "home-current-l3-label": {"input_type": "label", "device": "home", "label_key": "home_current_l3_label", "depends_on": "home-current-l3-data"},
    "home-power-l1-label":   {"input_type": "label", "device": "home", "label_key": "home_power_l1_label",   "depends_on": "home-power-l1-data"},
    "home-power-l2-label":   {"input_type": "label", "device": "home", "label_key": "home_power_l2_label",   "depends_on": "home-power-l2-data"},
    "home-power-l3-label":   {"input_type": "label", "device": "home", "label_key": "home_power_l3_label",   "depends_on": "home-power-l3-data"},
    "total-power-label":     {"input_type": "label", "device": "home", "label_key": "home_power_total_label", "depends_on": "total-power-data"},

    "home-current-l1-data": {"input_type": "entity", "device": "home", "label_key": "home_current_l1", "prefix": "", "device_class": "current"},
    "home-current-l2-data": {"input_type": "entity", "device": "home", "label_key": "home_current_l2", "prefix": "", "device_class": "current"},
    "home-current-l3-data": {"input_type": "entity", "device": "home", "label_key": "home_current_l3", "prefix": "", "device_class": "current"},
    "home-power-l1-data":   {"input_type": "entity", "device": "home", "label_key": "home_power_l1",   "prefix": "", "device_class": "power"},
    "home-power-l2-data":   {"input_type": "entity", "device": "home", "label_key": "home_power_l2",   "prefix": "", "device_class": "power"},
    "home-power-l3-data":   {"input_type": "entity", "device": "home", "label_key": "home_power_l3",   "prefix": "", "device_class": "power"},
    "total-power-data":     {"input_type": "entity", "device": "home", "label_key": "home_power_total","prefix": "", "device_class": "power"},

    # ============================================================
    # SIEĆ / OSD (z full-backup)
    # ============================================================
    "grid_phase_labels_visible":   {"input_type": "boolean", "device": "grid", "label_key": "grid_phase_labels_visible",   "default": True, "hides": ["GRID_Phase_label_L1", "GRID_Phase_label_L2", "GRID_Phase_label_L3", "GRID_Phase_label_N"]},
    "grid_voltage_labels_visible": {"input_type": "boolean", "device": "grid", "label_key": "grid_voltage_labels_visible", "default": True, "hides": ["grid-voltage-l1-label", "grid-voltage-l2-label", "grid-voltage-l3-label"]},
    "grid_current_labels_visible": {"input_type": "boolean", "device": "grid", "label_key": "grid_current_labels_visible", "default": True, "hides": ["grid-current-l1-label", "grid-current-l2-label", "grid-current-l3-label"]},
    "grid_meter_labels_visible":   {"input_type": "boolean", "device": "grid", "label_key": "grid_meter_labels_visible",   "default": True, "hides": ["meter-power-label", "meter-power-produced_day-label"]},

    "GRID_Phase_label_L1": {"input_type": "label", "device": "grid", "label_key": "phase_l1", "always_show": True},
    "GRID_Phase_label_L2": {"input_type": "label", "device": "grid", "label_key": "phase_l2", "always_show": True},
    "GRID_Phase_label_L3": {"input_type": "label", "device": "grid", "label_key": "phase_l3", "always_show": True},
    "GRID_Phase_label_N":  {"input_type": "label", "device": "grid", "label_key": "phase_n",  "always_show": True},

    "grid-voltage-l1-label": {"input_type": "label", "device": "grid", "label_key": "grid_voltage_label", "depends_on": "grid-voltage-l1-data"},
    "grid-voltage-l2-label": {"input_type": "label", "device": "grid", "label_key": "grid_voltage_label", "depends_on": "grid-voltage-l2-data"},
    "grid-voltage-l3-label": {"input_type": "label", "device": "grid", "label_key": "grid_voltage_label", "depends_on": "grid-voltage-l3-data"},

    "grid-current-l1-label": {"input_type": "label", "device": "grid", "label_key": "grid_current_label", "depends_on": "grid-current-l1-data"},
    "grid-current-l2-label": {"input_type": "label", "device": "grid", "label_key": "grid_current_label", "depends_on": "grid-current-l2-data"},
    "grid-current-l3-label": {"input_type": "label", "device": "grid", "label_key": "grid_current_label", "depends_on": "grid-current-l3-data"},

    "meter-power-label":              {"input_type": "label", "device": "grid", "label_key": "meter_power_label",  "depends_on": "meter-power-data"},
    "meter-power-produced_day-label": {"input_type": "label", "device": "grid", "label_key": "meter_energy_label", "depends_on": "meter-power-produced_day-data"},

    "grid-voltage-l1-data": {"input_type": "entity", "device": "grid", "label_key": "grid_v_l1", "prefix": "", "device_class": "voltage"},
    "grid-voltage-l2-data": {"input_type": "entity", "device": "grid", "label_key": "grid_v_l2", "prefix": "", "device_class": "voltage"},
    "grid-voltage-l3-data": {"input_type": "entity", "device": "grid", "label_key": "grid_v_l3", "prefix": "", "device_class": "voltage"},
    "grid-current-l1-data": {"input_type": "entity", "device": "grid", "label_key": "grid_i_l1", "prefix": "", "device_class": "current"},
    "grid-current-l2-data": {"input_type": "entity", "device": "grid", "label_key": "grid_i_l2", "prefix": "", "device_class": "current"},
    "grid-current-l3-data": {"input_type": "entity", "device": "grid", "label_key": "grid_i_l3", "prefix": "", "device_class": "current"},
    "meter-power-data":              {"input_type": "entity", "device": "grid", "label_key": "meter_power",  "prefix": "", "device_class": "power"},
    "meter-power-produced_day-data": {"input_type": "entity", "device": "grid", "label_key": "meter_energy", "prefix": "", "device_class": "energy"},
}