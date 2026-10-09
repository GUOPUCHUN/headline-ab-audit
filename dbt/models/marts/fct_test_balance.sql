-- One row per test with the inputs for a sample ratio mismatch (SRM) check.
-- Assumes equal allocation across arms; this assumption is checked in the notebook.
-- Excludes single-arm tests and tests with zero impressions (no comparison possible).
-- p-values are computed in Python: BigQuery has no chi-square distribution function.

with packages as (
    select test_id, impressions
    from {{ ref('stg_packages') }}
),

tests as (
    select *
    from {{ ref('int_tests') }}
    where n_arms >= 2
      and total_impressions > 0
),

arms as (
    select
        p.test_id,
        p.impressions as observed,
        t.total_impressions / t.n_arms as expected
    from packages as p
    inner join tests as t using (test_id)
)

select
    t.test_id,
    t.dataset_split,
    t.started_at,
    t.is_problem_period,
    t.n_arms,
    t.total_impressions,
    t.arm_created_spread_minutes,
    min(a.observed) as min_arm_impressions,
    max(a.observed) as max_arm_impressions,
    sum(pow(a.observed - a.expected, 2) / a.expected) as chi_square_stat,
    t.n_arms - 1 as degrees_of_freedom
from tests as t
inner join arms as a using (test_id)
group by 1, 2, 3, 4, 5, 6, 7