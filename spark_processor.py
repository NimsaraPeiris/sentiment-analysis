from pyspark.sql import SparkSession
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType, StructType, StructField
from textblob import TextBlob
from config import *

class SparkProcessor:
    def __init__(self):
        self.spark = SparkSession.builder \
            .appName(SPARK_APP_NAME) \
            .master(SPARK_MASTER) \
            .getOrCreate()

    @staticmethod
    def analyze_sentiment(text):
        analysis = TextBlob(text)
        if analysis.sentiment.polarity > 0:
            return 'Positive'
        elif analysis.sentiment.polarity == 0:
            return 'Neutral'
        else:
            return 'Negative'

    def process_reviews(self, reviews):
        # Define schema for DataFrame
        schema = StructType([
            StructField("Review Title", StringType(), True),
            StructField("Customer name", StringType(), True)
        ])
        
        # Create DataFrame with schema
        df = self.spark.createDataFrame(reviews, schema=schema)
        
        # Register UDF
        sentiment_udf = udf(self.analyze_sentiment, StringType())
        
        # Apply sentiment analysis
        results_df = df.withColumn('sentiment', 
                                sentiment_udf(df['Review Title']))
        
        # Calculate statistics
        total = results_df.count()
        sentiment_counts = results_df.groupBy('sentiment').count()
        
        stats = {
            'total': total,
            'counts': sentiment_counts.collect()
        }
        
        return results_df.collect(), stats
