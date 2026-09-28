import os
import json

telemetry_dir = os.path.abspath("sample_telemetry")
os.makedirs(telemetry_dir, exist_ok=True)

# Remove all existing telemetry_*.json files
for f in os.listdir(telemetry_dir):
    if f.startswith("telemetry_") and f.endswith(".json"):
        os.remove(os.path.join(telemetry_dir, f))

door_samples = [
    # --- GROUP A: First 10 Sample Telemetries (Single-Stage 100% Pass on Rank 1) ---
    {
        "filename": "telemetry_01_door_sill_physical_obstruction.json",
        "title": "[F14 / #01] Landing Sill Physical Obstruction & High Motor Current",
        "fault_code": "F14",
        "verification_stage": "SINGLE_STAGE",
        "subsystem": "door",
        "elevator_id": "KONE-DOOR-101",
        "model": "KONE MonoSpace 500",
        "operating_state": "DOOR_CLOSE",
        "installation_age_years": 2.1,
        "alarms": [
            {"alarm_code": "door_close_timeout", "alarm_type": "door_close_timeout", "severity": "critical", "subsystem": "door", "timestamp": "2026-09-24T10:00:00.000Z", "state": "ACTIVE"},
            {"alarm_code": "door_motor_overcurrent", "alarm_type": "door_motor_overcurrent", "severity": "warning", "subsystem": "door", "timestamp": "2026-09-24T10:00:01.500Z", "state": "ACTIVE"}
        ],
        "telemetry": [
            {"signal_name": "door_motor_current", "value": 3.4, "unit": "A", "quality": "good", "timestamp": "2026-09-24T10:00:00.000Z", "baseline_value": 1.5, "deviation_pct": 126.7},
            {"signal_name": "door_cycle_time_ms", "value": 5400.0, "unit": "ms", "quality": "good", "timestamp": "2026-09-24T10:00:00.000Z", "baseline_value": 2800.0, "deviation_pct": 92.9},
            {"signal_name": "reopen_location_consistent", "value": "TRUE", "unit": "state", "quality": "good", "timestamp": "2026-09-24T10:00:00.000Z", "baseline_value": "FALSE", "deviation_pct": 0.0}
        ],
        "maintenance_history": [],
        "technician_free_text": "Door hits a hard stop at consistent 120mm position before fully closed. Physical object lodged in sill groove."
    },
    {
        "filename": "telemetry_02_door_photoeye_dirt_attenuation.json",
        "title": "[F74 / #02] Single-Beam Optical Photo-eye Lens Dust Clouding",
        "fault_code": "F74",
        "verification_stage": "SINGLE_STAGE",
        "subsystem": "door",
        "elevator_id": "KONE-DOOR-102",
        "model": "KONE MiniSpace",
        "operating_state": "DOOR_CLOSE",
        "installation_age_years": 3.0,
        "alarms": [
            {"alarm_code": "door_photoeye_obstruction", "alarm_type": "door_photoeye_obstruction", "severity": "warning", "subsystem": "door", "timestamp": "2026-09-24T10:05:00.000Z", "state": "ACTIVE"}
        ],
        "telemetry": [
            {"signal_name": "door_cycle_time_ms", "value": 4200.0, "unit": "ms", "quality": "good", "timestamp": "2026-09-24T10:05:00.000Z", "baseline_value": 2800.0, "deviation_pct": 50.0},
            {"signal_name": "photoeye_state_erratic", "value": "TRUE", "unit": "state", "quality": "good", "timestamp": "2026-09-24T10:05:00.000Z", "baseline_value": "FALSE", "deviation_pct": 0.0},
            {"signal_name": "reopen_location_consistent", "value": "FALSE", "unit": "state", "quality": "good", "timestamp": "2026-09-24T10:05:00.000Z", "baseline_value": "FALSE", "deviation_pct": 0.0}
        ],
        "maintenance_history": [],
        "technician_free_text": "Door intermittently reverses at varying random travel distances. Optical receiver shows heavy dust layer on lens."
    },
    {
        "filename": "telemetry_03_door_drive_belt_tension_slip.json",
        "title": "[F44 / #03] Door Operator Toothed Drive Belt Stretch & Speed Variation",
        "fault_code": "F44",
        "verification_stage": "SINGLE_STAGE",
        "subsystem": "door",
        "elevator_id": "KONE-DOOR-103",
        "model": "KONE MonoSpace 500",
        "operating_state": "DOOR_CLOSE",
        "installation_age_years": 4.5,
        "alarms": [
            {"alarm_code": "door_close_timeout", "alarm_type": "door_close_timeout", "severity": "warning", "subsystem": "door", "timestamp": "2026-09-24T10:10:00.000Z", "state": "ACTIVE"}
        ],
        "telemetry": [
            {"signal_name": "door_speed_variation", "value": 0.22, "unit": "m/s", "quality": "good", "timestamp": "2026-09-24T10:10:00.000Z", "baseline_value": 0.05, "deviation_pct": 340.0},
            {"signal_name": "door_cycle_time_ms", "value": 3900.0, "unit": "ms", "quality": "good", "timestamp": "2026-09-24T10:10:00.000Z", "baseline_value": 2800.0, "deviation_pct": 39.3}
        ],
        "maintenance_history": [],
        "technician_free_text": "Drive belt sagging over 16mm under nominal finger pressure. Motor pulley slips during peak door acceleration."
    },
    {
        "filename": "telemetry_04_door_lock_contact_oxidation.json",
        "title": "[F14 / #04] Landing Door Interlock Electrical Contact Oxidation & Loop Break",
        "fault_code": "F14",
        "verification_stage": "SINGLE_STAGE",
        "subsystem": "door",
        "elevator_id": "KONE-DOOR-104",
        "model": "KONE MonoSpace 500",
        "operating_state": "DOOR_CLOSE",
        "installation_age_years": 5.0,
        "alarms": [
            {"alarm_code": "door_lock_circuit_open", "alarm_type": "door_lock_circuit_open", "severity": "critical", "subsystem": "door", "timestamp": "2026-09-24T10:15:00.000Z", "state": "ACTIVE"}
        ],
        "telemetry": [
            {"signal_name": "door_lock_confirmed", "value": "FALSE", "unit": "state", "quality": "good", "timestamp": "2026-09-24T10:15:00.000Z", "baseline_value": "TRUE", "deviation_pct": 0.0},
            {"signal_name": "door_fully_closed", "value": "TRUE", "unit": "state", "quality": "good", "timestamp": "2026-09-24T10:15:00.000Z", "baseline_value": "TRUE", "deviation_pct": 0.0}
        ],
        "maintenance_history": [],
        "technician_free_text": "Door physically reaches full close position but safety circuit remains open. Floor 3 interlock contact pads severely pitted."
    },
    {
        "filename": "telemetry_05_door_open_limit_switch_jam.json",
        "title": "[F24 / #05] Door Full-Open Limit Switch (DOL) Open-Circuit Fault",
        "fault_code": "F24",
        "verification_stage": "SINGLE_STAGE",
        "subsystem": "door",
        "elevator_id": "KONE-DOOR-105",
        "model": "KONE MonoSpace 500",
        "operating_state": "DOOR_OPEN",
        "installation_age_years": 2.8,
        "alarms": [
            {"alarm_code": "door_open_timeout", "alarm_type": "door_open_timeout", "severity": "warning", "subsystem": "door", "timestamp": "2026-09-24T10:20:00.000Z", "state": "ACTIVE"}
        ],
        "telemetry": [
            {"signal_name": "door_cycle_time_ms", "value": 4800.0, "unit": "ms", "quality": "good", "timestamp": "2026-09-24T10:20:00.000Z", "baseline_value": 2800.0, "deviation_pct": 71.4},
            {"signal_name": "door_motor_current", "value": 2.2, "unit": "A", "quality": "good", "timestamp": "2026-09-24T10:20:00.000Z", "baseline_value": 1.5, "deviation_pct": 46.7}
        ],
        "maintenance_history": [],
        "technician_free_text": "Door opens fully to rubber stop bumper but controller fails to receive DOL signal. Limit microswitch plunger stuck."
    },
    {
        "filename": "telemetry_06_door_close_limit_cam_misalignment.json",
        "title": "[F34 / #06] Door Full-Close Limit Sensor (DCL) Cam Jam & Timeout",
        "fault_code": "F34",
        "verification_stage": "SINGLE_STAGE",
        "subsystem": "door",
        "elevator_id": "KONE-DOOR-106",
        "model": "KONE MonoSpace 500",
        "operating_state": "DOOR_CLOSE",
        "installation_age_years": 3.4,
        "alarms": [
            {"alarm_code": "door_close_timeout", "alarm_type": "door_close_timeout", "severity": "warning", "subsystem": "door", "timestamp": "2026-09-24T10:25:00.000Z", "state": "ACTIVE"}
        ],
        "telemetry": [
            {"signal_name": "door_cycle_time_ms", "value": 4600.0, "unit": "ms", "quality": "good", "timestamp": "2026-09-24T10:25:00.000Z", "baseline_value": 2800.0, "deviation_pct": 64.3},
            {"signal_name": "door_motor_current", "value": 2.1, "unit": "A", "quality": "good", "timestamp": "2026-09-24T10:25:00.000Z", "baseline_value": 1.5, "deviation_pct": 40.0}
        ],
        "maintenance_history": [],
        "technician_free_text": "DCL cam mounting bracket loosened, causing late actuation after mechanical interlock contact engagement."
    },
    {
        "filename": "telemetry_07_door_operator_motor_thermal_saturation.json",
        "title": "[F54 / #07] Door Operator PM Motor Torque Loss & Current Rise",
        "fault_code": "F54",
        "verification_stage": "SINGLE_STAGE",
        "subsystem": "door",
        "elevator_id": "KONE-DOOR-107",
        "model": "KONE MonoSpace 500",
        "operating_state": "DOOR_CLOSE",
        "installation_age_years": 5.2,
        "alarms": [
            {"alarm_code": "door_close_timeout", "alarm_type": "door_close_timeout", "severity": "critical", "subsystem": "door", "timestamp": "2026-09-24T10:30:00.000Z", "state": "ACTIVE"},
            {"alarm_code": "door_motor_overcurrent", "alarm_type": "door_motor_overcurrent", "severity": "warning", "subsystem": "door", "timestamp": "2026-09-24T10:30:02.000Z", "state": "ACTIVE"}
        ],
        "telemetry": [
            {"signal_name": "door_motor_current", "value": 3.1, "unit": "A", "quality": "good", "timestamp": "2026-09-24T10:30:00.000Z", "baseline_value": 1.5, "deviation_pct": 106.7},
            {"signal_name": "door_cycle_time_ms", "value": 5100.0, "unit": "ms", "quality": "good", "timestamp": "2026-09-24T10:30:00.000Z", "baseline_value": 2800.0, "deviation_pct": 82.1}
        ],
        "maintenance_history": [],
        "technician_free_text": "Operator motor casing hot to touch (68°C). Stator winding impedance degraded under prolonged peak duty."
    },
    {
        "filename": "telemetry_08_door_hanger_roller_bearing_wear.json",
        "title": "[F54 / #08] Door Hanger Roller Bearing Flat Spot Mechanical Wear",
        "fault_code": "F54",
        "verification_stage": "SINGLE_STAGE",
        "subsystem": "door",
        "elevator_id": "KONE-DOOR-108",
        "model": "KONE MonoSpace 500",
        "operating_state": "DOOR_CLOSE",
        "installation_age_years": 4.1,
        "alarms": [
            {"alarm_code": "door_close_timeout", "alarm_type": "door_close_timeout", "severity": "warning", "subsystem": "door", "timestamp": "2026-09-24T10:35:00.000Z", "state": "ACTIVE"}
        ],
        "telemetry": [
            {"signal_name": "door_motor_current", "value": 2.8, "unit": "A", "quality": "good", "timestamp": "2026-09-24T10:35:00.000Z", "baseline_value": 1.5, "deviation_pct": 86.7},
            {"signal_name": "door_cycle_time_ms", "value": 4600.0, "unit": "ms", "quality": "good", "timestamp": "2026-09-24T10:35:00.000Z", "baseline_value": 2800.0, "deviation_pct": 64.3}
        ],
        "maintenance_history": [],
        "technician_free_text": "Audible rhythmic clicking sound during door closing. Top left hanger roller bearing has 1.2mm flat spot."
    },
    {
        "filename": "telemetry_09_door_reopen_limit_bounce.json",
        "title": "[F74 / #09] 3D Light Curtain Multi-Beam Optical Degradation & False Reopenings",
        "fault_code": "F74",
        "verification_stage": "SINGLE_STAGE",
        "subsystem": "door",
        "elevator_id": "KONE-DOOR-109",
        "model": "KONE MiniSpace",
        "operating_state": "DOOR_CLOSE",
        "installation_age_years": 3.7,
        "alarms": [
            {"alarm_code": "door_photoeye_obstruction", "alarm_type": "door_photoeye_obstruction", "severity": "warning", "subsystem": "door", "timestamp": "2026-09-24T10:40:00.000Z", "state": "ACTIVE"}
        ],
        "telemetry": [
            {"signal_name": "door_cycle_time_ms", "value": 4500.0, "unit": "ms", "quality": "good", "timestamp": "2026-09-24T10:40:00.000Z", "baseline_value": 2800.0, "deviation_pct": 60.7},
            {"signal_name": "photoeye_state_erratic", "value": "TRUE", "unit": "state", "quality": "good", "timestamp": "2026-09-24T10:40:00.000Z", "baseline_value": "FALSE", "deviation_pct": 0.0},
            {"signal_name": "reopen_location_consistent", "value": "FALSE", "unit": "state", "quality": "good", "timestamp": "2026-09-24T10:40:00.000Z", "baseline_value": "FALSE", "deviation_pct": 0.0}
        ],
        "maintenance_history": [],
        "technician_free_text": "Curtain LED indicates channel 14-18 signal attenuation. Sunlight reflection triggering intermittent reopening cycles."
    },
    {
        "filename": "telemetry_10_door_safety_edge_switch_trip.json",
        "title": "[F14 / #10] Mechanical Safety Edge Shoe Jam & Motor Current Spike",
        "fault_code": "F14",
        "verification_stage": "SINGLE_STAGE",
        "subsystem": "door",
        "elevator_id": "KONE-DOOR-110",
        "model": "KONE MonoSpace 500",
        "operating_state": "DOOR_CLOSE",
        "installation_age_years": 3.1,
        "alarms": [
            {"alarm_code": "door_close_timeout", "alarm_type": "door_close_timeout", "severity": "critical", "subsystem": "door", "timestamp": "2026-09-24T10:45:00.000Z", "state": "ACTIVE"}
        ],
        "telemetry": [
            {"signal_name": "door_motor_current", "value": 3.3, "unit": "A", "quality": "good", "timestamp": "2026-09-24T10:45:00.000Z", "baseline_value": 1.5, "deviation_pct": 120.0},
            {"signal_name": "door_cycle_time_ms", "value": 5300.0, "unit": "ms", "quality": "good", "timestamp": "2026-09-24T10:45:00.000Z", "baseline_value": 2800.0, "deviation_pct": 89.3},
            {"signal_name": "reopen_location_consistent", "value": "TRUE", "unit": "state", "quality": "good", "timestamp": "2026-09-24T10:45:00.000Z", "baseline_value": "FALSE", "deviation_pct": 0.0}
        ],
        "maintenance_history": [],
        "technician_free_text": "Leading mechanical safety shoe binding against car door return frame. Current spike triggers protective reverse."
    },

    # --- GROUP B: Next 10 Sample Telemetries (Two-Stage Verification: Stage 1 + Stage 2 Secondary Root Cause Resolution) ---
    {
        "filename": "telemetry_11_door_repeat_roller_misdiagnosis_track_misalignment.json",
        "title": "[F64 / #11] Door Track Misalignment / Geometric Distortion (Resolving Repeat Roller Swaps)",
        "fault_code": "F64",
        "verification_stage": "TWO_STAGE",
        "subsystem": "door",
        "elevator_id": "KONE-DOOR-201",
        "model": "KONE MonoSpace 500",
        "operating_state": "DOOR_CLOSE",
        "installation_age_years": 4.2,
        "alarms": [
            {"alarm_code": "door_close_timeout", "alarm_type": "door_close_timeout", "severity": "critical", "subsystem": "door", "timestamp": "2026-09-24T11:00:00.000Z", "state": "ACTIVE"},
            {"alarm_code": "door_motor_overcurrent", "alarm_type": "door_motor_overcurrent", "severity": "warning", "subsystem": "door", "timestamp": "2026-09-24T11:00:02.000Z", "state": "ACTIVE"}
        ],
        "telemetry": [
            {"signal_name": "door_cycle_time_ms", "value": 4900.0, "unit": "ms", "quality": "good", "timestamp": "2026-09-24T11:00:00.000Z", "baseline_value": 2800.0, "deviation_pct": 75.0},
            {"signal_name": "door_motor_current", "value": 2.7, "unit": "A", "quality": "good", "timestamp": "2026-09-24T11:00:00.000Z", "baseline_value": 1.5, "deviation_pct": 80.0},
            {"signal_name": "vibration_rms", "value": 0.22, "unit": "m/s2", "quality": "good", "timestamp": "2026-09-24T11:00:00.000Z", "baseline_value": 0.08, "deviation_pct": 175.0}
        ],
        "maintenance_history": [
            {"date": "2026-06-10T10:00:00Z", "component": "Door Roller", "action": "Replaced worn hanger rollers", "technician_notes": "Replaced top rollers after door timeout fault", "part_replaced": True},
            {"date": "2026-08-15T14:30:00Z", "component": "Door Roller", "action": "Replaced hanger rollers again", "technician_notes": "Door sticking again, installed new rollers", "part_replaced": True}
        ],
        "technician_free_text": "Previous technicians replaced door rollers twice in past 3 months. Door binding persists due to underlying header track geometric distortion."
    },
    {
        "filename": "telemetry_12_door_curtain_drift_and_lock_pitting.json",
        "title": "[F74 / #12] Optical Sensor Drift with Latent Landing Interlock Oxidation",
        "fault_code": "F74",
        "verification_stage": "TWO_STAGE",
        "subsystem": "door",
        "elevator_id": "KONE-DOOR-202",
        "model": "KONE MonoSpace 500",
        "operating_state": "DOOR_CLOSE",
        "installation_age_years": 4.6,
        "alarms": [
            {"alarm_code": "door_close_timeout", "alarm_type": "door_close_timeout", "severity": "critical", "subsystem": "door", "timestamp": "2026-09-24T11:05:00.000Z", "state": "ACTIVE"},
            {"alarm_code": "door_photoeye_obstruction", "alarm_type": "door_photoeye_obstruction", "severity": "warning", "subsystem": "door", "timestamp": "2026-09-24T11:05:01.000Z", "state": "ACTIVE"}
        ],
        "telemetry": [
            {"signal_name": "door_cycle_time_ms", "value": 4700.0, "unit": "ms", "quality": "good", "timestamp": "2026-09-24T11:05:00.000Z", "baseline_value": 2800.0, "deviation_pct": 67.9},
            {"signal_name": "photoeye_state_erratic", "value": "TRUE", "unit": "state", "quality": "good", "timestamp": "2026-09-24T11:05:00.000Z", "baseline_value": "FALSE", "deviation_pct": 0.0},
            {"signal_name": "door_lock_confirmed", "value": "FALSE", "unit": "state", "quality": "good", "timestamp": "2026-09-24T11:05:00.000Z", "baseline_value": "TRUE", "deviation_pct": 0.0}
        ],
        "maintenance_history": [],
        "technician_free_text": "Primary symptom is optical curtain false triggers. Secondary inspection reveals intermittent Floor 2 interlock contact drop."
    },
    {
        "filename": "telemetry_13_door_operator_belt_slip_and_motor_torque_loss.json",
        "title": "[F44 / #13] Drive Belt Slack Slip with Secondary Operator Motor Torque Loss",
        "fault_code": "F44",
        "verification_stage": "TWO_STAGE",
        "subsystem": "door",
        "elevator_id": "KONE-DOOR-203",
        "model": "KONE MonoSpace 500",
        "operating_state": "DOOR_CLOSE",
        "installation_age_years": 5.1,
        "alarms": [
            {"alarm_code": "door_close_timeout", "alarm_type": "door_close_timeout", "severity": "critical", "subsystem": "door", "timestamp": "2026-09-24T11:10:00.000Z", "state": "ACTIVE"}
        ],
        "telemetry": [
            {"signal_name": "door_speed_variation", "value": 0.20, "unit": "m/s", "quality": "good", "timestamp": "2026-09-24T11:10:00.000Z", "baseline_value": 0.05, "deviation_pct": 300.0},
            {"signal_name": "door_motor_current", "value": 2.9, "unit": "A", "quality": "good", "timestamp": "2026-09-24T11:10:00.000Z", "baseline_value": 1.5, "deviation_pct": 93.3},
            {"signal_name": "door_cycle_time_ms", "value": 5000.0, "unit": "ms", "quality": "good", "timestamp": "2026-09-24T11:10:00.000Z", "baseline_value": 2800.0, "deviation_pct": 78.6}
        ],
        "maintenance_history": [],
        "technician_free_text": "Belt teeth worn, slipping on start. Operator motor winding resistance tests 20% higher than OEM spec."
    },
    {
        "filename": "telemetry_14_door_track_distortion_and_hanger_roller_flatspots.json",
        "title": "[F64 / #14] Header Track Binding accompanied by Roller Flat Spot Wear",
        "fault_code": "F64",
        "verification_stage": "TWO_STAGE",
        "subsystem": "door",
        "elevator_id": "KONE-DOOR-204",
        "model": "KONE MonoSpace 500",
        "operating_state": "DOOR_CLOSE",
        "installation_age_years": 4.8,
        "alarms": [
            {"alarm_code": "door_close_timeout", "alarm_type": "door_close_timeout", "severity": "critical", "subsystem": "door", "timestamp": "2026-09-24T11:15:00.000Z", "state": "ACTIVE"},
            {"alarm_code": "door_motor_overcurrent", "alarm_type": "door_motor_overcurrent", "severity": "warning", "subsystem": "door", "timestamp": "2026-09-24T11:15:02.000Z", "state": "ACTIVE"}
        ],
        "telemetry": [
            {"signal_name": "door_motor_current", "value": 3.0, "unit": "A", "quality": "good", "timestamp": "2026-09-24T11:15:00.000Z", "baseline_value": 1.5, "deviation_pct": 100.0},
            {"signal_name": "vibration_rms", "value": 0.20, "unit": "m/s2", "quality": "good", "timestamp": "2026-09-24T11:15:00.000Z", "baseline_value": 0.08, "deviation_pct": 150.0},
            {"signal_name": "door_cycle_time_ms", "value": 5200.0, "unit": "ms", "quality": "good", "timestamp": "2026-09-24T11:15:00.000Z", "baseline_value": 2800.0, "deviation_pct": 85.7}
        ],
        "maintenance_history": [],
        "technician_free_text": "Header rail bowed horizontally by 3.5mm. Hanger rollers have developed secondary flat spots from running along distorted track."
    },
    {
        "filename": "telemetry_15_door_sill_gap_wear_and_interlock_drop.json",
        "title": "[F14 / #15] Landing Sill Foreign Debris with Interlock Switch Bounce",
        "fault_code": "F14",
        "verification_stage": "TWO_STAGE",
        "subsystem": "door",
        "elevator_id": "KONE-DOOR-205",
        "model": "KONE MonoSpace 500",
        "operating_state": "DOOR_CLOSE",
        "installation_age_years": 3.9,
        "alarms": [
            {"alarm_code": "door_close_timeout", "alarm_type": "door_close_timeout", "severity": "critical", "subsystem": "door", "timestamp": "2026-09-24T11:20:00.000Z", "state": "ACTIVE"},
            {"alarm_code": "door_lock_circuit_open", "alarm_type": "door_lock_circuit_open", "severity": "critical", "subsystem": "door", "timestamp": "2026-09-24T11:20:01.500Z", "state": "ACTIVE"}
        ],
        "telemetry": [
            {"signal_name": "door_motor_current", "value": 3.2, "unit": "A", "quality": "good", "timestamp": "2026-09-24T11:20:00.000Z", "baseline_value": 1.5, "deviation_pct": 113.3},
            {"signal_name": "reopen_location_consistent", "value": "TRUE", "unit": "state", "quality": "good", "timestamp": "2026-09-24T11:20:00.000Z", "baseline_value": "FALSE", "deviation_pct": 0.0},
            {"signal_name": "door_lock_confirmed", "value": "FALSE", "unit": "state", "quality": "good", "timestamp": "2026-09-24T11:20:00.000Z", "baseline_value": "TRUE", "deviation_pct": 0.0}
        ],
        "maintenance_history": [],
        "technician_free_text": "Debris lodged in sill prevents complete door seating; landing door interlock latch fails to drop into fully locked position."
    },
    {
        "filename": "telemetry_16_door_open_limit_and_cable_loom_pinch.json",
        "title": "[F24 / #16] Door Open Limit Sensor Stuck with Car Gate Harness Pinch",
        "fault_code": "F24",
        "verification_stage": "TWO_STAGE",
        "subsystem": "door",
        "elevator_id": "KONE-DOOR-206",
        "model": "KONE MonoSpace 500",
        "operating_state": "DOOR_OPEN",
        "installation_age_years": 4.3,
        "alarms": [
            {"alarm_code": "door_open_timeout", "alarm_type": "door_open_timeout", "severity": "warning", "subsystem": "door", "timestamp": "2026-09-24T11:25:00.000Z", "state": "ACTIVE"}
        ],
        "telemetry": [
            {"signal_name": "door_cycle_time_ms", "value": 4900.0, "unit": "ms", "quality": "good", "timestamp": "2026-09-24T11:25:00.000Z", "baseline_value": 2800.0, "deviation_pct": 75.0},
            {"signal_name": "door_motor_current", "value": 2.4, "unit": "A", "quality": "good", "timestamp": "2026-09-24T11:25:00.000Z", "baseline_value": 1.5, "deviation_pct": 60.0}
        ],
        "maintenance_history": [],
        "technician_free_text": "DOL switch circuit open. Visual inspection reveals flex cable pinched behind operator header bracket."
    },
    {
        "filename": "telemetry_17_door_photoeye_lens_and_receiver_sync_drift.json",
        "title": "[F74 / #17] Optical Safety Edge Dust with Multi-Beam Sync Timing Drift",
        "fault_code": "F74",
        "verification_stage": "TWO_STAGE",
        "subsystem": "door",
        "elevator_id": "KONE-DOOR-207",
        "model": "KONE MiniSpace",
        "operating_state": "DOOR_CLOSE",
        "installation_age_years": 3.8,
        "alarms": [
            {"alarm_code": "door_photoeye_obstruction", "alarm_type": "door_photoeye_obstruction", "severity": "warning", "subsystem": "door", "timestamp": "2026-09-24T11:30:00.000Z", "state": "ACTIVE"}
        ],
        "telemetry": [
            {"signal_name": "door_cycle_time_ms", "value": 4400.0, "unit": "ms", "quality": "good", "timestamp": "2026-09-24T11:30:00.000Z", "baseline_value": 2800.0, "deviation_pct": 57.1},
            {"signal_name": "photoeye_state_erratic", "value": "TRUE", "unit": "state", "quality": "good", "timestamp": "2026-09-24T11:30:00.000Z", "baseline_value": "FALSE", "deviation_pct": 0.0},
            {"signal_name": "reopen_location_consistent", "value": "FALSE", "unit": "state", "quality": "good", "timestamp": "2026-09-24T11:30:00.000Z", "baseline_value": "FALSE", "deviation_pct": 0.0}
        ],
        "maintenance_history": [],
        "technician_free_text": "Transmitter lens clouded. In addition, curtain sync controller shows clock drift under elevated hoistway temperatures."
    },
    {
        "filename": "telemetry_18_door_close_limit_cam_and_roller_eccentric_gap.json",
        "title": "[F34 / #18] DCL Limit Sensor Cam Binding with Roller Eccentric Gap Runout",
        "fault_code": "F34",
        "verification_stage": "TWO_STAGE",
        "subsystem": "door",
        "elevator_id": "KONE-DOOR-208",
        "model": "KONE MonoSpace 500",
        "operating_state": "DOOR_CLOSE",
        "installation_age_years": 4.7,
        "alarms": [
            {"alarm_code": "door_close_timeout", "alarm_type": "door_close_timeout", "severity": "warning", "subsystem": "door", "timestamp": "2026-09-24T11:35:00.000Z", "state": "ACTIVE"}
        ],
        "telemetry": [
            {"signal_name": "door_cycle_time_ms", "value": 4700.0, "unit": "ms", "quality": "good", "timestamp": "2026-09-24T11:35:00.000Z", "baseline_value": 2800.0, "deviation_pct": 67.9},
            {"signal_name": "door_motor_current", "value": 2.5, "unit": "A", "quality": "good", "timestamp": "2026-09-24T11:35:00.000Z", "baseline_value": 1.5, "deviation_pct": 66.7}
        ],
        "maintenance_history": [],
        "technician_free_text": "Close limit switch cam loose. Roller eccentric bushing has 0.45mm play exceeding 0.20mm OEM tolerance."
    },
    {
        "filename": "telemetry_19_door_motor_driver_inverter_and_belt_friction.json",
        "title": "[F54 / #19] Door Driver Board Current Sense Drift with Toothed Belt Friction",
        "fault_code": "F54",
        "verification_stage": "TWO_STAGE",
        "subsystem": "door",
        "elevator_id": "KONE-DOOR-209",
        "model": "KONE MonoSpace 500",
        "operating_state": "DOOR_CLOSE",
        "installation_age_years": 5.4,
        "alarms": [
            {"alarm_code": "door_close_timeout", "alarm_type": "door_close_timeout", "severity": "critical", "subsystem": "door", "timestamp": "2026-09-24T11:40:00.000Z", "state": "ACTIVE"},
            {"alarm_code": "door_motor_overcurrent", "alarm_type": "door_motor_overcurrent", "severity": "warning", "subsystem": "door", "timestamp": "2026-09-24T11:40:02.000Z", "state": "ACTIVE"}
        ],
        "telemetry": [
            {"signal_name": "door_motor_current", "value": 3.3, "unit": "A", "quality": "good", "timestamp": "2026-09-24T11:40:00.000Z", "baseline_value": 1.5, "deviation_pct": 120.0},
            {"signal_name": "door_speed_variation", "value": 0.16, "unit": "m/s", "quality": "good", "timestamp": "2026-09-24T11:40:00.000Z", "baseline_value": 0.05, "deviation_pct": 220.0},
            {"signal_name": "door_cycle_time_ms", "value": 5200.0, "unit": "ms", "quality": "good", "timestamp": "2026-09-24T11:40:00.000Z", "baseline_value": 2800.0, "deviation_pct": 85.7}
        ],
        "maintenance_history": [],
        "technician_free_text": "Operator driver board shunt resistor drifted hot; drive belt teeth worn causing intermittent torque hunting."
    },
    {
        "filename": "telemetry_20_door_interlock_hook_depth_and_sill_alignment.json",
        "title": "[F14 / #20] Landing Interlock Hook Depth Drop with Sill Guide Distortion",
        "fault_code": "F14",
        "verification_stage": "TWO_STAGE",
        "subsystem": "door",
        "elevator_id": "KONE-DOOR-210",
        "model": "KONE MonoSpace 500",
        "operating_state": "DOOR_CLOSE",
        "installation_age_years": 4.9,
        "alarms": [
            {"alarm_code": "door_lock_circuit_open", "alarm_type": "door_lock_circuit_open", "severity": "critical", "subsystem": "door", "timestamp": "2026-09-24T11:45:00.000Z", "state": "ACTIVE"},
            {"alarm_code": "door_close_timeout", "alarm_type": "door_close_timeout", "severity": "warning", "subsystem": "door", "timestamp": "2026-09-24T11:45:02.000Z", "state": "ACTIVE"}
        ],
        "telemetry": [
            {"signal_name": "door_lock_confirmed", "value": "FALSE", "unit": "state", "quality": "good", "timestamp": "2026-09-24T11:45:00.000Z", "baseline_value": "TRUE", "deviation_pct": 0.0},
            {"signal_name": "door_fully_closed", "value": "TRUE", "unit": "state", "quality": "good", "timestamp": "2026-09-24T11:45:00.000Z", "baseline_value": "TRUE", "deviation_pct": 0.0},
            {"signal_name": "door_motor_current", "value": 2.6, "unit": "A", "quality": "good", "timestamp": "2026-09-24T11:45:00.000Z", "baseline_value": 1.5, "deviation_pct": 73.3}
        ],
        "maintenance_history": [],
        "technician_free_text": "Interlock locking hook engagement depth less than 7mm OEM minimum. Door sill guide shoe has lateral play."
    }
]

# Write the 20 files
catalog = []
for sample in door_samples:
    filename = sample["filename"]
    filepath = os.path.join(telemetry_dir, filename)
    payload = {
        "elevator_id": sample["elevator_id"],
        "timestamp_utc": "2026-09-24T10:00:00.000Z",
        "operating_state": sample["operating_state"],
        "elevator_model": sample["model"],
        "installation_age_years": sample["installation_age_years"],
        "verification_stage": sample["verification_stage"],
        "alarms": sample["alarms"],

        "telemetry": sample["telemetry"],
        "maintenance_history": sample["maintenance_history"],
        "technician_free_text": sample["technician_free_text"]
    }
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    
    catalog.append({
        "filename": filename,
        "title": sample["title"],
        "fault_code": sample["fault_code"],
        "verification_stage": sample["verification_stage"],
        "subsystem": sample["subsystem"],
        "elevator_id": sample["elevator_id"],
        "model": sample["model"]
    })

# Write updated TELEMETRY_CATALOG.json with exactly 20 door samples
with open(os.path.join(telemetry_dir, "TELEMETRY_CATALOG.json"), "w", encoding="utf-8") as f:
    json.dump(catalog, f, indent=2)

print(f"Successfully generated {len(catalog)} Door Telemetry Samples in {telemetry_dir}")
