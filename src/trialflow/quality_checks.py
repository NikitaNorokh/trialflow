import sys
from pathlib import Path

import duckdb

PROJECT_ROOT = Path(__file__).resolve().parents[2]
CSV_PATH = PROJECT_ROOT / "data" / "processed" / "clinical_trials.csv"
SQL_PATH = PROJECT_ROOT / "sql" / "quality_checks.sql"


def main():
    if not CSV_PATH.exists():
        print(f"ERROR: CSV file not found: {CSV_PATH}")
        print("Run pipeline.py first.")
        sys.exit(1)

    sql = SQL_PATH.read_text(encoding="utf-8")
    sql = sql.replace(
        "data/processed/clinical_trials.csv",
        CSV_PATH.as_posix()
    )


    con = duckdb.connect(":memory:")

    try:
        results = con.execute(sql).df()
    finally:
        con.close()

    print("\nDATA QUALITY REPORT")
    print("=" * 55)
    print(results.to_string(index=False))

    failed = results[results["result"] == "FAIL"]

    if not failed.empty:
        print(f"\nFAILED: {len(failed)} quality check(s)")
        sys.exit(1)

    print("\nSUCCESS: All quality checks passed.")


if __name__ == "__main__":
    main()