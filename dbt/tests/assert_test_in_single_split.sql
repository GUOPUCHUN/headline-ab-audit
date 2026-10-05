-- Each test must belong to exactly one dataset split
-- (int_tests relies on this when it uses any_value).
select
    test_id,
    count(distinct dataset_split) as n_splits
from {{ ref('stg_packages') }}
group by test_id
having count(distinct dataset_split) > 1