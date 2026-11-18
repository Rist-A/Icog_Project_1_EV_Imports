# data/processed - made by notebooks 01 and 02 (safe to delete and regenerate)

| File | Made by | Meaning |
|---|---|---|
| `cleaned_dataset.csv` | 01 | The validated 30-row dataset used for scoring |
| `missing_report.csv` | 01 | How many cells are missing for each key evidence field |
| `coverage_by_vehicle.csv` | 01 | Per vehicle: fitment found, prices found, NHTSA rows, judgement filled |
| `cleaning_log.csv` | 01 | Every cleaning action taken, with row counts |
| `scored_vehicle_part.csv` | 02 | Five factor scores and the total for each vehicle-part row |
| `part_ranking.csv` | 02 | All 10 parts ranked, with evidence coverage |
| `top5_parts.csv` | 02 | **The five recommended parts** |
| `sensitivity_ranks.csv`, `sensitivity_stability.csv` | 02 | Does the ranking change when the weights change? |
| `scoring_config.json` | 02 | The exact weights and fitment scores used, so the ranking can be reproduced |
| `vehicle_selection.csv` | 00a | **The 5 candidates ranked**: Adey listings, Gezat presence, part-data sources, selection score, how stable the rank is, suggested top 3 and your selection. This is the evidence for the choice of vehicles |
| `vehicle_selection_sensitivity.csv` | 00a | Rank of each candidate under other weights |
