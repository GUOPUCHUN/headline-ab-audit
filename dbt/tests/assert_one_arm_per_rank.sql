-- Each test must have exactly one arm at each CTR rank.
select
    test_id,
    ctr_rank,
    count(*) as n_arms_at_rank
from {{ ref('fct_arm_results') }}
group by test_id, ctr_rank
having count(*) > 1