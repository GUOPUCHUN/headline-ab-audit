-- Impressions and clicks are counts and cannot be negative.
select *
from {{ ref('stg_packages') }}
where impressions < 0
   or clicks < 0
   