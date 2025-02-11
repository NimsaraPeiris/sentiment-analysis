from pymongo import MongoClient
import pandas as pd
import json

client = MongoClient("mongodb://localhost:27017/")
db = client["customer_reviews_db"]
collection = db["reviews"]

# Try different encodings
encodings = ['utf-8', 'latin1', 'iso-8859-1', 'cp1252']
for encoding in encodings:
    try:
        df = pd.read_csv("reviews.csv", encoding=encoding)
        print(f"Successfully read file with {encoding} encoding")
        break
    except UnicodeDecodeError:
        continue
    except FileNotFoundError:
        print("Error: reviews.csv file not found in the current directory")
        exit(1)
else:
    print("Error: Could not read the file with any of the attempted encodings")
    exit(1)

# Select only required columns
df_selected = df[['Review Title', 'Customer name']]

# Replace NaN values with empty strings
df_selected = df_selected.fillna("")

data_dict = df_selected.to_dict(orient="records")

# Save to JSON file
json_file_path = "reviews.json"
with open(json_file_path, 'w', encoding='utf-8') as f:
    json.dump(data_dict, f, ensure_ascii=False, indent=4)
print(f"Data successfully saved to {json_file_path}")

# Remove current data in MongoDB and insert new tweets
collection.delete_many({})

collection.insert_many(data_dict)
print("Data successfully imported to MongoDB")