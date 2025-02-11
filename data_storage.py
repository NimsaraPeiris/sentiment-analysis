from pymongo import MongoClient
from hdfs import InsecureClient
import logging
from config import *

class DataStorage:
    def __init__(self):
        # MongoDB connection
        try:
            self.mongo_client = MongoClient(MONGODB_URI)
            self.db = self.mongo_client[MONGODB_DB]
            self.collection = self.db[MONGODB_COLLECTION]
        except Exception as e:
            logging.error(f"MongoDB connection failed: {e}")
            raise
        
        # HDFS connection (disabled by default)
        self.hdfs_client = None
        self.hdfs_enabled = False

    def store_reviews(self, reviews):
        # Store in MongoDB
        try:
            # Convert reviews to proper format
            formatted_reviews = [{
                'review_title': review['Review Title'],
                'customer_name': review['Customer name']
            } for review in reviews]
            self.collection.insert_many(formatted_reviews)
            logging.info(f"Stored {len(formatted_reviews)} reviews in MongoDB")
        except Exception as e:
            logging.error(f"MongoDB storage failed: {e}")
            raise

    def get_reviews(self):
        try:
            # Project specific fields and exclude _id
            return list(self.collection.find(
                {}, 
                {
                    '_id': 0, 
                    'review_title': 1, 
                    'customer_name': 1
                }
            ))
        except Exception as e:
            logging.error(f"MongoDB retrieval failed: {e}")
            raise
