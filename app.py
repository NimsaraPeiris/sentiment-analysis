from flask import Flask, render_template, request, jsonify
from textblob import TextBlob
import json

app = Flask(__name__)

def analyze_sentiment(text):
    analysis = TextBlob(text)
    # Determine sentiment
    if analysis.sentiment.polarity > 0:
        return 'Positive'
    elif analysis.sentiment.polarity == 0:
        return 'Neutral'
    else:
        return 'Negative'

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
        data = json.load(file)
        results = []
        
        for review in data:
            sentiment = analyze_sentiment(review['Review Title'])
            results.append({
                'review': review['Review Title'],
                'customer': review['Customer name'],
                'sentiment': sentiment
            })
        
        # Calculate statistics
        total = len(results)
        positive = sum(1 for r in results if r['sentiment'] == 'Positive')
        negative = sum(1 for r in results if r['sentiment'] == 'Negative')
        neutral = sum(1 for r in results if r['sentiment'] == 'Neutral')
        
        stats = {
            'total': total,
            'positive': positive,
            'negative': negative,
            'neutral': neutral,
            'positive_percent': (positive/total)*100,
            'negative_percent': (negative/total)*100,
            'neutral_percent': (neutral/total)*100
        }
        
        return jsonify({
            'results': results,
            'stats': stats
        })
        
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
