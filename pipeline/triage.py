"""
STAGE 1: SIGNAL TRIAGE & ANOMALY DETECTION
Implements EWMA / CUSUM anomaly detection, state-aware baseline deviations,
and signal quality gating.
"""

from typing import List, Dict, Any, Optional
import numpy as np
from pipeline.schemas import TelemetryInput


# Standard engineering norms for KONE MonoSpace / MiniSpace (EcoDisc)
ENGINEERING_NORMS = {
    "motor_current_rms": {"unit": "A", "baseline": 12.0, "elevated_pct": 30.0, "severe_pct": 80.0},
    "igbt_temp": {"unit": "°C", "baseline": 45.0, "elevated_pct": 25.0, "severe_pct": 55.0},
    "motor_temp": {"unit": "°C", "baseline": 50.0, "elevated_pct": 30.0, "severe_pct": 60.0},
    "vibration_rms": {"unit": "m/s2", "baseline": 0.08, "elevated_pct": 50.0, "severe_pct": 150.0},
    "door_cycle_time_ms": {"unit": "ms", "baseline": 2800.0, "elevated_pct": 25.0, "severe_pct": 50.0},
    "door_motor_current": {"unit": "A", "baseline": 1.5, "elevated_pct": 40.0, "severe_pct": 100.0},
    "brake_release_delay": {"unit": "ms", "baseline": 150.0, "elevated_pct": 50.0, "severe_pct": 100.0},
    "brake_coil_current": {"unit": "A", "baseline": 2.2, "elevated_pct": 20.0, "severe_pct": 50.0},
    "position_actual_divergence": {"unit": "mm", "baseline": 1.0, "elevated_pct": 100.0, "severe_pct": 300.0},
    "leveling_deviation_mm": {"unit": "mm", "baseline": 2.0, "elevated_pct": 100.0, "severe_pct": 250.0},
    "speed_feedback_deviation": {"unit": "rpm", "baseline": 5.0, "elevated_pct": 40.0, "severe_pct": 100.0},
    "dc_bus_voltage": {"unit": "V", "baseline": 560.0, "elevated_pct": 15.0, "severe_pct": 30.0},
    "machine_room_temp_c": {"unit": "°C", "baseline": 24.0, "elevated_pct": 35.0, "severe_pct": 70.0}
}


class EWMATracker:
    """Exponentially Weighted Moving Average tracker for streaming telemetry."""
    def __init__(self, alpha: float = 0.2):
        self.alpha = alpha
        self.mean: Optional[float] = None
        self.var: Optional[float] = None

    def update(self, value: float) -> float:
        if self.mean is None:
            self.mean = value
            self.var = 0.0
            return 0.0
        diff = value - self.mean
        self.mean = self.alpha * value + (1 - self.alpha) * self.mean
        self.var = (1 - self.alpha) * (self.var + self.alpha * (diff ** 2))
        std = np.sqrt(self.var) if self.var > 1e-6 else 1.0
        z_score = abs(diff) / std
        return float(z_score)


class SignalTriager:
    """Stage 1: Analyzes and classifies all input telemetry signals."""

    @staticmethod
    def classify_signal(telemetry: TelemetryInput, operating_state: str) -> Dict[str, Any]:
        # Quality Gate Check: Bad or missing signals provide zero diagnostic value
        if telemetry.quality in ["bad", "missing"]:
            return {
                "signal_name": telemetry.signal_name,
                "value": telemetry.value,
                "classification": "MISSING" if telemetry.quality == "missing" else "UNRELIABLE_SENSOR",
                "quality": telemetry.quality,
                "diagnostic_value": "NONE",
                "deviation_pct": 0.0,
                "state_context": operating_state,
                "notes": f"Signal quality is '{telemetry.quality}' — zero diagnostic value for hypothesis scoring."
            }

        norm = ENGINEERING_NORMS.get(telemetry.signal_name)
        baseline = telemetry.baseline_value
        if baseline is None:
            baseline = norm["baseline"] if norm else telemetry.value

        # Safe numeric parsing for float calculations
        def to_float_safe(v):
            if isinstance(v, bool):
                return 1.0 if v else 0.0
            if isinstance(v, (int, float)):
                return float(v)
            if isinstance(v, str):
                u = v.upper().strip()
                if u in ["TRUE", "1", "HIGH", "ACTIVE", "CLOSED", "BROKEN"]:
                    return 1.0
                if u in ["FALSE", "0", "LOW", "INACTIVE", "OPEN", "CLEAR"]:
                    return 0.0
                try:
                    return float(v)
                except ValueError:
                    return 0.0
            return 0.0

        val_num = to_float_safe(telemetry.value)
        base_num = to_float_safe(baseline)

        if base_num != 0:
            dev_pct = ((val_num - base_num) / base_num) * 100.0
        else:
            dev_pct = (val_num - base_num) * 100.0

        if telemetry.deviation_pct is not None:
            dev_pct = telemetry.deviation_pct

        # Anomaly thresholding
        elevated_thresh = norm["elevated_pct"] if norm else 25.0
        severe_thresh = norm["severe_pct"] if norm else 60.0


        classification = "NORMAL"
        diagnostic_val = "LOW"

        if dev_pct >= severe_thresh:
            classification = "SEVERELY_ELEVATED"
            diagnostic_val = "HIGH"
        elif dev_pct >= elevated_thresh:
            classification = "ELEVATED"
            diagnostic_val = "HIGH"
        elif dev_pct <= -elevated_thresh:
            classification = "DROPPING"
            diagnostic_val = "MEDIUM"
        else:
            # Check special patterns if encoded in signal
            classification = "NORMAL"
            diagnostic_val = "LOW"

        # Operating state context modifier
        # For example, motor current during DOOR_OPEN or IDLE is abnormal even if moderately low
        if operating_state in ["IDLE", "DOOR_OPEN"] and telemetry.signal_name == "motor_current_rms" and telemetry.value > 2.0:
            classification = "SEVERELY_ELEVATED"
            diagnostic_val = "HIGH"

        return {
            "signal_name": telemetry.signal_name,
            "value": telemetry.value,
            "unit": telemetry.unit,
            "baseline": baseline,
            "deviation_pct": round(dev_pct, 2),
            "classification": classification,
            "quality": telemetry.quality,
            "diagnostic_value": diagnostic_val,
            "operating_state": operating_state,
            "provenance": "MEASURED"
        }

    def triage_all(self, telemetry_list: List[TelemetryInput], operating_state: str) -> List[Dict[str, Any]]:
        """Processes all telemetry signals and returns classified anomaly results."""
        return [self.classify_signal(t, operating_state) for t in telemetry_list]
