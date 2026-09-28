"""
ElevateRCA — Interactive CLI Scenario Demonstration
Executes all 5 Canonical Fault Scenarios + Scenario 6 Abstention Benchmark
with full 5-stage explainability trace output.
"""

import sys
import json
import time

# Ensure UTF-8 stdout encoding on Windows
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from pipeline.engine import ElevateRCAEngine
from simulator.scenarios import ScenarioFactory


def print_banner(title: str):
    print("\n" + "=" * 78)
    print(f"  {title.upper()}")
    print("=" * 78)


def run_and_display_scenario(scenario_func, name: str, description: str, engine: ElevateRCAEngine):
    print_banner(f"RUNNING: {name}")
    print(f"Pattern & Context: {description}\n")

    input_payload = scenario_func()
    print(f"Asset ID:         {input_payload.elevator_id} ({input_payload.elevator_model or 'KONE MonoSpace'})")
    print(f"Operating State:  {input_payload.operating_state}")
    print(f"Alarms Triggered: {[f'{a.alarm_code} ({a.subsystem})' for a in input_payload.alarms]}")
    print(f"Telemetry Signals: {[f'{t.signal_name}={t.value}{t.unit}' for t in input_payload.telemetry]}")
    if input_payload.technician_free_text:
        print(f"Technician Note:  \"{input_payload.technician_free_text}\"")

    print("\n" + "-" * 35 + " [EXECUTING 5-STAGE PIPELINE] " + "-" * 35)
    start_time = time.perf_counter()
    trace = engine.analyze(input_payload)
    elapsed_ms = (time.perf_counter() - start_time) * 1000

    # STAGE 2: Alarm Cascade
    print("\n[>] STAGE 2: ALARM CASCADE CORRELATION")
    print(f"  * Primary Trigger:       {trace.fault_episode.primary_alarm.alarm_code} [{trace.fault_episode.primary_alarm.subsystem}]")
    print(f"  * Time Span:             {trace.fault_episode.time_span_seconds:.2f}s")
    print(f"  * Consequential Alarms:  {len(trace.fault_episode.consequential_alarms)}")
    for c in trace.fault_episode.consequential_alarms:
        print(f"    - {c.alarm_code}: {c.causal_relationship}")

    # STAGE 4: Bayesian Ranking
    print("\n[>] STAGE 4: BAYESIAN MULTI-HYPOTHESIS RANKING")
    for h in trace.hypotheses:
        prob_bar = "#" * int(h.posterior_probability * 25) + "." * (25 - int(h.posterior_probability * 25))
        status_flag = f"[{h.status}]"
        print(f"  Rank #{h.rank} {status_flag:<18} [{prob_bar}] {h.posterior_probability*100:4.1f}% | {h.hypothesis_id}: {h.root_cause}")
        if h.supporting_evidence:
            print(f"     [+] Supporting: {'; '.join([s.evidence for s in h.supporting_evidence])}")
        if h.contradicting_evidence:
            print(f"     [-] Contradicting: {'; '.join([c.evidence for c in h.contradicting_evidence])}")
        if h.eliminated_reason:
            print(f"     [x] Eliminated Reason: {h.eliminated_reason}")

    # STAGE 5: Synthesis & Decision
    print("\n[>] STAGE 5: DUAL CONFIDENCE & SYNTHESIS")
    print(f"  * Root Cause Winner:     {trace.rca_conclusion.root_cause}")
    print(f"  * Root Cause Confidence: {trace.rca_conclusion.root_cause_confidence*100:.1f}% ({trace.rca_conclusion.root_cause_confidence_tier})")
    print(f"  * Action Confidence:     {trace.rca_conclusion.action_confidence*100:.1f}% ({trace.rca_conclusion.action_confidence_tier})")
    print(f"  * Abstained:             {trace.rca_conclusion.abstained}")
    print(f"\n  [Causal Narrative]:\n  {trace.rca_conclusion.causal_narrative}")

    # Views
    print("\n[>] TECHNICIAN DIAGNOSTIC VIEW (OEM SOP)")
    print(f"  * Recommended Action:    {trace.corrective_recommendation.recommended_action} ({trace.corrective_recommendation.estimated_severity} SEVERITY)")
    print("  * Mandatory Steps:")
    for step in trace.corrective_recommendation.specific_steps[:3]:
        print(f"    [ ] {step}")
    print("  * Prohibited (DO NOT DO):")
    for d in trace.corrective_recommendation.do_not_do:
        print(f"    [!] {d}")

    print("\n[>] BUILDING MANAGER VIEW")
    print(f"  * Summary:           {trace.building_manager_view.summary}")
    print(f"  * Expected Downtime: {trace.building_manager_view.expected_downtime}")
    print(f"  * Safety Status:     {trace.building_manager_view.safety_status}")

    print(f"\nCompleted in {elapsed_ms:.2f} ms")


def main():
    engine = ElevateRCAEngine(
        failure_modes_path="knowledge/failure_modes.yaml",
        causal_links_path="knowledge/causal_links.yaml",
        corrective_actions_path="knowledge/corrective_actions.yaml"
    )

    scenarios = [
        (
            ScenarioFactory.scenario_1_igbt_overcurrent,
            "Scenario 1: IGBT Power Electronics Failure",
            "motor_current step spike +136.7%, igbt_temp elevated, drive self-test FAILED"
        ),
        (
            ScenarioFactory.scenario_2_mechanical_jam,
            "Scenario 2: Hoistway / Guide Rail Mechanical Jam",
            "motor_current +90%, vibration +250%, motor_temp elevated, drive self-test PASSED"
        ),
        (
            ScenarioFactory.scenario_3_door_photoeye_drift,
            "Scenario 3: Door 3D Light Curtain Optical Drift",
            "door_cycle_time +58.9%, recurring reopens at varying door positions"
        ),
        (
            ScenarioFactory.scenario_4_encoder_fault,
            "Scenario 4: EcoDisc Motor Encoder Pulse Loss",
            "Leveling deviation +325%, position divergence +580%, independent sensor normal"
        ),
        (
            ScenarioFactory.scenario_5_brake_drag_timing,
            "Scenario 5: EcoDisc Brake Release Timing Violation",
            "Brake release delay 360ms (+140%), normal motor torque demand, position drift"
        ),
        (
            ScenarioFactory.scenario_6_abstention_conflicting,
            "Scenario 6: Principled Abstention Benchmark",
            "Conflicting signals, normal brake & vibration, bad/missing temperature sensors"
        )
    ]

    print_banner("ELEVATERCA - 6 CANONICAL SCENARIO EXECUTION SUITE")
    print("Read-Only Advisory Intelligence Layer for KONE MonoSpace / MiniSpace Elevators")

    for scenario_func, name, desc in scenarios:
        run_and_display_scenario(scenario_func, name, desc, engine)

    print("\n" + "=" * 78)
    print("  ALL 6 CANONICAL SCENARIOS EVALUATED SUCCESSFULLY")
    print("  [!] HUMAN VERIFICATION REQUIRED -- Advisory only.")
    print("=" * 78 + "\n")


if __name__ == "__main__":
    main()
