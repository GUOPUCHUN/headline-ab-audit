-- One row per test with exactly one editor-selected winner,
-- comparing the winner with the top two arms by CTR.

with arms as (
    select * from {{ ref('fct_arm_results') }}
),

decided_tests as (
    select test_id
    from arms
    group by test_id
    having countif(is_winner) = 1
),

winners as (
    select
        test_id,
        ctr_rank as winner_rank,
        impressions as winner_impressions,
        clicks as winner_clicks,
        ctr as winner_ctr
    from arms
    where is_winner
),

top_two as (
    select
        test_id,
        max(if(ctr_rank = 1, impressions, null)) as top_impressions,
        max(if(ctr_rank = 1, clicks, null)) as top_clicks,
        max(if(ctr_rank = 1, ctr, null)) as top_ctr,
        max(if(ctr_rank = 2, impressions, null)) as runner_up_impressions,
        max(if(ctr_rank = 2, clicks, null)) as runner_up_clicks,
        max(if(ctr_rank = 2, ctr, null)) as runner_up_ctr
    from arms
    group by test_id
)

select
    t.test_id,
    t.dataset_split,
    t.started_at,
    t.n_arms,
    t.is_problem_period,
    w.winner_rank,
    w.winner_rank = 1 as winner_is_top,
    w.winner_impressions,
    w.winner_clicks,
    w.winner_ctr,
    tt.top_impressions,
    tt.top_clicks,
    tt.top_ctr,
    tt.runner_up_impressions,
    tt.runner_up_clicks,
    tt.runner_up_ctr
from {{ ref('int_tests') }} as t
inner join decided_tests as d using (test_id)
inner join winners as w using (test_id)
inner join top_two as tt using (test_id)
where t.n_arms >= 2