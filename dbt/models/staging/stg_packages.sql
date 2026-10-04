-- One row per package (one arm of a headline test), from both dataset splits.
-- Raw columns are all STRING; types are cast here.
-- Dropped: row_index (export artifact), square (mixed types, unused),
-- significance (undocumented calculation), test_week (not needed).

with exploratory as (
    select *, 'exploratory' as dataset_split
    from {{ source('raw', 'packages_exploratory') }}
),

confirmatory as (
    select *, 'confirmatory' as dataset_split
    from {{ source('raw', 'packages_confirmatory') }}
),

unioned as (
    select * from exploratory
    union all
    select * from confirmatory
)

select
    clickability_test_id as test_id,
    eyecatcher_id,
    headline,
    excerpt,
    lede,
    slug,
    share_text,
    cast(created_at as timestamp) as created_at,
    cast(updated_at as timestamp) as updated_at,
    cast(impressions as int64) as impressions,
    cast(clicks as int64) as clicks,
    safe_divide(cast(clicks as int64), cast(impressions as int64)) as ctr,
    lower(first_place) = 'true' as is_first_place,
    lower(winner) = 'true' as is_winner,
    dataset_split
from unioned