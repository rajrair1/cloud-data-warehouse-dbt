with ranked as (
  select *, row_number() over (partition by city, weather_date order by ingested_at desc) as recency_rank
  from {{ ref('stg_weather_daily') }}
)
select
  {{ dbt_utils.generate_surrogate_key(['city', 'weather_date']) }} as weather_key,
  city,
  weather_date,
  temperature_max_c,
  temperature_min_c,
  round((temperature_max_c + temperature_min_c) / 2, 2) as temperature_avg_c,
  precipitation_mm,
  ingested_at
from ranked
where recency_rank = 1
