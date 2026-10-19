from trialflow.pipeline import transform_studies


def test_transform_study():
    studies = [
        {
            "protocolSection": {
                "identificationModule": {
                    "nctId": "NCT12345678",
                    "briefTitle": "Example clinical study",
                },
                "statusModule": {
                    "overallStatus": "RECRUITING",
                    "startDateStruct": {
                        "date": "2026-01-15"
                    },
                },
                "designModule": {
                    "phases": ["PHASE2"],
                },
                "conditionsModule": {
                    "conditions": ["Diabetes"],
                },
            }
        }
    ]

    df = transform_studies(studies)

    assert len(df) == 1
    assert df.loc[0, "nct_id"] == "NCT12345678"
    assert df.loc[0, "title"] == "Example clinical study"
    assert df.loc[0, "status"] == "RECRUITING"
    assert df.loc[0, "phase"] == "PHASE2"
    assert df.loc[0, "condition"] == "Diabetes"
    assert df.loc[0, "start_date"] == "2026-01-15"


def test_transform_empty_input():
    df = transform_studies([])

    assert df.empty
    assert list(df.columns) == [
        "nct_id",
        "title",
        "status",
        "phase",
        "condition",
        "start_date",
    ]