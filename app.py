from flask import Flask, render_template, request,jsonify
import pandas as pd
from textblob import TextBlob
import random

app = Flask(__name__)

# Load data from CSV files into pandas DataFrames
books_df = pd.read_csv('static/data/books.csv')
songs_df = pd.read_csv('static/data/songs.csv')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommendations', methods=['POST'])
def recommendations():
    try:
        user_text = request.form.get('user_text')
        sentiment_analysis = TextBlob(user_text)
        sentiment = sentiment_analysis.sentiment.polarity
        
        # Determine mood based on sentiment
        if sentiment > 0:
            sentiment_category = 'positive'
        elif sentiment < 0:
            sentiment_category = 'negative'
        else:
            sentiment_category = 'neutral'
        
        
        # Perform recommendation logic
        recommended_books = books_df[books_df['mood'] == sentiment_category]
        recommended_songs = songs_df[songs_df['mood'] == sentiment_category]

        # Select one random book and one random song
        recommended_book = random.choice(recommended_books['title'].tolist()) if not recommended_books.empty else "No book recommendations available for this mood."
        recommended_song = random.choice(recommended_songs['title'].tolist()) if not recommended_songs.empty else "No song recommendations available for this mood."
        
        positive_sentiment = max(0, sentiment)
        negative_sentiment = max(0, -sentiment)
        neutral_sentiment = 1 - positive_sentiment - negative_sentiment
        return render_template('result.html', overall_sentiment=sentiment_category, positive_sentiment=positive_sentiment, negative_sentiment=negative_sentiment, neutral_sentiment=neutral_sentiment, user_text=user_text, sentiment=sentiment, books=recommended_book, songs=recommended_song)
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
