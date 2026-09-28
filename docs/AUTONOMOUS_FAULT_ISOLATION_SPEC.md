# Autonomous Fault Isolation and Root Cause Analysis (RCA) Assistant
## Technical Architecture, Theoretical Foundations & System Specification

---

### 1. Executive Summary & Problem Formulation

Modern elevator systems (such as **KONE MonoSpace / MiniSpace** with **EcoDisc PMSM** gearless drives) are complex cyber-physical machines. When an electromechanical or sensory anomaly occurs, the controller generates **cascading alarm floods**, where a single primary physical fault triggers 3 to 5 consequential secondary alarms across adjacent subsystems (e.g., *Motor Overcurrent* $\rightarrow$ *Drive Protective Trip* $\rightarrow$ *Leveling Deviation* $\rightarrow$ *Safety Chain Drop*).

Traditional diagnostic approaches treat alarms independently or rely on simple rule-based lookups, leading to:
1. **Symptom Treatment & Misdiagnosis**: Replacing consequential parts (e.g., boards or leveling switches) while the root cause remains unresolved.
2. **Extended Mean Time to Repair (MTTR)** and unnecessary component replacement costs.
3. **High Callback Rates** due to unisolated intermittent faults.

**ElevateRCA** is an autonomous, evidence-driven Fault Isolation and Root Cause Analysis Assistant designed to ingest raw telemetry and alarm streams, isolate the primary physical failure mode across a multi-hypothesis Bayesian space, eliminate alternative causes using negative evidence, and generate auditable diagnostic work orders.

```
                  ┌──────────────────────────────────────────────────────────┐
                  │                 RAW ELEVATOR INPUT DATA                  │
                  │   • Multi-Rate Telemetry (Current, Temp, Vibration, etc.)│
                  │   • Controller Alarms (Timestamped Cascade Events)       │
                  │   • Historical Maintenance Records & Operating State     │
                  └─────────────────────────────┬────────────────────────────┘
                                                │
                                                ▼
 ┌──────────────────────────────────────────────────────────────────────────────────────────────┐
 │                              5-STAGE RCA REASONING PIPELINE                                  │
 │                                                                                              │
 │  ┌─────────────────────────┐      ┌─────────────────────────┐      ┌──────────────────────┐  │
 │  │ STAGE 1: SIGNAL TRIAGE  │ ───► │ STAGE 2: ALARM CASCADE  │ ───► │ STAGE 3: EVIDENCE    │  │
 │  │ • EWMA / CUSUM Anomaly  │      │ • ISA-18.2 15s Window   │      │   BUNDLE ASSEMBLY    │  │
 │  │ • State Contextualizing │      │ • Causal Graph Splitting│      │ • Provenance Tagging │  │
 │  │ • Sensor Quality Gating │      │ • Primary vs Secondary  │      │ • Pos/Neg Tagging    │  │
 │  └─────────────────────────┘      └─────────────────────────┘      └──────────┬───────────┘  │
 │                                                                               │              │
 │                                                                               ▼              │
 │  ┌──────────────────────────────────────────────────────────┐      ┌──────────────────────┐  │
 │  │ STAGE 5: SYNTHESIS & DUAL CONFIDENCE                     │ ◄─── │ STAGE 4: BAYESIAN    │  │
 │  │ • root_cause_confidence & action_confidence              │      │   FAULT TREE RANKING │  │
 │  │ • Calibrated Tiers: HIGH (≥0.75), MEDIUM, LOW, ABSTAIN   │      │ • 6-Subsystem Trees  │  │
 │  │ • Dual View: Technician Work Order + Manager Summary     │      │ • 4-Step Q1-Q4 Logic │  │
 │  │ • Approved OEM SOP Lookup Table (Zero Invented Actions)  │      │ • True Negative Rules│  │
 │  └──────────────────────────────────────────────────────────┘      └──────────────────────┘  │
 └──────────────────────────────────────────────┬───────────────────────────────────────────────┘
                                                │
                                                ▼
 ┌──────────────────────────────────────────────────────────────────────────────────────────────┐
 │                                   OUTPUT ARTIFACTS                                           │
 │   1. Auditable ExplainabilityTrace JSON (Full Provenance Trail)                              │
 │   2. Interactive Technician Work Order (OEM SOP Checklist & Prohibited Actions)               │
 │   3. Facility Operations Summary (Downtime Forecast & Hardware Safety Guarantee)             │
 │   4. Human-In-The-Loop Audit Ledger (Digital Sign-off & Historical Traceability)             │
 └──────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

### 2. Core Scientific Differentiators

| Dimension | Industry Standard (Level 2-3) | ElevateRCA Autonomous Assistant (Level 5-6) |
| :--- | :--- | :--- |
| **Alarm Flood Handling** | Isolated alarm alerts; treats every alarm as an independent event. | **ISA-18.2 Causal Clustering**: Reconstructs physical cascade topology to isolate the single root trigger. |
| **Hypothesis Space** | Single heuristic guess or top-1 statistical match. | **Multi-Hypothesis Bayesian Network**: Evaluates 6 to 9 competing physical failure modes simultaneously. |
| **Negative Evidence** | Only searches for positive matches; ignores contradictory readings. | **True Negative Elimination**: Explicitly uses normal readings (e.g. passing self-test) to eliminate competing causes. |
| **Confidence Scoring** | Uncalibrated / arbitrary score or binary classification. | **Calibrated Dual Confidence**: Separates diagnostic certainty from action certainty with principled abstention. |
| **Auditability** | Black-box output with no provenance. | **ExplainabilityTrace**: Every claim is cited with provenance (`[MEASURED]`, `[LOGGED]`, `[HISTORICAL]`). |

---

### 3. Subsystem Fault Trees & Mathematical Formulation

ElevateRCA models failure mechanisms across 6 elevator subsystems:
1. **Drive / Motor Subsystem** (`drive_motor`): IGBT breakdown, mechanical hoistway jam, brake drag, motor winding insulation failure, cable faults, VFD parameter drift, traction rope slip.
2. **Door Operator Subsystem** (`door`): 3D light curtain optical degradation, sill debris obstruction, hanger roller wear, operator motor degradation, interlock contact bounce.
3. **Brake & Traction Subsystem** (`brake_traction`): Brake release timing delay, friction lining wear, actuator solenoid breakdown, traction rope elongation.
4. **Encoder & Position Subsystem** (`encoder_position`): Optical encoder pulse loss/contamination, mounting looseness, floor leveling vane misalignment, physical rope creep.
5. **Safety Chain Subsystem** (`safety_chain`): Landing door interlock break, terminal buffer switch trip, overspeed governor contact, emergency stop button.
6. **Sensor & Environmental Subsystem** (`sensor_env`): Current sensor drift, machine room thermal stress, vibration-induced wiring disconnect.

#### Bayesian Posterior Calculation:
Given evidence vector $\mathbf{E} = \{e_1, e_2, \dots, e_m\}$ and competing hypotheses $H_i \in \{H_1, \dots, H_n\}$:

$$P(H_i \mid \mathbf{E}) = \frac{P(H_i) \prod_{j=1}^{m} P(e_j \mid H_i)}{\sum_{k=1}^{n} P(H_k) \prod_{j=1}^{m} P(e_j \mid H_k)}$$

Where:
- $P(H_i)$ is the domain prior probability derived from OEM FMEA failure tables.
- $P(e_j \mid H_i)$ represents the likelihood of observing telemetry feature $e_j$ under hypothesis $H_i$.
- Negative evidence (e.g., $e_j = \text{NORMAL}$ when $H_i$ requires $\text{SEVERELY\_ELEVATED}$) heavily penalizes the likelihood ($P(e_j \mid H_i) \le 0.05$), eliminating $H_i$.

---

### 4. Verification Benchmarks across 6 Canonical Scenarios

```
Scenario 1: IGBT Inverter Breakdown      --> Ranked #1: RC1 (97.0% Posterior, HIGH Confidence)
Scenario 2: Hoistway Guide Rail Jam      --> Ranked #1: RC2 (78.0% Posterior, HIGH Confidence)
Scenario 3: Door Light Curtain Drift     --> Ranked #1: RC1 (64.0% Posterior, MEDIUM Confidence)
Scenario 4: Encoder Pulse Loss           --> Ranked #1: RC1 (74.0% Posterior, HIGH Confidence)
Scenario 5: Brake Lift Timing Delay      --> Ranked #1: RC1 (75.0% Posterior, HIGH Confidence)
Scenario 6: Sensor Ambiguity / Degraded  --> Principled Abstention (32.0% Posterior, ABSTAIN Tier)
```

---

### 5. Production REST API Endpoints

- `GET  /api/v1/incidents`: Active fleet incident queue with asset IDs, locations, and severities.
- `POST /api/v1/incidents/{incident_id}/analyze`: Analyzes active incident through the 5-stage pipeline.
- `POST /api/v1/analyze`: Ingests custom/uploaded raw KONE elevator software JSON output.
- `POST /api/v1/human-review`: Records digital technician verification and commits to the audit log.
- `GET  /api/v1/audit-log`: Retrieves complete audit log history.
