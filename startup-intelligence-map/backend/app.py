from flask import Flask, jsonify, render_template, request
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from data_processing import DataProcessor
from sector_classifier import SectorClassifier

app = Flask(
    __name__,
    template_folder=os.path.join(os.path.dirname(__file__), '..', 'templates'),
    static_folder=os.path.join(os.path.dirname(__file__), '..', 'static')
)

processor = DataProcessor()
classifier = SectorClassifier()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/trends')
def get_trends():
    data = processor.get_all_data()
    trends = processor.calculate_trend_scores(data)
    return jsonify(trends)

@app.route('/api/news')
def get_news():
    news = processor.get_news_data()
    return jsonify(news)

@app.route('/api/jobs')
def get_jobs():
    jobs = processor.get_job_data()
    return jsonify(jobs)

@app.route('/api/startups')
def get_startups():
    startups = processor.get_startup_data()
    return jsonify(startups)

@app.route('/api/prediction')
def get_prediction():
    data = processor.get_all_data()
    prediction = processor.generate_prediction(data)
    return jsonify(prediction)

@app.route('/api/map-data')
def get_map_data():
    return jsonify(processor.get_map_data())

@app.route('/api/historical')
def get_historical():
    return jsonify(processor.get_historical_data())

if __name__ == '__main__':
    app.run(debug=True, port=5000)
