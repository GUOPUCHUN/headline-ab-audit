-- A package cannot have more clicks than impressions.
select *
from {{ ref('stg_packages') }}
where clicks > impressions