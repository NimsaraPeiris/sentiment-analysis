from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, col
from pyspark.sql.types import StringType
from preprocessor import preprocess_text

# Create Spark session
spark = SparkSession.builder.appName("SentimentAnalysis").getOrCreate()

# Load data and print schema to verify column names
df = spark.read.json("reviews.json")
print("DataFrame Schema:")
df.printSchema()

# Register preprocessing function as UDF
preprocess_udf = udf(preprocess_text, StringType())

# Apply preprocessing using proper column reference
df_processed = df.withColumn("processed_text", preprocess_udf(col("`Review Title`")))

print("\nProcessed reviews:")
df_processed.select(col("`Review Title`"), "processed_text").show(5, truncate=False)

# Optional: Save processed data
# df_processed.write.json("processed_reviews.json")
