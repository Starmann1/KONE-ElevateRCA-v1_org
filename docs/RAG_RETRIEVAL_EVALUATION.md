# ElevateRCA RAG Retrieval Evaluation & Benchmarking

## 1. Evaluation Methodology

The RAG subsystem is evaluated across 5 core dimensions:
1. **Subsystem Precision:** Percentage of retrieved sources directly relevant to the active subsystem.
2. **Authority Alignment:** Priority ranking respecting the 5-tier document authority hierarchy.
3. **Configuration Accuracy:** Correct filtering and applicability tagging for configuration-constrained documents (`SETS / EGOV`).
4. **Latency Benchmarks:** Query execution time on standard CPU hardware.
5. **Bayesian Invariant Integrity:** Demonstration that RAG augmentation does not distort Bayesian posterior probabilities.

---

## 2. Benchmark Results

### 2.1 Latency Performance
| Operation | Target | Measured Result | Status |
|---|---|---|---|
| Vector Store Query (Cached Model) | $< 250\text{ ms}$ | **$100\text{ ms} - 170\text{ ms}$** | **PASS** |
| Keyword Search (`collection.get`) | $< 50\text{ ms}$ | **$8\text{ ms} - 15\text{ ms}$** | **PASS** |
| End-to-End Hybrid Retrieval | $< 500\text{ ms}$ | **$120\text{ ms} - 190\text{ ms}$** | **PASS** |
| Full 5-Stage RCA Pipeline Run | $< 1000\text{ ms}$ | **$210\text{ ms} - 350\text{ ms}$** | **PASS** |
| 25-Test Automated Verification Suite | $< 60\text{ s}$ | **$27.58\text{ s}$** | **PASS** |

### 2.2 Subsystem Retrieval Precision
| Subsystem Query | Top Retrieved Source | Authority Level | Expected Document Class | Accuracy |
|---|---|---|---|:---:|
| Door operator belt slip & reopen drift | `elevator_door_operations.pdf` / `ELV-005` | `COMPONENT_GUIDE` / `TROUBLESHOOTING` | Door System Guide | **100%** |
| Brake pad lining wear & air gap violation | `brake_of_gearless_traction_machine.pdf` | `COMPONENT_GUIDE` | EcoDisc PMSM Brake Manual | **100%** |
| Motor overcurrent & drive trip | `elevator_troubleshooting_dataset.csv (ELV-009)` | `TROUBLESHOOTING` | Drive / Motor Record | **100%** |
| SETS Terminal slowdown switch | `sets_egov_8_9.pdf` / `sets-11.pdf` | `OEM_REFERENCE` | SETS Configuration Guide | **100%** |
| Hoisting rope broken wires & crown wear | `elevator_hoisting_rope.pdf` | `COMPONENT_GUIDE` | ISO 4309 Rope Inspection | **100%** |

### 2.3 Configuration Filter Validation
- **Target Configuration: `EGOV 8/9`**
  - Retrieved `sets_egov_8_9.pdf`: `applicability = "MATCHED"` (Score: $0.85+$)
  - Retrieved `sets_egov_a.pdf`: `applicability = "NOT_APPLICABLE"` (Penalized by $-0.30$)
- **Target Configuration: Unknown / Unspecified**
  - Retrieved `sets_egov_*.pdf`: `applicability = "CONFIGURATION_UNKNOWN"`
  - System warning appended to technician view: `[⚠ Configuration applicability unknown — verify before applying]`

---

## 3. Ground-Truth Preservation Check

Across all 6 canonical validation scenarios, root cause ranking and calibrated confidence tiers remain strictly identical between baseline and RAG-augmented runs:

| Scenario | Injected Fault | Baseline Top Cause | RAG-Augmented Top Cause | Posterior $P$ | Abstention |
|---|---|---|---|:---:|:---:|
| **Scenario 1** | Drive Inverter IGBT Breakdown | IGBT Failure (`RC1`) | IGBT Failure (`RC1`) | $0.85$ | `False` |
| **Scenario 2** | Hoistway Mechanical Jam | Mechanical Obstruction (`RC2`) | Mechanical Obstruction (`RC2`) | $0.81$ | `False` |
| **Scenario 3** | Optical Light Curtain Drift | Photo-eye Degradation (`RC1`) | Photo-eye Degradation (`RC1`) | $0.68$ | `False` |
| **Scenario 4** | Encoder Pulse Degradation | Encoder Signal Degradation (`RC1`) | Encoder Signal Degradation (`RC1`) | $0.62$ | `False` |
| **Scenario 5** | Brake Release Timing Delay | Brake Release Timing (`RC1`) | Brake Release Timing (`RC1`) | $0.59$ | `False` |
| **Scenario 6** | Conflicting Sensor Signals | *None (Insufficient Data)* | *None (Insufficient Data)* | $< 0.45$ | **`True`** |

**Conclusion:** RAG integration successfully provides external grounding, step-by-step OEM execution checklists, and physical tolerance citations without corrupting mathematical Bayesian decision boundaries.
