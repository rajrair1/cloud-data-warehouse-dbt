import sys
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from pyspark.sql import functions as F

args = getResolvedOptions(sys.argv, ["JOB_NAME", "SOURCE_PATH", "TARGET_PATH"])
glue = GlueContext(SparkContext.getOrCreate())
job = Job(glue)
job.init(args["JOB_NAME"], args)

raw = glue.spark_session.read.option("multiline", True).json(args["SOURCE_PATH"])
daily = (raw.select("city", "ingested_at", F.posexplode("payload.daily.time").alias("day_index", "weather_date"), "payload.daily")
         .select(
             "city", F.to_date("weather_date").alias("weather_date"), F.to_timestamp("ingested_at").alias("ingested_at"),
             F.col("daily.temperature_2m_max")[F.col("day_index")].cast("double").alias("temperature_max_c"),
             F.col("daily.temperature_2m_min")[F.col("day_index")].cast("double").alias("temperature_min_c"),
             F.col("daily.precipitation_sum")[F.col("day_index")].cast("double").alias("precipitation_mm"),
         ).dropDuplicates(["city", "weather_date", "ingested_at"]))

(daily.write.mode("overwrite").partitionBy("weather_date").parquet(args["TARGET_PATH"]))
job.commit()
