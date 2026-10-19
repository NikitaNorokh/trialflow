WITH studies AS (
    SELECT *
    FROM read_csv_auto('data/processed/clinical_trials.csv')
),

checks AS (
    SELECT
        'missing_nct_id' AS check_name,
        COUNT(*) FILTER (
            WHERE nct_id IS NULL OR TRIM(nct_id) = ''
        ) AS failed_rows
    FROM studies

    UNION ALL

    SELECT
        'duplicate_nct_id',
        COUNT(*)
    FROM (
        SELECT nct_id
        FROM studies
        WHERE nct_id IS NOT NULL
        GROUP BY nct_id
        HAVING COUNT(*) > 1
    ) duplicates

    UNION ALL

    SELECT
        'missing_title',
        COUNT(*) FILTER (
            WHERE title IS NULL OR TRIM(title) = ''
        )
    FROM studies

    UNION ALL

    SELECT
        'missing_status',
        COUNT(*) FILTER (
            WHERE status IS NULL OR TRIM(status) = ''
        )
    FROM studies

    UNION ALL

    SELECT
        'invalid_nct_id_format',
        COUNT(*) FILTER (
            WHERE nct_id IS NOT NULL
              AND NOT regexp_matches(nct_id, '^NCT[0-9]{8}$')
        )
    FROM studies
)

SELECT
    check_name,
    failed_rows,
    CASE
        WHEN failed_rows = 0 THEN 'PASS'
        ELSE 'FAIL'
    END AS result
FROM checks
ORDER BY check_name;