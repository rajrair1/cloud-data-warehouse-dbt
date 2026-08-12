select
  lower(trim(city)) as city,
  cast(weather_date as date) as weather_date,
  cast(temperature_max_c as decimal(8,2)) as temperature_max_c,
  cast(temperature_min_c as decimal(8,2)) as temperature_min_c,
  cast(precipitation_mm as decimal(10,2)) as precipitation_mm,
  cast(ingested_at as timestamp) as ingested_at
from {{ source('raw', 'weather_daily') }}
