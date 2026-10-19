import requests
import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

API_URL = "https://clinicaltrials.gov/api/v2/studies"


def fetch_studies(condition="diabetes", page_size=50):
    """Fetch clinical studies from the ClinicalTrials.gov API."""

    response = requests.get(
        API_URL,
        params={
            "format": "json",
            "query.cond": condition,
            "pageSize": page_size,
        },
        timeout=30,
    )

    response.raise_for_status()
    payload = response.json()

    return payload.get("studies", [])


def transform_studies(studies):
    """Transform nested API data into a flat table."""

    rows = []

    for study in studies:
        protocol = study.get("protocolSection", {})

        identification = protocol.get("identificationModule", {})
        status_info = protocol.get("statusModule", {})
        design = protocol.get("designModule", {})
        conditions_info = protocol.get("conditionsModule", {})

        phases = design.get("phases") or []
        conditions = conditions_info.get("conditions") or []

        start_date = status_info.get("startDateStruct", {})
        start_date = start_date.get("date")

        rows.append({
            "nct_id": identification.get("nctId"),
            "title": identification.get("briefTitle"),
            "status": status_info.get("overallStatus"),
            "phase": ", ".join(phases) if phases else None,
            "condition": ", ".join(conditions) if conditions else None,
            "start_date": start_date,
        })

    return pd.DataFrame(rows, columns=[
        "nct_id",
        "title",
        "status",
        "phase",
        "condition",
        "start_date",
    ])


def main():
    studies = fetch_studies()
    df = transform_studies(studies)

    output_path = (
        PROJECT_ROOT / "data" / "processed" / "clinical_trials.csv"
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)

    df.to_csv(output_path, index=False)

    print(f"Fetched {len(studies)} studies")
    print(f"Saved table to {output_path}")
    print(df.head(5).to_string(index=False))


if __name__ == "__main__":
    main()