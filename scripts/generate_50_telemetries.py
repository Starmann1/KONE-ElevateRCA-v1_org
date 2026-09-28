"""
Script to generate 50 comprehensive, domain-grounded KONE elevator telemetry datasets
based on the 15-page KONE Elevate Five-Subsystem Fault Dictionary.
"""

import os
import json
from datetime import datetime, timezone


def generate_all_50():
    os.makedirs("sample_telemetry", exist_ok=True)
    telemetries = []

    # =========================================================================
    # SUBSYSTEM 1: DRIVE / MOTOR (Files 01 - 10)
    # =========================================================================
    
    # 01. IGBT Short Circuit / Inverter Failure
    telemetries.append({
        "filename": "telemetry_01_drive_igbt_short_circuit.json",
        "title": "EcoDisc Drive IGBT Inverter Short Circuit & DC Link Surge",
        "subsystem": "drive_motor",
        "data": {
            "elevator_id": "KONE-MONO-501",
            "timestamp_utc": "2026-09-24T08:15:30.000Z",
            "operating_state": "ACCELERATING",
            "elevator_model": "KONE MonoSpace 500 (EcoDisc MX10)",
            "installation_age_years": 3.5,
            "alarms": [
                {"alarm_code": "motor_overcurrent", "alarm_type": "motor_overcurrent", "severity": "critical", "subsystem": "drive_motor", "timestamp": "2026-09-24T08:15:30.000Z", "state": "ACTIVE"},
                {"alarm_code": "drive_trip", "alarm_type": "drive_trip", "severity": "critical", "subsystem": "drive_motor", "timestamp": "2026-09-24T08:15:30.300Z", "state": "ACTIVE"}
            ],
            "telemetry": [
                {"signal_name": "motor_current_rms", "value": 31.2, "unit": "A", "quality": "good", "timestamp": "2026-09-24T08:15:30.000Z", "baseline_value": 12.0, "deviation_pct": 160.0},
                {"signal_name": "igbt_temp", "value": 82.0, "unit": "°C", "quality": "good", "timestamp": "2026-09-24T08:15:30.000Z", "baseline_value": 45.0, "deviation_pct": 82.2},
                {"signal_name": "vibration_rms", "value": 0.07, "unit": "m/s2", "quality": "good", "timestamp": "2026-09-24T08:15:30.000Z", "baseline_value": 0.08, "deviation_pct": -12.5}
            ],
            "maintenance_history": [],
            "technician_free_text": "Drive self-test FAILED with internal bridge short circuit error. Inverter gate-drive fault flag TRUE."
        }
    })

    # 02. Hoistway Mechanical Jam
    telemetries.append({
        "filename": "telemetry_02_drive_mechanical_jam.json",
        "title": "Hoistway Guide Rail Obstruction & Severe Mechanical Drag",
        "subsystem": "drive_motor",
        "data": {
            "elevator_id": "KONE-MONO-502",
            "timestamp_utc": "2026-09-24T08:30:00.000Z",
            "operating_state": "CONSTANT_SPEED",
            "elevator_model": "KONE MonoSpace 700",
            "installation_age_years": 4.8,
            "alarms": [
                {"alarm_code": "motor_overcurrent", "alarm_type": "motor_overcurrent", "severity": "critical", "subsystem": "drive_motor", "timestamp": "2026-09-24T08:30:00.000Z", "state": "ACTIVE"},
                {"alarm_code": "drive_trip", "alarm_type": "drive_trip", "severity": "critical", "subsystem": "drive_motor", "timestamp": "2026-09-24T08:30:00.600Z", "state": "ACTIVE"}
            ],
            "telemetry": [
                {"signal_name": "motor_current_rms", "value": 24.5, "unit": "A", "quality": "good", "timestamp": "2026-09-24T08:30:00.000Z", "baseline_value": 12.0, "deviation_pct": 104.2},
                {"signal_name": "vibration_rms", "value": 0.32, "unit": "m/s2", "quality": "good", "timestamp": "2026-09-24T08:30:00.000Z", "baseline_value": 0.08, "deviation_pct": 300.0},
                {"signal_name": "motor_temp", "value": 71.0, "unit": "°C", "quality": "good", "timestamp": "2026-09-24T08:30:00.000Z", "baseline_value": 50.0, "deviation_pct": 42.0}
            ],
            "maintenance_history": [],
            "technician_free_text": "Severe vibration and shuddering between floors 6 and 7. Drive self-test PASSED, electronics healthy."
        }
    })

    # 03. Motor Stator Winding Insulation Degradation
    telemetries.append({
        "filename": "telemetry_03_drive_motor_winding_imbalance.json",
        "title": "PMSM Stator Phase Current Imbalance & Insulation Breakdown",
        "subsystem": "drive_motor",
        "data": {
            "elevator_id": "KONE-MONO-503",
            "timestamp_utc": "2026-09-24T09:10:00.000Z",
            "operating_state": "ACCELERATING",
            "elevator_model": "KONE MonoSpace 500",
            "installation_age_years": 8.0,
            "alarms": [
                {"alarm_code": "phase_imbalance", "alarm_type": "phase_imbalance", "severity": "warning", "subsystem": "drive_motor", "timestamp": "2026-09-24T09:10:00.000Z", "state": "ACTIVE"},
                {"alarm_code": "motor_overcurrent", "alarm_type": "motor_overcurrent", "severity": "critical", "subsystem": "drive_motor", "timestamp": "2026-09-24T09:10:01.000Z", "state": "ACTIVE"}
            ],
            "telemetry": [
                {"signal_name": "phase_current_imbalance", "value": 3.8, "unit": "A", "quality": "good", "timestamp": "2026-09-24T09:10:00.000Z", "baseline_value": 0.2, "deviation_pct": 1800.0},
                {"signal_name": "motor_temp", "value": 79.0, "unit": "°C", "quality": "good", "timestamp": "2026-09-24T09:10:00.000Z", "baseline_value": 50.0, "deviation_pct": 58.0},
                {"signal_name": "motor_current_rms", "value": 19.5, "unit": "A", "quality": "good", "timestamp": "2026-09-24T09:10:00.000Z", "baseline_value": 12.0, "deviation_pct": 62.5}
            ],
            "maintenance_history": [],
            "technician_free_text": "Phase U and W drawing asymmetric current. Stator winding temperature elevated."
        }
    })

    # 04. DC Bus Overvoltage during Regenerative Braking
    telemetries.append({
        "filename": "telemetry_04_drive_dc_bus_overvoltage_regen.json",
        "title": "VFD Intermediate DC Bus Overvoltage on Downward Deceleration",
        "subsystem": "drive_motor",
        "data": {
            "elevator_id": "KONE-MINI-304",
            "timestamp_utc": "2026-09-24T09:40:00.000Z",
            "operating_state": "DECELERATING",
            "elevator_model": "KONE MiniSpace High-Rise",
            "installation_age_years": 4.1,
            "alarms": [
                {"alarm_code": "dc_bus_overvoltage", "alarm_type": "dc_bus_overvoltage", "severity": "warning", "subsystem": "drive_motor", "timestamp": "2026-09-24T09:40:00.000Z", "state": "ACTIVE"},
                {"alarm_code": "drive_trip", "alarm_type": "drive_trip", "severity": "critical", "subsystem": "drive_motor", "timestamp": "2026-09-24T09:40:00.400Z", "state": "ACTIVE"}
            ],
            "telemetry": [
                {"signal_name": "dc_bus_voltage", "value": 785.0, "unit": "V", "quality": "good", "timestamp": "2026-09-24T09:40:00.000Z", "baseline_value": 560.0, "deviation_pct": 40.2},
                {"signal_name": "motor_current_rms", "value": 11.8, "unit": "A", "quality": "good", "timestamp": "2026-09-24T09:40:00.000Z", "baseline_value": 12.0, "deviation_pct": -1.7}
            ],
            "maintenance_history": [],
            "technician_free_text": "Overvoltage occurred specifically during full-load descent deceleration. Braking chopper circuit anomaly suspected."
        }
    })

    # 05. Seized Motor Bearing / Mechanical Binding
    telemetries.append({
        "filename": "telemetry_05_drive_seized_bearing.json",
        "title": "EcoDisc Rotor Bearing Breakdown & High Mechanical Friction",
        "subsystem": "drive_motor",
        "data": {
            "elevator_id": "KONE-MONO-505",
            "timestamp_utc": "2026-09-24T10:05:00.000Z",
            "operating_state": "CONSTANT_SPEED",
            "elevator_model": "KONE MonoSpace 500",
            "installation_age_years": 9.2,
            "alarms": [
                {"alarm_code": "motor_overcurrent", "alarm_type": "motor_overcurrent", "severity": "critical", "subsystem": "drive_motor", "timestamp": "2026-09-24T10:05:00.000Z", "state": "ACTIVE"}
            ],
            "telemetry": [
                {"signal_name": "vibration_rms", "value": 0.45, "unit": "m/s2", "quality": "good", "timestamp": "2026-09-24T10:05:00.000Z", "baseline_value": 0.08, "deviation_pct": 462.5},
                {"signal_name": "motor_temp", "value": 84.0, "unit": "°C", "quality": "good", "timestamp": "2026-09-24T10:05:00.000Z", "baseline_value": 50.0, "deviation_pct": 68.0},
                {"signal_name": "motor_current_rms", "value": 21.0, "unit": "A", "quality": "good", "timestamp": "2026-09-24T10:05:00.000Z", "baseline_value": 12.0, "deviation_pct": 75.0}
            ],
            "maintenance_history": [],
            "technician_free_text": "High acoustic squeal from motor machine assembly. High high-frequency bearing vibration."
        }
    })

    # 06. Intermittent Motor Power Cable Loose Terminal
    telemetries.append({
        "filename": "telemetry_06_drive_cable_terminal_fault.json",
        "title": "VFD Output Cable Terminal Looseness & Current Spiking",
        "subsystem": "drive_motor",
        "data": {
            "elevator_id": "KONE-MONO-506",
            "timestamp_utc": "2026-09-24T10:30:00.000Z",
            "operating_state": "ACCELERATING",
            "elevator_model": "KONE MonoSpace 500",
            "installation_age_years": 6.1,
            "alarms": [
                {"alarm_code": "motor_overcurrent", "alarm_type": "motor_overcurrent", "severity": "warning", "subsystem": "drive_motor", "timestamp": "2026-09-24T10:30:00.000Z", "state": "ACTIVE"}
            ],
            "telemetry": [
                {"signal_name": "motor_current_rms", "value": 26.0, "unit": "A", "quality": "good", "timestamp": "2026-09-24T10:30:00.000Z", "baseline_value": 12.0, "deviation_pct": 116.7},
                {"signal_name": "vibration_rms", "value": 0.09, "unit": "m/s2", "quality": "good", "timestamp": "2026-09-24T10:30:00.000Z", "baseline_value": 0.08, "deviation_pct": 12.5}
            ],
            "maintenance_history": [],
            "technician_free_text": "Transient overcurrent spike during upward acceleration. No steady mechanical load."
        }
    })

    # 07. VFD Current Limit Parameter Misconfiguration
    telemetries.append({
        "filename": "telemetry_07_drive_vfd_parameter_misconfig.json",
        "title": "VFD Software Current Trip Threshold Misconfiguration",
        "subsystem": "drive_motor",
        "data": {
            "elevator_id": "KONE-MONO-507",
            "timestamp_utc": "2026-09-24T11:00:00.000Z",
            "operating_state": "ACCELERATING",
            "elevator_model": "KONE MonoSpace 500",
            "installation_age_years": 1.2,
            "alarms": [
                {"alarm_code": "motor_overcurrent", "alarm_type": "motor_overcurrent", "severity": "warning", "subsystem": "drive_motor", "timestamp": "2026-09-24T11:00:00.000Z", "state": "ACTIVE"}
            ],
            "telemetry": [
                {"signal_name": "motor_current_rms", "value": 15.5, "unit": "A", "quality": "good", "timestamp": "2026-09-24T11:00:00.000Z", "baseline_value": 12.0, "deviation_pct": 29.2}
            ],
            "maintenance_history": [
                {"date": "2026-09-22T14:00:00Z", "component": "VFD Controller", "action": "Firmware parameter update and tuning", "technician_notes": "Updated drive parameter profile", "part_replaced": False}
            ],
            "technician_free_text": "Fault began occurring immediately following drive parameter update."
        }
    })

    # 08. DC Link Capacitor Degradation
    telemetries.append({
        "filename": "telemetry_08_drive_dc_link_capacitor_wear.json",
        "title": "VFD DC-Link Intermediate Capacitor Bank Aging & Ripple",
        "subsystem": "drive_motor",
        "data": {
            "elevator_id": "KONE-MONO-508",
            "timestamp_utc": "2026-09-24T11:20:00.000Z",
            "operating_state": "CONSTANT_SPEED",
            "elevator_model": "KONE MonoSpace 500",
            "installation_age_years": 11.5,
            "alarms": [
                {"alarm_code": "undervoltage", "alarm_type": "undervoltage", "severity": "warning", "subsystem": "drive_motor", "timestamp": "2026-09-24T11:20:00.000Z", "state": "ACTIVE"}
            ],
            "telemetry": [
                {"signal_name": "dc_bus_voltage", "value": 470.0, "unit": "V", "quality": "good", "timestamp": "2026-09-24T11:20:00.000Z", "baseline_value": 560.0, "deviation_pct": -16.1},
                {"signal_name": "motor_current_rms", "value": 14.8, "unit": "A", "quality": "good", "timestamp": "2026-09-24T11:20:00.000Z", "baseline_value": 12.0, "deviation_pct": 23.3}
            ],
            "maintenance_history": [],
            "technician_free_text": "DC bus voltage sag and high ripple voltage detected across intermediate filter capacitors."
        }
    })

    # 09. Motor Stator Overheating Under Extended Duty
    telemetries.append({
        "filename": "telemetry_09_drive_motor_thermal_overload.json",
        "title": "EcoDisc PMSM Thermal Overload Under Heavy Peak Duty",
        "subsystem": "drive_motor",
        "data": {
            "elevator_id": "KONE-MONO-509",
            "timestamp_utc": "2026-09-24T11:45:00.000Z",
            "operating_state": "CONSTANT_SPEED",
            "elevator_model": "KONE MonoSpace 700",
            "installation_age_years": 5.0,
            "alarms": [
                {"alarm_code": "motor_overheat", "alarm_type": "motor_overheat", "severity": "warning", "subsystem": "drive_motor", "timestamp": "2026-09-24T11:45:00.000Z", "state": "ACTIVE"}
            ],
            "telemetry": [
                {"signal_name": "motor_temp", "value": 92.0, "unit": "°C", "quality": "good", "timestamp": "2026-09-24T11:45:00.000Z", "baseline_value": 50.0, "deviation_pct": 84.0},
                {"signal_name": "motor_current_rms", "value": 14.0, "unit": "A", "quality": "good", "timestamp": "2026-09-24T11:45:00.000Z", "baseline_value": 12.0, "deviation_pct": 16.7}
            ],
            "maintenance_history": [],
            "technician_free_text": "Elevator in continuous peak traffic for 4 hours. Motor thermistor tripped warning limit."
        }
    })

    # 10. IGBT Thermal Runaway & Cooling Fan Stoppage
    telemetries.append({
        "filename": "telemetry_10_drive_igbt_thermal_runaway.json",
        "title": "Inverter Heatsink Cooling Clogged & Thermal Trip",
        "subsystem": "drive_motor",
        "data": {
            "elevator_id": "KONE-MONO-510",
            "timestamp_utc": "2026-09-24T12:00:00.000Z",
            "operating_state": "CONSTANT_SPEED",
            "elevator_model": "KONE MonoSpace 500",
            "installation_age_years": 6.5,
            "alarms": [
                {"alarm_code": "drive_trip", "alarm_type": "drive_trip", "severity": "critical", "subsystem": "drive_motor", "timestamp": "2026-09-24T12:00:00.000Z", "state": "ACTIVE"}
            ],
            "telemetry": [
                {"signal_name": "igbt_temp", "value": 89.0, "unit": "°C", "quality": "good", "timestamp": "2026-09-24T12:00:00.000Z", "baseline_value": 45.0, "deviation_pct": 97.8},
                {"signal_name": "motor_current_rms", "value": 12.4, "unit": "A", "quality": "good", "timestamp": "2026-09-24T12:00:00.000Z", "baseline_value": 12.0, "deviation_pct": 3.3}
            ],
            "maintenance_history": [],
            "technician_free_text": "IGBT junction temperature spiked to 89°C while motor current remained nominal. Heatsink fan failed."
        }
    })

    # =========================================================================
    # SUBSYSTEM 2: DOOR SYSTEM (Files 11 - 20)
    # =========================================================================

    # 11. THE USER'S SPECIFIC SCENARIO: Repeat Roller Replacement vs Track Misalignment / Placement
    telemetries.append({
        "filename": "telemetry_11_door_repeat_roller_misdiagnosis_track_misalignment.json",
        "title": "Door Track Misalignment / Geometric Placement (Resolving Repeat Roller Swaps)",
        "subsystem": "door",
        "data": {
            "elevator_id": "KONE-MONO-511",
            "timestamp_utc": "2026-09-24T12:30:00.000Z",
            "operating_state": "DOOR_CLOSE",
            "elevator_model": "KONE MonoSpace 500",
            "installation_age_years": 4.2,
            "alarms": [
                {"alarm_code": "door_close_timeout", "alarm_type": "door_close_timeout", "severity": "critical", "subsystem": "door", "timestamp": "2026-09-24T12:30:00.000Z", "state": "ACTIVE"},
                {"alarm_code": "door_motor_overcurrent", "alarm_type": "door_motor_overcurrent", "severity": "warning", "subsystem": "door", "timestamp": "2026-09-24T12:30:02.000Z", "state": "ACTIVE"}
            ],
            "telemetry": [
                {"signal_name": "door_cycle_time_ms", "value": 4900.0, "unit": "ms", "quality": "good", "timestamp": "2026-09-24T12:30:00.000Z", "baseline_value": 2800.0, "deviation_pct": 75.0},
                {"signal_name": "door_motor_current", "value": 2.7, "unit": "A", "quality": "good", "timestamp": "2026-09-24T12:30:00.000Z", "baseline_value": 1.5, "deviation_pct": 80.0},
                {"signal_name": "vibration_rms", "value": 0.22, "unit": "m/s2", "quality": "good", "timestamp": "2026-09-24T12:30:00.000Z", "baseline_value": 0.08, "deviation_pct": 175.0}
            ],
            "maintenance_history": [
                {"date": "2026-06-10T10:00:00Z", "component": "Door Roller", "action": "Replaced worn hanger rollers", "technician_notes": "Replaced top rollers after door timeout fault", "part_replaced": True},
                {"date": "2026-08-15T14:30:00Z", "component": "Door Roller", "action": "Replaced hanger rollers again", "technician_notes": "Door sticking again, installed new rollers", "part_replaced": True}
            ],
            "technician_free_text": "Previous technicians replaced door rollers twice in past 3 months but door binding persists. Header track appears twisted/misaligned near close position."
        }
    })

    # 12. 3D Light Curtain Optical Degradation
    telemetries.append({
        "filename": "telemetry_12_door_light_curtain_optical_drift.json",
        "title": "3D Light Curtain Multi-Beam Optical Degradation & False Reopenings",
        "subsystem": "door",
        "data": {
            "elevator_id": "KONE-MINI-312",
            "timestamp_utc": "2026-09-24T12:50:00.000Z",
            "operating_state": "DOOR_CLOSE",
            "elevator_model": "KONE MiniSpace",
            "installation_age_years": 5.5,
            "alarms": [
                {"alarm_code": "door_obstruction_detected", "alarm_type": "door_obstruction_detected", "severity": "warning", "subsystem": "door", "timestamp": "2026-09-24T12:49:50.000Z", "state": "ACTIVE"},
                {"alarm_code": "door_close_timeout", "alarm_type": "door_close_timeout", "severity": "critical", "subsystem": "door", "timestamp": "2026-09-24T12:50:00.000Z", "state": "ACTIVE"}
            ],
            "telemetry": [
                {"signal_name": "door_cycle_time_ms", "value": 4350.0, "unit": "ms", "quality": "good", "timestamp": "2026-09-24T12:50:00.000Z", "baseline_value": 2800.0, "deviation_pct": 55.4},
                {"signal_name": "door_motor_current", "value": 1.55, "unit": "A", "quality": "good", "timestamp": "2026-09-24T12:50:00.000Z", "baseline_value": 1.5, "deviation_pct": 3.3}
            ],
            "maintenance_history": [],
            "technician_free_text": "Doors reopen repeatedly with no obstacle present. Reopening occurs at random varying door positions, photo-eye signal erratic."
        }
    })

    # 13. Fixed Physical Sill Obstruction (Debris)
    telemetries.append({
        "filename": "telemetry_13_door_sill_physical_obstruction.json",
        "title": "Landing Sill Foreign Object Blockage at Exact Position",
        "subsystem": "door",
        "data": {
            "elevator_id": "KONE-MONO-513",
            "timestamp_utc": "2026-09-24T13:15:00.000Z",
            "operating_state": "DOOR_CLOSE",
            "elevator_model": "KONE MonoSpace 500",
            "installation_age_years": 2.0,
            "alarms": [
                {"alarm_code": "door_close_timeout", "alarm_type": "door_close_timeout", "severity": "critical", "subsystem": "door", "timestamp": "2026-09-24T13:15:00.000Z", "state": "ACTIVE"}
            ],
            "telemetry": [
                {"signal_name": "door_motor_current", "value": 3.2, "unit": "A", "quality": "good", "timestamp": "2026-09-24T13:15:00.000Z", "baseline_value": 1.5, "deviation_pct": 113.3},
                {"signal_name": "door_cycle_time_ms", "value": 5200.0, "unit": "ms", "quality": "good", "timestamp": "2026-09-24T13:15:00.000Z", "baseline_value": 2800.0, "deviation_pct": 85.7}
            ],
            "maintenance_history": [],
            "technician_free_text": "Door hits a hard stop at consistent location 120mm before fully closed. Physical object wedged in sill groove."
        }
    })

    # 14. Door Hanger Roller Bearing Flat Spots
    telemetries.append({
        "filename": "telemetry_14_door_roller_bearing_wear.json",
        "title": "Single-Cycle Door Roller Bearing Flat Spot Wear",
        "subsystem": "door",
        "data": {
            "elevator_id": "KONE-MONO-514",
            "timestamp_utc": "2026-09-24T13:30:00.000Z",
            "operating_state": "DOOR_CLOSE",
            "elevator_model": "KONE MonoSpace 500",
            "installation_age_years": 7.5,
            "alarms": [
                {"alarm_code": "door_close_timeout", "alarm_type": "door_close_timeout", "severity": "warning", "subsystem": "door", "timestamp": "2026-09-24T13:30:00.000Z", "state": "ACTIVE"}
            ],
            "telemetry": [
                {"signal_name": "door_motor_current", "value": 2.2, "unit": "A", "quality": "good", "timestamp": "2026-09-24T13:30:00.000Z", "baseline_value": 1.5, "deviation_pct": 46.7},
                {"signal_name": "door_cycle_time_ms", "value": 3800.0, "unit": "ms", "quality": "good", "timestamp": "2026-09-24T13:30:00.000Z", "baseline_value": 2800.0, "deviation_pct": 35.7}
            ],
            "maintenance_history": [],
            "technician_free_text": "Polyurethane roller tread degraded with flat spot. Rollers have never been replaced since commissioning."
        }
    })

    # 15. Door Interlock Lock Contact Pitting / Oxidation
    telemetries.append({
        "filename": "telemetry_15_door_lock_contact_pitting.json",
        "title": "Landing Door Interlock Electrical Contact Oxidation",
        "subsystem": "door",
        "data": {
            "elevator_id": "KONE-MONO-515",
            "timestamp_utc": "2026-09-24T13:50:00.000Z",
            "operating_state": "DOOR_CLOSE",
            "elevator_model": "KONE MonoSpace 500",
            "installation_age_years": 8.5,
            "alarms": [
                {"alarm_code": "door_lock_not_confirmed", "alarm_type": "door_lock_not_confirmed", "severity": "critical", "subsystem": "door", "timestamp": "2026-09-24T13:50:00.000Z", "state": "ACTIVE"},
                {"alarm_code": "safety_chain_open", "alarm_type": "safety_chain_open", "severity": "critical", "subsystem": "safety_chain", "timestamp": "2026-09-24T13:50:01.000Z", "state": "ACTIVE"}
            ],
            "telemetry": [
                {"signal_name": "door_motor_current", "value": 1.5, "unit": "A", "quality": "good", "timestamp": "2026-09-24T13:50:00.000Z", "baseline_value": 1.5, "deviation_pct": 0.0}
            ],
            "maintenance_history": [],
            "technician_free_text": "Door physically closed flush, but electrical lock contact failed to confirm closed state."
        }
    })

    # 16. Door Operator Drive Belt Slip & Tension Loss
    telemetries.append({
        "filename": "telemetry_16_door_drive_belt_slip.json",
        "title": "Door Operator Toothed Belt Stretch & Speed Variation",
        "subsystem": "door",
        "data": {
            "elevator_id": "KONE-MONO-516",
            "timestamp_utc": "2026-09-24T14:10:00.000Z",
            "operating_state": "DOOR_CLOSE",
            "elevator_model": "KONE MonoSpace 500",
            "installation_age_years": 6.0,
            "alarms": [
                {"alarm_code": "door_close_timeout", "alarm_type": "door_close_timeout", "severity": "warning", "subsystem": "door", "timestamp": "2026-09-24T14:10:00.000Z", "state": "ACTIVE"}
            ],
            "telemetry": [
                {"signal_name": "door_speed_variation", "value": 32.0, "unit": "rpm", "quality": "good", "timestamp": "2026-09-24T14:10:00.000Z", "baseline_value": 5.0, "deviation_pct": 540.0},
                {"signal_name": "door_cycle_time_ms", "value": 3950.0, "unit": "ms", "quality": "good", "timestamp": "2026-09-24T14:10:00.000Z", "baseline_value": 2800.0, "deviation_pct": 41.1}
            ],
            "maintenance_history": [],
            "technician_free_text": "Drive motor turning smoothly but door panel movement lags. Belt tension severely slack."
        }
    })

    # 17. Door Motor Commutator / Winding Degradation
    telemetries.append({
        "filename": "telemetry_17_door_operator_motor_wear.json",
        "title": "Door Operator PM Motor Torque Loss & Current Rise",
        "subsystem": "door",
        "data": {
            "elevator_id": "KONE-MONO-517",
            "timestamp_utc": "2026-09-24T14:30:00.000Z",
            "operating_state": "DOOR_OPEN",
            "elevator_model": "KONE MonoSpace 500",
            "installation_age_years": 9.0,
            "alarms": [
                {"alarm_code": "door_motor_overcurrent", "alarm_type": "door_motor_overcurrent", "severity": "warning", "subsystem": "door", "timestamp": "2026-09-24T14:30:00.000Z", "state": "ACTIVE"}
            ],
            "telemetry": [
                {"signal_name": "door_motor_current", "value": 2.8, "unit": "A", "quality": "good", "timestamp": "2026-09-24T14:30:00.000Z", "baseline_value": 1.5, "deviation_pct": 86.7},
                {"signal_name": "door_cycle_time_ms", "value": 4100.0, "unit": "ms", "quality": "good", "timestamp": "2026-09-24T14:30:00.000Z", "baseline_value": 2800.0, "deviation_pct": 46.4}
            ],
            "maintenance_history": [],
            "technician_free_text": "Door operator motor running very hot. Armature drawing high current under light manual load."
        }
    })

    # 18. Optical Photo-Eye Lens Surface Contamination
    telemetries.append({
        "filename": "telemetry_18_door_photoeye_lens_dirt.json",
        "title": "Single-Beam Optical Safety Edge Lens Dust Clouding",
        "subsystem": "door",
        "data": {
            "elevator_id": "KONE-MINI-318",
            "timestamp_utc": "2026-09-24T14:50:00.000Z",
            "operating_state": "DOOR_CLOSE",
            "elevator_model": "KONE MiniSpace",
            "installation_age_years": 3.0,
            "alarms": [
                {"alarm_code": "door_obstruction_detected", "alarm_type": "door_obstruction_detected", "severity": "warning", "subsystem": "door", "timestamp": "2026-09-24T14:50:00.000Z", "state": "ACTIVE"}
            ],
            "telemetry": [
                {"signal_name": "door_cycle_time_ms", "value": 3700.0, "unit": "ms", "quality": "good", "timestamp": "2026-09-24T14:50:00.000Z", "baseline_value": 2800.0, "deviation_pct": 32.1}
            ],
            "maintenance_history": [],
            "technician_free_text": "Heavy drywall dust in lobby. Photo-eye receiver lens coated in dust film."
        }
    })

    # 19. Door Open Limit Switch Contact Failure
    telemetries.append({
        "filename": "telemetry_19_door_open_limit_sensor_fault.json",
        "title": "Door Full-Open Limit Switch Microswitch Open-Circuit",
        "subsystem": "door",
        "data": {
            "elevator_id": "KONE-MONO-519",
            "timestamp_utc": "2026-09-24T15:10:00.000Z",
            "operating_state": "DOOR_OPEN",
            "elevator_model": "KONE MonoSpace 500",
            "installation_age_years": 5.2,
            "alarms": [
                {"alarm_code": "door_close_timeout", "alarm_type": "door_close_timeout", "severity": "warning", "subsystem": "door", "timestamp": "2026-09-24T15:10:00.000Z", "state": "ACTIVE"}
            ],
            "telemetry": [
                {"signal_name": "door_motor_current", "value": 1.6, "unit": "A", "quality": "good", "timestamp": "2026-09-24T15:10:00.000Z", "baseline_value": 1.5, "deviation_pct": 6.7}
            ],
            "maintenance_history": [],
            "technician_free_text": "Doors reached full mechanical open position but controller failed to receive open-limit signal."
        }
    })

    # 20. Door Close Limit Switch Mechanical Jam
    telemetries.append({
        "filename": "telemetry_20_door_close_limit_switch_jam.json",
        "title": "Door Full-Close Limit Sensor Cam Misalignment",
        "subsystem": "door",
        "data": {
            "elevator_id": "KONE-MONO-520",
            "timestamp_utc": "2026-09-24T15:30:00.000Z",
            "operating_state": "DOOR_CLOSE",
            "elevator_model": "KONE MonoSpace 500",
            "installation_age_years": 4.5,
            "alarms": [
                {"alarm_code": "door_lock_not_confirmed", "alarm_type": "door_lock_not_confirmed", "severity": "critical", "subsystem": "door", "timestamp": "2026-09-24T15:30:00.000Z", "state": "ACTIVE"}
            ],
            "telemetry": [
                {"signal_name": "door_cycle_time_ms", "value": 3600.0, "unit": "ms", "quality": "good", "timestamp": "2026-09-24T15:30:00.000Z", "baseline_value": 2800.0, "deviation_pct": 28.6}
            ],
            "maintenance_history": [],
            "technician_free_text": "Close limit actuator cam bent, failing to trigger close limit switch."
        }
    })

    # =========================================================================
    # SUBSYSTEM 3: BRAKE / TRACTION (Files 21 - 30)
    # =========================================================================

    # 21. Brake Release Timing Violation
    telemetries.append({
        "filename": "telemetry_21_brake_release_timing_delay.json",
        "title": "EcoDisc Brake Armature Lift Delay Exceeding Millisecond Tolerance",
        "subsystem": "brake_traction",
        "data": {
            "elevator_id": "KONE-MONO-521",
            "timestamp_utc": "2026-09-24T15:50:00.000Z",
            "operating_state": "ACCELERATING",
            "elevator_model": "KONE MonoSpace 500",
            "installation_age_years": 3.8,
            "alarms": [
                {"alarm_code": "brake_fault", "alarm_type": "brake_fault", "severity": "critical", "subsystem": "brake_traction", "timestamp": "2026-09-24T15:50:00.000Z", "state": "ACTIVE"},
                {"alarm_code": "brake_timing_violation", "alarm_type": "brake_timing_violation", "severity": "critical", "subsystem": "brake_traction", "timestamp": "2026-09-24T15:50:00.350Z", "state": "ACTIVE"}
            ],
            "telemetry": [
                {"signal_name": "brake_release_delay", "value": 375.0, "unit": "ms", "quality": "good", "timestamp": "2026-09-24T15:50:00.000Z", "baseline_value": 150.0, "deviation_pct": 150.0},
                {"signal_name": "position_drift_mm", "value": 3.9, "unit": "mm", "quality": "good", "timestamp": "2026-09-24T15:50:00.000Z", "baseline_value": 0.5, "deviation_pct": 680.0},
                {"signal_name": "motor_current_rms", "value": 12.8, "unit": "A", "quality": "good", "timestamp": "2026-09-24T15:50:00.000Z", "baseline_value": 12.0, "deviation_pct": 6.7}
            ],
            "maintenance_history": [],
            "technician_free_text": "Brake lift monitoring switch timed out before motor energization. Motor torque demand nominal."
        }
    })

    # 22. Brake Friction Pad Lining Wear
    telemetries.append({
        "filename": "telemetry_22_brake_lining_wear_slip.json",
        "title": "EcoDisc Brake Lining Friction Material Thinning & Car Slip",
        "subsystem": "brake_traction",
        "data": {
            "elevator_id": "KONE-MONO-522",
            "timestamp_utc": "2026-09-24T16:10:00.000Z",
            "operating_state": "IDLE",
            "elevator_model": "KONE MonoSpace 500",
            "installation_age_years": 10.0,
            "alarms": [
                {"alarm_code": "brake_fault", "alarm_type": "brake_fault", "severity": "critical", "subsystem": "brake_traction", "timestamp": "2026-09-24T16:10:00.000Z", "state": "ACTIVE"},
                {"alarm_code": "position_drift", "alarm_type": "position_drift", "severity": "warning", "subsystem": "brake_traction", "timestamp": "2026-09-24T16:10:01.000Z", "state": "ACTIVE"}
            ],
            "telemetry": [
                {"signal_name": "position_drift_mm", "value": 6.5, "unit": "mm", "quality": "good", "timestamp": "2026-09-24T16:10:00.000Z", "baseline_value": 0.5, "deviation_pct": 1200.0},
                {"signal_name": "brake_holding_force", "value": 62.0, "unit": "%", "quality": "good", "timestamp": "2026-09-24T16:10:00.000Z", "baseline_value": 100.0, "deviation_pct": -38.0}
            ],
            "maintenance_history": [],
            "technician_free_text": "Elevator car drifted 6.5mm downward while stopped with doors open and heavy load boarding."
        }
    })

    # 23. Brake Actuation Solenoid Coil Current Drop
    telemetries.append({
        "filename": "telemetry_23_brake_solenoid_coil_fault.json",
        "title": "Brake Electromagnetic Coil Resistance Shift & Weak Pull-In",
        "subsystem": "brake_traction",
        "data": {
            "elevator_id": "KONE-MONO-523",
            "timestamp_utc": "2026-09-24T16:30:00.000Z",
            "operating_state": "ACCELERATING",
            "elevator_model": "KONE MonoSpace 500",
            "installation_age_years": 7.0,
            "alarms": [
                {"alarm_code": "brake_fault", "alarm_type": "brake_fault", "severity": "critical", "subsystem": "brake_traction", "timestamp": "2026-09-24T16:30:00.000Z", "state": "ACTIVE"}
            ],
            "telemetry": [
                {"signal_name": "brake_coil_current", "value": 0.8, "unit": "A", "quality": "good", "timestamp": "2026-09-24T16:30:00.000Z", "baseline_value": 2.2, "deviation_pct": -63.6}
            ],
            "maintenance_history": [],
            "technician_free_text": "Brake coil circuit resistance abnormal. Coil current dropped below minimum pickup threshold."
        }
    })

    # 24. Suspension Rope Wire-Break Count Exceeded
    telemetries.append({
        "filename": "telemetry_24_traction_rope_wire_breaks.json",
        "title": "Steel Suspension Rope Wire Strand Fatigue & High Vibration",
        "subsystem": "brake_traction",
        "data": {
            "elevator_id": "KONE-MINI-324",
            "timestamp_utc": "2026-09-24T16:50:00.000Z",
            "operating_state": "CONSTANT_SPEED",
            "elevator_model": "KONE MiniSpace",
            "installation_age_years": 8.5,
            "alarms": [
                {"alarm_code": "rope_slip_detected", "alarm_type": "rope_slip_detected", "severity": "warning", "subsystem": "brake_traction", "timestamp": "2026-09-24T16:50:00.000Z", "state": "ACTIVE"}
            ],
            "telemetry": [
                {"signal_name": "traction_slip_ratio", "value": 4.5, "unit": "%", "quality": "good", "timestamp": "2026-09-24T16:50:00.000Z", "baseline_value": 0.5, "deviation_pct": 800.0},
                {"signal_name": "vibration_rms", "value": 0.26, "unit": "m/s2", "quality": "good", "timestamp": "2026-09-24T16:50:00.000Z", "baseline_value": 0.08, "deviation_pct": 225.0}
            ],
            "maintenance_history": [],
            "technician_free_text": "Rope condition monitoring sensor logged multiple broken wire strands on rope 3."
        }
    })

    # 25. Traction Sheave Groove Wear & Rope Slip
    telemetries.append({
        "filename": "telemetry_25_traction_sheave_groove_wear.json",
        "title": "EcoDisc Drive Sheave Undercut Groove Wear & Slip Under Load",
        "subsystem": "brake_traction",
        "data": {
            "elevator_id": "KONE-MONO-525",
            "timestamp_utc": "2026-09-24T17:10:00.000Z",
            "operating_state": "ACCELERATING",
            "elevator_model": "KONE MonoSpace 700",
            "installation_age_years": 12.0,
            "alarms": [
                {"alarm_code": "rope_slip_detected", "alarm_type": "rope_slip_detected", "severity": "warning", "subsystem": "brake_traction", "timestamp": "2026-09-24T17:10:00.000Z", "state": "ACTIVE"}
            ],
            "telemetry": [
                {"signal_name": "traction_slip_ratio", "value": 6.8, "unit": "%", "quality": "good", "timestamp": "2026-09-24T17:10:00.000Z", "baseline_value": 0.5, "deviation_pct": 1260.0},
                {"signal_name": "speed_feedback_deviation", "value": 16.0, "unit": "rpm", "quality": "good", "timestamp": "2026-09-24T17:10:00.000Z", "baseline_value": 5.0, "deviation_pct": 220.0}
            ],
            "maintenance_history": [],
            "technician_free_text": "Ropes bottoming out in hardened sheave grooves. Significant slip during high acceleration."
        }
    })

    # 26. Counterweight Imbalance & Asymmetric Directional Current
    telemetries.append({
        "filename": "telemetry_26_traction_counterweight_imbalance.json",
        "title": "Counterweight Filler Block Imbalance & Directional Load Asymmetry",
        "subsystem": "brake_traction",
        "data": {
            "elevator_id": "KONE-MONO-526",
            "timestamp_utc": "2026-09-24T17:30:00.000Z",
            "operating_state": "CONSTANT_SPEED",
            "elevator_model": "KONE MonoSpace 500",
            "installation_age_years": 2.5,
            "alarms": [
                {"alarm_code": "motor_overcurrent", "alarm_type": "motor_overcurrent", "severity": "warning", "subsystem": "drive_motor", "timestamp": "2026-09-24T17:30:00.000Z", "state": "ACTIVE"}
            ],
            "telemetry": [
                {"signal_name": "directional_current_imbalance", "value": 8.5, "unit": "A", "quality": "good", "timestamp": "2026-09-24T17:30:00.000Z", "baseline_value": 1.0, "deviation_pct": 750.0},
                {"signal_name": "motor_current_rms", "value": 18.2, "unit": "A", "quality": "good", "timestamp": "2026-09-24T17:30:00.000Z", "baseline_value": 12.0, "deviation_pct": 51.7}
            ],
            "maintenance_history": [],
            "technician_free_text": "Up-direction travel draws 18.2A while down-direction travel draws only 5.1A with empty car."
        }
    })

    # 27. Overspeed Governor Mechanical Trip (UCMP)
    telemetries.append({
        "filename": "telemetry_27_brake_governor_overspeed_trip.json",
        "title": "Car Overspeed Governor Contact Trip & Safety Gear Engagement",
        "subsystem": "brake_traction",
        "data": {
            "elevator_id": "KONE-MINI-327",
            "timestamp_utc": "2026-09-24T17:50:00.000Z",
            "operating_state": "CONSTANT_SPEED",
            "elevator_model": "KONE MiniSpace",
            "installation_age_years": 4.0,
            "alarms": [
                {"alarm_code": "overspeed_detected", "alarm_type": "overspeed_detected", "severity": "critical", "subsystem": "safety_chain", "timestamp": "2026-09-24T17:50:00.000Z", "state": "ACTIVE"},
                {"alarm_code": "safety_chain_open", "alarm_type": "safety_chain_open", "severity": "critical", "subsystem": "safety_chain", "timestamp": "2026-09-24T17:50:00.100Z", "state": "ACTIVE"}
            ],
            "telemetry": [
                {"signal_name": "car_velocity_pct", "value": 122.0, "unit": "%", "quality": "good", "timestamp": "2026-09-24T17:50:00.000Z", "baseline_value": 100.0, "deviation_pct": 22.0}
            ],
            "maintenance_history": [],
            "technician_free_text": "Governor flyweights swung out and opened overspeed safety switch during downward run."
        }
    })

    # 28. Unequal Suspension Rope Tension
    telemetries.append({
        "filename": "telemetry_28_traction_unequal_rope_tension.json",
        "title": "Individual Suspension Rope Tension Imbalance & Vibration",
        "subsystem": "brake_traction",
        "data": {
            "elevator_id": "KONE-MONO-528",
            "timestamp_utc": "2026-09-24T18:10:00.000Z",
            "operating_state": "CONSTANT_SPEED",
            "elevator_model": "KONE MonoSpace 500",
            "installation_age_years": 5.0,
            "alarms": [
                {"alarm_code": "rope_slip_detected", "alarm_type": "rope_slip_detected", "severity": "warning", "subsystem": "brake_traction", "timestamp": "2026-09-24T18:10:00.000Z", "state": "ACTIVE"}
            ],
            "telemetry": [
                {"signal_name": "rope_tension_imbalance", "value": 35.0, "unit": "%", "quality": "good", "timestamp": "2026-09-24T18:10:00.000Z", "baseline_value": 5.0, "deviation_pct": 600.0},
                {"signal_name": "vibration_rms", "value": 0.19, "unit": "m/s2", "quality": "good", "timestamp": "2026-09-24T18:10:00.000Z", "baseline_value": 0.08, "deviation_pct": 137.5}
            ],
            "maintenance_history": [],
            "technician_free_text": "Spring tensioners on rope hitch unequal. Rope 2 carrying 60% of total car load."
        }
    })

    # 29. Unintended Car Movement (UCMP) at Landing
    telemetries.append({
        "filename": "telemetry_29_brake_ucmp_unintended_movement.json",
        "title": "Unintended Car Movement Away from Landing with Doors Unlocked",
        "subsystem": "brake_traction",
        "data": {
            "elevator_id": "KONE-MONO-529",
            "timestamp_utc": "2026-09-24T18:30:00.000Z",
            "operating_state": "IDLE",
            "elevator_model": "KONE MonoSpace 500",
            "installation_age_years": 3.0,
            "alarms": [
                {"alarm_code": "unintended_movement", "alarm_type": "unintended_movement", "severity": "critical", "subsystem": "brake_traction", "timestamp": "2026-09-24T18:30:00.000Z", "state": "ACTIVE"},
                {"alarm_code": "safety_chain_open", "alarm_type": "safety_chain_open", "severity": "critical", "subsystem": "safety_chain", "timestamp": "2026-09-24T18:30:00.200Z", "state": "ACTIVE"}
            ],
            "telemetry": [
                {"signal_name": "position_drift_mm", "value": 145.0, "unit": "mm", "quality": "good", "timestamp": "2026-09-24T18:30:00.000Z", "baseline_value": 0.5, "deviation_pct": 28900.0}
            ],
            "maintenance_history": [],
            "technician_free_text": "UCMP module detected car moving outside door zone without drive run command. Safety gear clamped."
        }
    })

    # 30. Brake Microswitch Lift Verification Mismatch
    telemetries.append({
        "filename": "telemetry_30_brake_microswitch_contact_bounce.json",
        "title": "Brake Shoe Feedback Microswitch Contact Chatter",
        "subsystem": "brake_traction",
        "data": {
            "elevator_id": "KONE-MONO-530",
            "timestamp_utc": "2026-09-24T18:50:00.000Z",
            "operating_state": "ACCELERATING",
            "elevator_model": "KONE MonoSpace 500",
            "installation_age_years": 6.8,
            "alarms": [
                {"alarm_code": "brake_fault", "alarm_type": "brake_fault", "severity": "critical", "subsystem": "brake_traction", "timestamp": "2026-09-24T18:50:00.000Z", "state": "ACTIVE"}
            ],
            "telemetry": [
                {"signal_name": "brake_release_delay", "value": 155.0, "unit": "ms", "quality": "good", "timestamp": "2026-09-24T18:50:00.000Z", "baseline_value": 150.0, "deviation_pct": 3.3}
            ],
            "maintenance_history": [],
            "technician_free_text": "Brake lifted mechanically, but left-side microswitch feedback contact flickered."
        }
    })

    # =========================================================================
    # SUBSYSTEM 4: ENCODER / POSITION (Files 31 - 40)
    # =========================================================================

    # 31. Optical Encoder Pulse Loss & Leveling Deviation
    telemetries.append({
        "filename": "telemetry_31_encoder_pulse_loss_leveling_fault.json",
        "title": "EcoDisc Motor Encoder Pulse Loss & Floor Leveling Deviation",
        "subsystem": "encoder_position",
        "data": {
            "elevator_id": "KONE-MONO-531",
            "timestamp_utc": "2026-09-24T19:10:00.000Z",
            "operating_state": "DECELERATING",
            "elevator_model": "KONE MonoSpace 500",
            "installation_age_years": 3.1,
            "alarms": [
                {"alarm_code": "leveling_deviation", "alarm_type": "leveling_deviation", "severity": "warning", "subsystem": "encoder_position", "timestamp": "2026-09-24T19:10:00.000Z", "state": "ACTIVE"},
                {"alarm_code": "encoder_fault", "alarm_type": "encoder_fault", "severity": "critical", "subsystem": "encoder_position", "timestamp": "2026-09-24T19:10:01.000Z", "state": "ACTIVE"}
            ],
            "telemetry": [
                {"signal_name": "position_actual_divergence", "value": 7.2, "unit": "mm", "quality": "good", "timestamp": "2026-09-24T19:10:00.000Z", "baseline_value": 1.0, "deviation_pct": 620.0},
                {"signal_name": "leveling_deviation_mm", "value": 9.0, "unit": "mm", "quality": "good", "timestamp": "2026-09-24T19:10:00.000Z", "baseline_value": 2.0, "deviation_pct": 350.0},
                {"signal_name": "speed_feedback_deviation", "value": 15.0, "unit": "rpm", "quality": "good", "timestamp": "2026-09-24T19:10:00.000Z", "baseline_value": 5.0, "deviation_pct": 200.0}
            ],
            "maintenance_history": [],
            "technician_free_text": "Independent leveling sensor reports car is physically level, but motor encoder count drifted."
        }
    })

    # 32. Shaft Encoder Mechanical Coupling Looseness
    telemetries.append({
        "filename": "telemetry_32_encoder_coupling_slippage.json",
        "title": "Encoder Shaft Flexible Coupling Set Screw Looseness",
        "subsystem": "encoder_position",
        "data": {
            "elevator_id": "KONE-MONO-532",
            "timestamp_utc": "2026-09-24T19:30:00.000Z",
            "operating_state": "ACCELERATING",
            "elevator_model": "KONE MonoSpace 500",
            "installation_age_years": 1.8,
            "alarms": [
                {"alarm_code": "position_mismatch", "alarm_type": "position_mismatch", "severity": "warning", "subsystem": "encoder_position", "timestamp": "2026-09-24T19:30:00.000Z", "state": "ACTIVE"}
            ],
            "telemetry": [
                {"signal_name": "position_actual_divergence", "value": 12.5, "unit": "mm", "quality": "good", "timestamp": "2026-09-24T19:30:00.000Z", "baseline_value": 1.0, "deviation_pct": 1150.0},
                {"signal_name": "vibration_rms", "value": 0.21, "unit": "m/s2", "quality": "good", "timestamp": "2026-09-24T19:30:00.000Z", "baseline_value": 0.08, "deviation_pct": 162.5}
            ],
            "maintenance_history": [],
            "technician_free_text": "Sudden jump in position error during upward acceleration. Set screw slipping on motor shaft."
        }
    })

    # 33. Single Floor Landing Vane Misalignment
    telemetries.append({
        "filename": "telemetry_33_encoder_single_floor_vane_misalignment.json",
        "title": "Floor 4 Leveling Vane Physical Angle Distortion",
        "subsystem": "encoder_position",
        "data": {
            "elevator_id": "KONE-MONO-533",
            "timestamp_utc": "2026-09-24T19:50:00.000Z",
            "operating_state": "DECELERATING",
            "elevator_model": "KONE MonoSpace 500",
            "installation_age_years": 4.0,
            "alarms": [
                {"alarm_code": "leveling_deviation", "alarm_type": "leveling_deviation", "severity": "warning", "subsystem": "encoder_position", "timestamp": "2026-09-24T19:50:00.000Z", "state": "ACTIVE"}
            ],
            "telemetry": [
                {"signal_name": "leveling_deviation_mm", "value": 7.8, "unit": "mm", "quality": "good", "timestamp": "2026-09-24T19:50:00.000Z", "baseline_value": 2.0, "deviation_pct": 290.0}
            ],
            "maintenance_history": [],
            "technician_free_text": "Leveling error occurs ONLY at Floor 4. All other 9 floors level with 0.5mm accuracy."
        }
    })

    # 34. Real Physical Suspension Rope Creep at Terminal Landing
    telemetries.append({
        "filename": "telemetry_34_encoder_rope_creep_leveling.json",
        "title": "High Building Thermal Rope Elongation & Floor Creep",
        "subsystem": "encoder_position",
        "data": {
            "elevator_id": "KONE-MINI-334",
            "timestamp_utc": "2026-09-24T20:10:00.000Z",
            "operating_state": "IDLE",
            "elevator_model": "KONE MiniSpace High-Rise",
            "installation_age_years": 6.2,
            "alarms": [
                {"alarm_code": "leveling_deviation", "alarm_type": "leveling_deviation", "severity": "warning", "subsystem": "encoder_position", "timestamp": "2026-09-24T20:10:00.000Z", "state": "ACTIVE"}
            ],
            "telemetry": [
                {"signal_name": "leveling_deviation_mm", "value": 6.0, "unit": "mm", "quality": "good", "timestamp": "2026-09-24T20:10:00.000Z", "baseline_value": 2.0, "deviation_pct": 200.0}
            ],
            "maintenance_history": [],
            "technician_free_text": "Both motor encoder AND independent optical sensor show car physically drifted downward 6mm under load."
        }
    })

    # 35. Guide Rail Distortion Localized at Mid-Shaft
    telemetries.append({
        "filename": "telemetry_35_encoder_guide_rail_distortion.json",
        "title": "Shaft Settlement Guide Rail Expansion Joint Binding",
        "subsystem": "encoder_position",
        "data": {
            "elevator_id": "KONE-MONO-535",
            "timestamp_utc": "2026-09-24T20:30:00.000Z",
            "operating_state": "CONSTANT_SPEED",
            "elevator_model": "KONE MonoSpace 700",
            "installation_age_years": 2.2,
            "alarms": [
                {"alarm_code": "leveling_deviation", "alarm_type": "leveling_deviation", "severity": "warning", "subsystem": "encoder_position", "timestamp": "2026-09-24T20:30:00.000Z", "state": "ACTIVE"}
            ],
            "telemetry": [
                {"signal_name": "vibration_rms", "value": 0.31, "unit": "m/s2", "quality": "good", "timestamp": "2026-09-24T20:30:00.000Z", "baseline_value": 0.08, "deviation_pct": 287.5}
            ],
            "maintenance_history": [],
            "technician_free_text": "Severe ride vibration localized specifically between 15m and 20m shaft height."
        }
    })

    # 36. Encoder Shielded Cable High-Frequency Inverter Noise
    telemetries.append({
        "filename": "telemetry_36_encoder_cable_shield_noise.json",
        "title": "Encoder Differential Pulse Noise from Inverter Ground Loop",
        "subsystem": "encoder_position",
        "data": {
            "elevator_id": "KONE-MONO-536",
            "timestamp_utc": "2026-09-24T20:50:00.000Z",
            "operating_state": "ACCELERATING",
            "elevator_model": "KONE MonoSpace 500",
            "installation_age_years": 4.1,
            "alarms": [
                {"alarm_code": "speed_feedback_error", "alarm_type": "speed_feedback_error", "severity": "warning", "subsystem": "encoder_position", "timestamp": "2026-09-24T20:50:00.000Z", "state": "ACTIVE"}
            ],
            "telemetry": [
                {"signal_name": "speed_feedback_deviation", "value": 18.5, "unit": "rpm", "quality": "good", "timestamp": "2026-09-24T20:50:00.000Z", "baseline_value": 5.0, "deviation_pct": 270.0}
            ],
            "maintenance_history": [],
            "technician_free_text": "Encoder cable shield grounding lug broken at drive cabinet chassis."
        }
    })

    # 37. Position Magnet Sensor Vane Chipping
    telemetries.append({
        "filename": "telemetry_37_encoder_position_magnet_chipped.json",
        "title": "Magnetic Hall-Effect Floor Marker Reader Distortion",
        "subsystem": "encoder_position",
        "data": {
            "elevator_id": "KONE-MONO-537",
            "timestamp_utc": "2026-09-24T21:10:00.000Z",
            "operating_state": "DECELERATING",
            "elevator_model": "KONE MonoSpace 500",
            "installation_age_years": 7.0,
            "alarms": [
                {"alarm_code": "position_mismatch", "alarm_type": "position_mismatch", "severity": "warning", "subsystem": "encoder_position", "timestamp": "2026-09-24T21:10:00.000Z", "state": "ACTIVE"}
            ],
            "telemetry": [
                {"signal_name": "position_actual_divergence", "value": 8.0, "unit": "mm", "quality": "good", "timestamp": "2026-09-24T21:10:00.000Z", "baseline_value": 1.0, "deviation_pct": 700.0}
            ],
            "maintenance_history": [],
            "technician_free_text": "Floor landing magnet strip chipped by traveling cable strike."
        }
    })

    # 38. Encoder Quad-Track Optical Grating Contamination
    telemetries.append({
        "filename": "telemetry_38_encoder_optical_disk_oil_mist.json",
        "title": "EcoDisc Encoder Glass Disk Oil Mist Contamination",
        "subsystem": "encoder_position",
        "data": {
            "elevator_id": "KONE-MONO-538",
            "timestamp_utc": "2026-09-24T21:30:00.000Z",
            "operating_state": "CONSTANT_SPEED",
            "elevator_model": "KONE MonoSpace 500",
            "installation_age_years": 8.5,
            "alarms": [
                {"alarm_code": "encoder_fault", "alarm_type": "encoder_fault", "severity": "critical", "subsystem": "encoder_position", "timestamp": "2026-09-24T21:30:00.000Z", "state": "ACTIVE"}
            ],
            "telemetry": [
                {"signal_name": "speed_feedback_deviation", "value": 19.0, "unit": "rpm", "quality": "good", "timestamp": "2026-09-24T21:30:00.000Z", "baseline_value": 5.0, "deviation_pct": 280.0}
            ],
            "maintenance_history": [],
            "technician_free_text": "Oil mist from adjacent gearless bearing seal fogged optical encoder glass disc."
        }
    })

    # 39. Missing Floor Slowdown Limit Sensor Signal
    telemetries.append({
        "filename": "telemetry_39_encoder_slowdown_limit_missed.json",
        "title": "Shaft Terminal Slowdown Limit Proximity Switch Failure",
        "subsystem": "encoder_position",
        "data": {
            "elevator_id": "KONE-MINI-339",
            "timestamp_utc": "2026-09-24T21:50:00.000Z",
            "operating_state": "DECELERATING",
            "elevator_model": "KONE MiniSpace",
            "installation_age_years": 5.8,
            "alarms": [
                {"alarm_code": "leveling_deviation", "alarm_type": "leveling_deviation", "severity": "warning", "subsystem": "encoder_position", "timestamp": "2026-09-24T21:50:00.000Z", "state": "ACTIVE"}
            ],
            "telemetry": [
                {"signal_name": "position_actual_divergence", "value": 9.5, "unit": "mm", "quality": "good", "timestamp": "2026-09-24T21:50:00.000Z", "baseline_value": 1.0, "deviation_pct": 850.0}
            ],
            "maintenance_history": [],
            "technician_free_text": "Terminal floor slowdown switch did not actuate before leveling zone entered."
        }
    })

    # 40. Leveling Error due to Car Weight Loading Sensor Drift
    telemetries.append({
        "filename": "telemetry_40_encoder_load_dependent_stopping_error.json",
        "title": "Leveling Stop Inaccuracy Dependent on Full Car Load",
        "subsystem": "encoder_position",
        "data": {
            "elevator_id": "KONE-MONO-540",
            "timestamp_utc": "2026-09-24T22:10:00.000Z",
            "operating_state": "DECELERATING",
            "elevator_model": "KONE MonoSpace 500",
            "installation_age_years": 4.5,
            "alarms": [
                {"alarm_code": "leveling_deviation", "alarm_type": "leveling_deviation", "severity": "warning", "subsystem": "encoder_position", "timestamp": "2026-09-24T22:10:00.000Z", "state": "ACTIVE"}
            ],
            "telemetry": [
                {"signal_name": "leveling_deviation_mm", "value": 8.2, "unit": "mm", "quality": "good", "timestamp": "2026-09-24T22:10:00.000Z", "baseline_value": 2.0, "deviation_pct": 310.0}
            ],
            "maintenance_history": [],
            "technician_free_text": "Stopping overshoot occurs exclusively when car is loaded >80% capacity."
        }
    })

    # =========================================================================
    # SUBSYSTEM 5: CONTROLLER / SAFETY CHAIN & SENSORS (Files 41 - 50)
    # =========================================================================

    # 41. Landing Door Lock Circuit Interruption
    telemetries.append({
        "filename": "telemetry_41_safety_door_lock_loop_break.json",
        "title": "Landing Door Interlock Contact Loop Drop During Travel",
        "subsystem": "safety_chain",
        "data": {
            "elevator_id": "KONE-MONO-541",
            "timestamp_utc": "2026-09-24T22:30:00.000Z",
            "operating_state": "CONSTANT_SPEED",
            "elevator_model": "KONE MonoSpace 500",
            "installation_age_years": 5.0,
            "alarms": [
                {"alarm_code": "safety_chain_open", "alarm_type": "safety_chain_open", "severity": "critical", "subsystem": "safety_chain", "timestamp": "2026-09-24T22:30:00.000Z", "state": "ACTIVE"},
                {"alarm_code": "drive_trip", "alarm_type": "drive_trip", "severity": "critical", "subsystem": "drive_motor", "timestamp": "2026-09-24T22:30:00.150Z", "state": "ACTIVE"}
            ],
            "telemetry": [
                {"signal_name": "motor_current_rms", "value": 0.0, "unit": "A", "quality": "good", "timestamp": "2026-09-24T22:30:00.000Z", "baseline_value": 12.0, "deviation_pct": -100.0}
            ],
            "maintenance_history": [],
            "technician_free_text": "Landing door gate lock contact on Floor 3 opened mid-travel due to door gib play."
        }
    })

    # 42. Terminal Buffer Limit Switch Trip
    telemetries.append({
        "filename": "telemetry_42_safety_pit_buffer_switch_actuation.json",
        "title": "Pit Oil Buffer Final Limit Switch Electrical Contact Trip",
        "subsystem": "safety_chain",
        "data": {
            "elevator_id": "KONE-MONO-542",
            "timestamp_utc": "2026-09-24T22:50:00.000Z",
            "operating_state": "FAULT_STOP",
            "elevator_model": "KONE MonoSpace 500",
            "installation_age_years": 6.5,
            "alarms": [
                {"alarm_code": "buffer_activation", "alarm_type": "buffer_activation", "severity": "critical", "subsystem": "safety_chain", "timestamp": "2026-09-24T22:50:00.000Z", "state": "ACTIVE"},
                {"alarm_code": "safety_chain_open", "alarm_type": "safety_chain_open", "severity": "critical", "subsystem": "safety_chain", "timestamp": "2026-09-24T22:50:00.100Z", "state": "ACTIVE"}
            ],
            "telemetry": [],
            "maintenance_history": [],
            "technician_free_text": "Elevator traveled past bottom terminal landing and depressed pit buffer switch."
        }
    })

    # 43. Emergency Stop Pushbutton Actuation
    telemetries.append({
        "filename": "telemetry_43_safety_estop_button_activated.json",
        "title": "Car Operating Panel Manual Emergency Stop Switch Activated",
        "subsystem": "safety_chain",
        "data": {
            "elevator_id": "KONE-MONO-543",
            "timestamp_utc": "2026-09-24T23:10:00.000Z",
            "operating_state": "CONSTANT_SPEED",
            "elevator_model": "KONE MonoSpace 500",
            "installation_age_years": 1.5,
            "alarms": [
                {"alarm_code": "emergency_stop_activated", "alarm_type": "emergency_stop_activated", "severity": "critical", "subsystem": "safety_chain", "timestamp": "2026-09-24T23:10:00.000Z", "state": "ACTIVE"},
                {"alarm_code": "safety_chain_open", "alarm_type": "safety_chain_open", "severity": "critical", "subsystem": "safety_chain", "timestamp": "2026-09-24T23:10:00.050Z", "state": "ACTIVE"}
            ],
            "telemetry": [],
            "maintenance_history": [],
            "technician_free_text": "Manual red e-stop pushbutton depressed on in-car panel."
        }
    })

    # 44. Safety Relay Coil Thermal Degradation & Contact Bounce
    telemetries.append({
        "filename": "telemetry_44_safety_relay_contact_bounce.json",
        "title": "Main Safety Relay Armature Chatter & Intermittent Tripping",
        "subsystem": "safety_chain",
        "data": {
            "elevator_id": "KONE-MONO-544",
            "timestamp_utc": "2026-09-24T23:30:00.000Z",
            "operating_state": "ACCELERATING",
            "elevator_model": "KONE MonoSpace 500",
            "installation_age_years": 10.5,
            "alarms": [
                {"alarm_code": "safety_circuit_trip", "alarm_type": "safety_circuit_trip", "severity": "critical", "subsystem": "safety_chain", "timestamp": "2026-09-24T23:30:00.000Z", "state": "ACTIVE"}
            ],
            "telemetry": [
                {"signal_name": "safety_chain_flicker_count", "value": 8.0, "unit": "count", "quality": "good", "timestamp": "2026-09-24T23:30:00.000Z", "baseline_value": 0.0, "deviation_pct": 800.0}
            ],
            "maintenance_history": [],
            "technician_free_text": "Safety relay coil warm. Contact resistance jumping between 0.5 ohm and open circuit."
        }
    })

    # 45. Controller CPU Watchdog Hardware Reset
    telemetries.append({
        "filename": "telemetry_45_controller_cpu_watchdog_reboot.json",
        "title": "Main Logic Board CPU Watchdog Reset & Bus Hang",
        "subsystem": "safety_chain",
        "data": {
            "elevator_id": "KONE-MONO-545",
            "timestamp_utc": "2026-09-24T23:50:00.000Z",
            "operating_state": "CONSTANT_SPEED",
            "elevator_model": "KONE MonoSpace 500",
            "installation_age_years": 7.2,
            "alarms": [
                {"alarm_code": "safety_chain_open", "alarm_type": "safety_chain_open", "severity": "critical", "subsystem": "safety_chain", "timestamp": "2026-09-24T23:50:00.000Z", "state": "ACTIVE"}
            ],
            "telemetry": [
                {"signal_name": "controller_reboot_count", "value": 4.0, "unit": "count", "quality": "good", "timestamp": "2026-09-24T23:50:00.000Z", "baseline_value": 0.0, "deviation_pct": 400.0}
            ],
            "maintenance_history": [],
            "technician_free_text": "Controller processor reset due to power supply 5V rail noise burst."
        }
    })

    # 46. Load Cell Miscalibration (Nuisance Overload Alarm)
    telemetries.append({
        "filename": "telemetry_46_sensor_load_cell_miscalibration.json",
        "title": "Car Bottom Load Weighing Sensor Gain Offset & Nuisance Hold",
        "subsystem": "sensor_env",
        "data": {
            "elevator_id": "KONE-MONO-546",
            "timestamp_utc": "2026-09-25T00:10:00.000Z",
            "operating_state": "DOOR_OPEN",
            "elevator_model": "KONE MonoSpace 500",
            "installation_age_years": 3.0,
            "alarms": [
                {"alarm_code": "sensor_implausible_reading", "alarm_type": "sensor_implausible_reading", "severity": "warning", "subsystem": "sensor_env", "timestamp": "2026-09-25T00:10:00.000Z", "state": "ACTIVE"}
            ],
            "telemetry": [
                {"signal_name": "load_measurement_deviation", "value": 420.0, "unit": "kg", "quality": "good", "timestamp": "2026-09-25T00:10:00.000Z", "baseline_value": 0.0, "deviation_pct": 420.0}
            ],
            "maintenance_history": [],
            "technician_free_text": "Elevator indicates 110% overload holding doors open with only 1 passenger inside."
        }
    })

    # 47. Machine Room Thermal Runaway / Environmental Overheat
    telemetries.append({
        "filename": "telemetry_47_sensor_machine_room_thermal_stress.json",
        "title": "Machine Room HVAC Outage & 54°C Ambient Overheat",
        "subsystem": "sensor_env",
        "data": {
            "elevator_id": "KONE-MINI-347",
            "timestamp_utc": "2026-09-25T00:30:00.000Z",
            "operating_state": "CONSTANT_SPEED",
            "elevator_model": "KONE MiniSpace",
            "installation_age_years": 4.5,
            "alarms": [
                {"alarm_code": "motor_overheat", "alarm_type": "motor_overheat", "severity": "warning", "subsystem": "drive_motor", "timestamp": "2026-09-25T00:30:00.000Z", "state": "ACTIVE"}
            ],
            "telemetry": [
                {"signal_name": "machine_room_temp_c", "value": 54.0, "unit": "°C", "quality": "good", "timestamp": "2026-09-25T00:30:00.000Z", "baseline_value": 24.0, "deviation_pct": 125.0},
                {"signal_name": "motor_temp", "value": 78.0, "unit": "°C", "quality": "good", "timestamp": "2026-09-25T00:30:00.000Z", "baseline_value": 50.0, "deviation_pct": 56.0}
            ],
            "maintenance_history": [],
            "technician_free_text": "Machine room air conditioner breaker tripped. Ambient room temperature reached 54°C."
        }
    })

    # 48. Accelerometer Vibration Sensor Mechanical Rattle
    telemetries.append({
        "filename": "telemetry_48_sensor_accelerometer_mount_loose.json",
        "title": "Ride Quality Sensor Bracket Looseness & Spurious Noise",
        "subsystem": "sensor_env",
        "data": {
            "elevator_id": "KONE-MONO-548",
            "timestamp_utc": "2026-09-25T00:50:00.000Z",
            "operating_state": "CONSTANT_SPEED",
            "elevator_model": "KONE MonoSpace 500",
            "installation_age_years": 5.0,
            "alarms": [
                {"alarm_code": "sensor_implausible_reading", "alarm_type": "sensor_implausible_reading", "severity": "warning", "subsystem": "sensor_env", "timestamp": "2026-09-25T00:50:00.000Z", "state": "ACTIVE"}
            ],
            "telemetry": [
                {"signal_name": "sensor_signal_noise", "value": 4.5, "unit": "V", "quality": "good", "timestamp": "2026-09-25T00:50:00.000Z", "baseline_value": 0.1, "deviation_pct": 4400.0}
            ],
            "maintenance_history": [],
            "technician_free_text": "Accelerometer bracket mounting screw loose on car crosshead, causing high noise spikes."
        }
    })

    # 49. Hall-Effect Current Sensor Baseline Offset Drift
    telemetries.append({
        "filename": "telemetry_49_sensor_current_transducer_drift.json",
        "title": "Motor Phase Current Shunt Sensor Zero-Point Drift",
        "subsystem": "sensor_env",
        "data": {
            "elevator_id": "KONE-MONO-549",
            "timestamp_utc": "2026-09-25T01:10:00.000Z",
            "operating_state": "IDLE",
            "elevator_model": "KONE MonoSpace 500",
            "installation_age_years": 6.8,
            "alarms": [
                {"alarm_code": "sensor_implausible_reading", "alarm_type": "sensor_implausible_reading", "severity": "warning", "subsystem": "sensor_env", "timestamp": "2026-09-25T01:10:00.000Z", "state": "ACTIVE"}
            ],
            "telemetry": [
                {"signal_name": "motor_current_rms", "value": 6.8, "unit": "A", "quality": "good", "timestamp": "2026-09-25T01:10:00.000Z", "baseline_value": 0.0, "deviation_pct": 680.0}
            ],
            "maintenance_history": [],
            "technician_free_text": "Current sensor reports 6.8A flowing while main contactors are open and motor stationary."
        }
    })

    # 50. Conflicting Multi-Sensor Degradation (Principled Abstention Benchmark)
    telemetries.append({
        "filename": "telemetry_50_sensor_conflicting_ambiguity_abstain.json",
        "title": "Degraded Multi-Rate Telemetry & Conflicting Diagnostic Signature",
        "subsystem": "sensor_env",
        "data": {
            "elevator_id": "KONE-MONO-550",
            "timestamp_utc": "2026-09-25T01:30:00.000Z",
            "operating_state": "CONSTANT_SPEED",
            "elevator_model": "KONE MonoSpace 500",
            "installation_age_years": 8.0,
            "alarms": [
                {"alarm_code": "motor_overcurrent", "alarm_type": "motor_overcurrent", "severity": "warning", "subsystem": "drive_motor", "timestamp": "2026-09-25T01:30:00.000Z", "state": "ACTIVE"}
            ],
            "telemetry": [
                {"signal_name": "motor_current_rms", "value": 14.2, "unit": "A", "quality": "good", "timestamp": "2026-09-25T01:30:00.000Z", "baseline_value": 12.0, "deviation_pct": 18.3},
                {"signal_name": "igbt_temp", "value": 0.0, "unit": "°C", "quality": "bad", "timestamp": "2026-09-25T01:30:00.000Z", "baseline_value": 45.0, "deviation_pct": 0.0},
                {"signal_name": "motor_temp", "value": 0.0, "unit": "°C", "quality": "missing", "timestamp": "2026-09-25T01:30:00.000Z", "baseline_value": 50.0, "deviation_pct": 0.0},
                {"signal_name": "vibration_rms", "value": 0.08, "unit": "m/s2", "quality": "good", "timestamp": "2026-09-25T01:30:00.000Z", "baseline_value": 0.08, "deviation_pct": 0.0},
                {"signal_name": "brake_release_delay", "value": 150.0, "unit": "ms", "quality": "good", "timestamp": "2026-09-25T01:30:00.000Z", "baseline_value": 150.0, "deviation_pct": 0.0}
            ],
            "maintenance_history": [],
            "technician_free_text": "Conflicting telemetry: mild current bump with normal vibration and passing drive self-test. Multiple temperature channels offline."
        }
    })

    # Write all 50 files
    catalog = []
    for item in telemetries:
        filepath = os.path.join("sample_telemetry", item["filename"])
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(item["data"], f, indent=2)
        catalog.append({
            "filename": item["filename"],
            "title": item["title"],
            "subsystem": item["subsystem"],
            "elevator_id": item["data"]["elevator_id"],
            "model": item["data"]["elevator_model"]
        })

    # Write catalog index
    with open("sample_telemetry/TELEMETRY_CATALOG.json", "w", encoding="utf-8") as f:
        json.dump(catalog, f, indent=2)

    # Write Markdown Catalog
    with open("sample_telemetry/README.md", "w", encoding="utf-8") as f:
        f.write("# KONE Elevate — 50 Canonical Telemetry Datasets Catalog\n\n")
        f.write("Directly aligned with the 15-page KONE Elevate Five-Subsystem Fault Dictionary.\n\n")
        f.write("| # | File | Subsystem | Fault / Phenomenon Description |\n")
        f.write("|---|---|---|---|\n")
        for i, c in enumerate(catalog, 1):
            f.write(f"| {i:02d} | [`{c['filename']}`]({c['filename']}) | `{c['subsystem']}` | {c['title']} ({c['elevator_id']}) |\n")

    print(f"Successfully generated all {len(telemetries)} structured telemetry files in sample_telemetry/")


if __name__ == "__main__":
    generate_all_50()
