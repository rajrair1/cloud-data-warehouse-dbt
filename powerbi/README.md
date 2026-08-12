# Power BI reporting layer

Connect Power BI to `WEATHER_ANALYTICS.ANALYTICS.MART_DAILY_CITY_WEATHER` through the Snowflake connector.

Suggested measures:

```DAX
Average Temperature C = AVERAGE(mart_daily_city_weather[temperature_avg_c])
Total Precipitation MM = SUM(mart_daily_city_weather[precipitation_mm])
Latest Refresh UTC = MAX(mart_daily_city_weather[ingested_at])
```

Suggested report pages:

1. City overview: latest temperature, precipitation, and refresh timestamp
2. Trends: daily min/max/average temperature by city
3. Data quality: freshness and missing-value indicators
