# GUIDE Technical Corpus Inventory & Authority Classification

## Overview
ElevateRCA integrates the authoritative technical documentation from the `GUIDE/` corpus to provide evidence-grounded diagnostics for KONE traction elevators (MonoSpace, MiniSpace with EcoDisc PMSM motors).

---

## 1. Document Inventory & Metadata Mapping

| Document Name | File Type | Authority Level | Subsystem | Component | Configuration / EGOV | Document Purpose |
|---|---|---|---|---|---|---|
| `elevator_door_operations.pdf` | PDF | `COMPONENT_GUIDE` (L2) | `door` | Door System / AMD Operator | General | Mechanical linkages, roller tolerances, sill gaps, interlock timings |
| `brake_of_geared_traction_machine.pdf` | PDF | `COMPONENT_GUIDE` (L2) | `brake_traction` | Geared Traction Brake | Geared | Drum brake air gap, spring tension, microswitch adjustments |
| `brake_of_gearless_traction_machine.pdf` | PDF | `COMPONENT_GUIDE` (L2) | `brake_traction` | PMSM Disc Brake | Gearless (EcoDisc) | Disc brake pad thickness, coil drop delay, air gap tolerances |
| `elevator_brake_pad.pdf` | PDF | `COMPONENT_GUIDE` (L2) | `brake_traction` | Brake Pad / Friction Lining | General | Pad wear limits, friction coefficient degradation, replacement criteria |
| `elevator_hoisting_rope.pdf` | PDF | `COMPONENT_GUIDE` (L2) | `brake_traction` | Suspension / Hoisting Ropes | ISO 4309 | Wire breaks per lay length, crown wear, rope slip ratio, lubrication |
| `sets_egov_8_9.pdf` | PDF | `OEM_REFERENCE` (L1) | `encoder_position` | SETS Slowdown Switch | `EGOV 8/9` | Terminal speed enforcement governor position calibration |
| `sets_egov_a.pdf` | PDF | `OEM_REFERENCE` (L1) | `encoder_position` | SETS Slowdown Switch | `EGOV A` | Speed governor slowdown switch configuration Variant A |
| `sets_egov_b.pdf` | PDF | `OEM_REFERENCE` (L1) | `encoder_position` | SETS Slowdown Switch | `EGOV B` | Speed governor slowdown switch configuration Variant B |
| `sets_egov_d_e.pdf` | PDF | `OEM_REFERENCE` (L1) | `encoder_position` | SETS Slowdown Switch | `EGOV D/E` | Speed governor slowdown switch configuration Variant D/E |
| `sets_egov_f.pdf` | PDF | `OEM_REFERENCE` (L1) | `encoder_position` | SETS Slowdown Switch | `EGOV F` | Speed governor slowdown switch configuration Variant F |
| `sets-11.pdf` | PDF | `OEM_REFERENCE` (L1) | `encoder_position` | SETS-11 System | `SETS-11` | Terminal slowdown switchboard layout, positioning tolerances |
| `kone guide maintainance procdure.pdf` | PDF | `OEM_REFERENCE` (L1) | Multi-subsystem | General Maintenance | KONE Standard | Field service checklist, lubrication schedules, annual inspection |
| `OEM 1.pdf` | PDF | `OEM_REFERENCE` (L1) | Multi-subsystem | Drive & Controller Specs | KONE Standard | EcoDisc inverter drive ratings, electrical clearances, fault codes |
| `elevator_troubleshooting_dataset.csv` | CSV | `TROUBLESHOOTING` (L3) | Multi-subsystem | 15 Components | ELV-001 to ELV-015 | Tabular symptoms, alarms, evidence, checks, and corrective actions |
| `elevator_troubleshooting_dataset.json` | JSON | `TROUBLESHOOTING` (L3) | Multi-subsystem | 15 Components | ELV-001 to ELV-015 | Structured JSON equivalent of field troubleshooting cases |

---

## 2. Document Authority Hierarchy (5 Tiers)

ElevateRCA resolves potential contradictions between sources using a strict 5-tier document authority hierarchy:

```
[Tier 1: OEM_REFERENCE]
  - sets_egov_*.pdf, sets-11.pdf, kone guide maintainance procdure.pdf, OEM 1.pdf
  - Weight: 1.0 (Highest authority for configuration, electrical limits, OEM standards)
         │
         ▼
[Tier 2: COMPONENT_GUIDE]
  - elevator_door_operations.pdf, brake_of_*.pdf, elevator_brake_pad.pdf, elevator_hoisting_rope.pdf
  - Weight: 0.85 (Authoritative for physical tolerances, clearances, wear limits)
         │
         ▼
[Tier 3: TROUBLESHOOTING]
  - elevator_troubleshooting_dataset.csv, elevator_troubleshooting_dataset.json (ELV-001–015)
  - Weight: 0.70 (Field diagnostic cases, symptom-to-cause mappings)
         │
         ▼
[Tier 4: PROJECT_KNOWLEDGE]
  - failure_modes.yaml, causal_links.yaml, corrective_actions.yaml, kone_error_matrix.yaml
  - Weight: 0.60 (Validated Bayesian fault trees, approved SOPs)
         │
         ▼
[Tier 5: GENERAL_KNOWLEDGE]
  - General LLM inference (Lowest authority; cannot override OEM/knowledge specifications)
```

### Hierarchy Rules:
1. **Specific Trumps General:** A configuration-specific OEM manual (`sets_egov_a.pdf`) always overrides a general component guide.
2. **Hard Specifications Overrule Heuristics:** Numerical tolerances (e.g., brake air gap `0.30 mm ± 0.05 mm`, door sill gap `4.0 mm ± 1.0 mm`) from Tier 1/2 documents cannot be overridden by lower-tier troubleshooting heuristics.
3. **Safety Proscriptions:** Prohibited actions ("DO NOT DO") from approved SOPs are absolute and cannot be softened by lower-tier texts.

---

## 3. Configuration-Specific Discipline

ElevateRCA prevents dangerous cross-configuration contamination:
- **EGOV 8/9, A, B, D/E, F & SETS-11** manuals contain different terminal slowdown switch positions and trip velocities.
- If the elevator configuration is known, only matching configuration documents receive positive relevance boosts.
- If the elevator configuration is **unknown**, documents with configuration constraints are tagged with:
  `[⚠ Configuration applicability unknown — verify before applying]` (`applicability = "CONFIGURATION_UNKNOWN"`).
- Documents from conflicting configurations receive a heavy negative ranking penalty (`applicability = "NOT_APPLICABLE"`).

---

## 4. Ingestion & Chunking Pipeline

- **Parser:** PyMuPDF (`fitz`) for text extraction and page boundary preservation.
- **Chunking:** Semantic paragraph chunker with 800-character windows and 100-character overlap.
- **Table Preservation:** Structured extraction of tabular tolerance specifications.
- **Warning Detection:** Automatic identification and tagging of safety notices (`is_warning = True`).
- **Procedure Detection:** Heuristic recognition of step-by-step diagnostic workflows (`is_procedure = True`).
