from flask import Flask, render_template, request, jsonify
import json
import pandas as pd
from data_storage import DataStorage
from spark_processor import SparkProcessor

app = Flask(__name__)
data_storage = DataStorage()
spark_processor = SparkProcessor()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'})
    
    try:
        # Load and store data
        reviews = json.load(file)
        data_storage.store_reviews(reviews)
        
        # Process with Spark
        results, stats = spark_processor.process_reviews(reviews)
        
        # Calculate statistics without Dask
        total = stats['total']
        counts = {row['sentiment']: row['count'] for row in stats['counts']}
        
        formatted_stats = {
            'total': total,
            'positive': counts.get('Positive', 0),
            'negative': counts.get('Negative', 0),
            'neutral': counts.get('Neutral', 0),
            'positive_percent': (counts.get('Positive', 0)/total)*100,
            'negative_percent': (counts.get('Negative', 0)/total)*100,
            'neutral_percent': (counts.get('Neutral', 0)/total)*100
        }
        
        formatted_results = [{
            'review': r['Review Title'],
            'customer': r['Customer name'],
            'sentiment': r['sentiment']
        } for r in results]
        
        return jsonify({
            'results': formatted_results,
            'stats': formatted_stats
        })
        
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
