# TrialFlow

A small data-engineering portfolio project using public clinical-trial data.

## Current status
- [x] Python API ingestion starter
- [ ] SQL transformations with DuckDB
- [ ] dbt models and data-quality tests
- [ ] GitHub Actions CI
- [ ] Optional interactive dashboard

## Quick start

Requires Python 3.10+.

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
PYTHONPATH=src python -m trialflow.ingest --condition diabetes --page-size 50
```

The script writes the unmodified API response to `data/raw/` with a timestamped filename.
Raw data is ignored by Git so the repository stays small.

## Data source
ClinicalTrials.gov API v2: https://clinicaltrials.gov/data-api/api

Independent portfolio project; not affiliated with ClinicalTrials.gov or MSD.
