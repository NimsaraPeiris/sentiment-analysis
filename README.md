# Sentiment Analysis with Big Data Technologies

A sentiment analysis application that processes customer reviews using big data technologies like Apache Spark, MongoDB, and Flask.

## Features

- Real-time sentiment analysis of customer reviews
- Interactive web interface with visualizations
- Big data processing with Apache Spark
- Data persistence using MongoDB
- Beautiful visualization using Chart.js
- RESTful API endpoints

## Tech Stack

- **Backend**: Python, Flask
- **Processing**: Apache Spark, TextBlob
- **Database**: MongoDB
- **Frontend**: HTML5, Bootstrap 5, Chart.js
- **Data Format**: JSON

## Prerequisites

- Python 3.8+
- MongoDB
- Apache Spark
- pip (Python package manager)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/sentiment-analysis.git
   cd sentiment-analysis
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Start MongoDB service:
   ```bash
   # Windows
   net start MongoDB
   
   # Linux/Mac
   sudo service mongod start
   ```

4. Run the application:
   ```bash
   python app.py
   ```

5. Open your browser and navigate to:
   ```
   http://localhost:5000
   ```

## Usage

1. Prepare your review data in JSON format following this structure:
   ```json
   [
     {
       "Review Title": "Your review text here",
       "Customer name": "Customer Name"
     }
   ]
   ```

2. Upload the JSON file through the web interface
3. View the sentiment analysis results and visualizations

## Project Structure

