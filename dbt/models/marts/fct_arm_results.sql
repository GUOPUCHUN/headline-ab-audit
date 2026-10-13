-- One row per arm (package) with its CTR rank within the test.
-- Ties in CTR are broken by impressions, so each test has exactly one arm per rank.

with packages as (
    select * from {{ ref('stg_packages') }}
),

tests as (
    select test_id, started_at, n_arms, is_problem_period
    from {{ ref('int_tests') }}
)

select
    p.test_id,
    p.dataset_split,
    t.started_at,
    t.n_arms,
    t.is_problem_period,
    p.created_at as arm_created_at,
    p.headline,
    p.eyecatcher_id,
    p.impressions,
    p.clicks,
    p.ctr,
    p.is_winner,
    p.is_first_place,
    row_number() over (
        partition by p.test_id
        order by p.ctr desc, p.impressions desc
    ) as ctr_rank
from packages as p
inner join tests as t using (test_id)