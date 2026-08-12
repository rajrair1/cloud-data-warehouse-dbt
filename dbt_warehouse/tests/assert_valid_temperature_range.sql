select *
from {{ ref('mart_daily_city_weather') }}
where temperature_min_c < -100
   or temperature_max_c > 70
   or temperature_min_c > temperature_max_c
