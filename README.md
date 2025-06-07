# DublinBikes Near‑Real‑Time Warehouse

> **dbt + DuckDB + GitHub Actions** — A zero‑cost pipeline that ingests the live DublinBikes GBFS feed every minute, models it with dbt, and stores everything in a local DuckDB file.  The project is designed for quick demos; you can run the whole thing on your laptop or schedule it in GitHub Actions for hands‑free updates.

---

## Features

| Layer              | Tech             | Highlights                                                                 |
| ------------------ | ---------------- | -------------------------------------------------------------------------- |
| **Ingestion**      | Python, DuckDB   | <1‑min latency, incremental append, single‑file DB                         |
| **Transformation** | dbt              | Incremental fact model, freshness tests, snapshots, real‑time tag selector |
| **CI / Scheduler** | GitHub Actions   | 5‑min cron, artefact persistence for DuckDB, job summary KPI               |

---

## Quick start (local)

```bash
# clone & bootstrap
$ git clone https://github.com/tetianakushniruk/dublinbikes-warehouse.git
$ cd dublinbikes-warehouse
$ python -m venv .venv && source .venv/bin/activate
$ pip install -r requirements.txt

# one‑off load + full build + docs
$ python scripts/ingest_dublinbikes.py
$ dbt build --full-refresh
$ dbt docs generate && dbt docs serve
```

---

## Repo layout

```
.
├─ models/                # dbt models (stg_, dim_, fact_)
├─ snapshots/             # SCD‑2 snapshot of station capacity
├─ macros/                # custom macros & tests
├─ scripts/ingest_dublinbikes.py
├─ run_realtime.sh        # local loop
├─ dev.duckdb             # DuckDB database (git‑ignored)
└─ .github/workflows/     # CI & real‑time cron
```

---

## Continuous build in GitHub Actions

1. The **realtime** workflow ingests the JSON feed, runs `dbt run --select tag:realtime+`, persists the updated `warehouse.duckdb` as a build artefact, and prints a KPI table.
2. Runs every 5 min (cron) or on manual trigger; each run cancels the previous one to avoid overlap.

You can download the artefact from any run and open it in DuckDB or Tableau for ad‑hoc analysis.

---

## Tests & quality gates

| Check              | Details                                                                 |
| ------------------ | ------------------------------------------------------------------------|
| **Null / Unique**  | `station_id`, `recorded_at_minute`                                      |
| **Accepted Range** | `bikes_available >= 0`, `availability_pct <= 1` (via `dbt_expectations`)|
| **Freshness**      | Warn after 3 min, error after 5 min on source feed                      |

CI fails on any test error so the warehouse never ships bad data.

---

## License

MIT for code.  Data © Dublin City Council & JCDecaux (Creative Commons).
