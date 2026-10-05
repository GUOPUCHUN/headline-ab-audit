-- One row per test, aggregated from packages (arms).
-- is_problem_period: the window the archive authors flagged for unreliable
-- randomization (2013-06-25 to 2014-01-10), reconstructed from started_at
-- because the OSF files do not include the `problem` column.

with packages as (
    select * from {{ ref('stg_packages') }}
)

select
    test_id,
    any_value(dataset_split) as dataset_split,
    min(created_at) as started_at,
    count(*) as n_arms,
    sum(impressions) as total_impressions,
    sum(clicks) as total_clicks,
    countif(is_winner) as n_winners,
    min(created_at) between timestamp '2013-06-25'
        and timestamp '2014-01-10 23:59:59' as is_problem_period
from packages
group by test_id