# data/raw - evidence exactly as collected (do not edit by hand, except the one sheet noted below)

| File | Made by | Meaning |
|---|---|---|
| `source_log.csv` | notebook 00 | Every source: URL, collection date, robots.txt result, note |
| `fetch_log.csv` | notebook 00 | Every request made (or skipped) with its status |
| `html_snapshots/` | notebook 00 | Saved copy of each page, as proof of what was seen |
| `parts_catalogue_raw.csv` | notebook 00 | Every part line found for the 3 vehicles (part number, OE number, price, source) |
| `nhtsa_complaints_raw.csv`, `nhtsa_components_found.csv` | notebook 00 | NHTSA complaints and the component labels they carry |
| `adey_listings_scraped.csv` | notebook 00a | Every Adey listing card read (live page, or saved page copies read offline). Counts from it are a visibility proxy, **not** registrations or sales |
| `gezat_scraped.csv` | notebook 00a | What the allowed Gezat pages show for each of the 5 candidates. Blank means unknown, not "not listed" |
| **`vehicle_manual_inputs.csv`** | **you** (template made by 00a) | Your hand-entered evidence for the 5 candidates (below) |
| `vehicle_part_combinations_scraped.csv` | notebook 00 | The 30-row sheet filled by code. Never overwritten by you |
| **`vehicle_part_combinations.csv`** | **you** | A copy of the scraped sheet that you complete by hand. This is the file notebook 01 reads |

## `vehicle_manual_inputs.csv` (one row per candidate vehicle)
| Column | What to enter |
|---|---|
| `gezat_listed` | 1 if you saw the model in the Gezat catalogue in your browser, 0 if you checked and it is not there, blank if not checked |
| `gezat_evidence_url`, `gezat_check_date`, `gezat_note` | Where and when you looked, and what you saw |
| `adey_manual_count`, `adey_manual_date` | Only if the code could not read Adey: the number of listings you counted by hand |
| `parts_sources_found` | Part-data sources that cover this vehicle, separated by `;`. Pre-filled from reading the source-pack pages once. **Verify it** |

A value typed here always wins over what the code found.

## Columns you fill by hand in `vehicle_part_combinations.csv`
| Column | What to enter |
|---|---|
| `wear_item` | 1 if the part wears out in normal use, else 0 - your judgement |
| `wear_basis` | Your reason, for example "pads wear with braking" |
| `local_sellers` | Number of Ethiopian sellers you found, or leave blank if not checked |
| `local_sellers_source`, `local_check_date` | How and when you checked |
| `in_stock` | 1 or 0 if a source states it, else blank |
| `fx_rate_to_usd`, `fx_rate_date` | Only if you want USD prices. Take the rate from an official source |
| `evidence_notes` / any blank cell the scraper could not fill | What you found by hand, with the source ID in `compat_source_ids` / `price_source_id` |

**Blank means unknown. 0 means you checked and found none.** Never type a guess.
Values you add by hand must still be traceable: put `manual` in `collection_method` and add the source to `source_log.csv`.
