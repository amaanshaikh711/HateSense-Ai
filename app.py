# app.py

from flask import Flask, render_template, request
import nltk
from model.predict import predict
from utils.cleaning import count_offensive_words, calculate_vulgarity_level, OFFENSIVE_WORDS
import plotly.graph_objects as go
import plotly.io as pio

nltk.download('stopwords')

# Initialize Flask app
app = Flask(__name__, static_folder='static', template_folder='templates')

@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/input', methods=['GET', 'POST'])
def input_page():
    sentiment = ""
    hate_speech = ""
    input_text = ""
    sentiment_score = {"Positive": 0, "Neutral": 0, "Negative": 0}
    hate_score = {"Hate Speech": 0, "None": 0}
    offensive_word_count = 0
    vulgarity = "--"
    pie_chart_div = None
    bar_chart_div = None
    line_chart_div = None
    highlighted_input = None
    sentiment_emoji = ""

    if request.method == 'POST':
        import logging
        input_text = request.form['user_input']
        # --- Offensive Word Detection ---
        OFFENSIVE_WORDS_LIST = ["damn", "stupid", "idiot", "dumb", "hate", "fool", "trash", "ugly", "loser", "moron", "sucks", "shut up", "nonsense", "jerk", "freak"]
        # Lowercase and split input
        words = [w.strip('.,!?;:').lower() for w in input_text.split()]
        offensive_found = [w for w in words if w in OFFENSIVE_WORDS_LIST]
        offensive_word_count = len(offensive_found)
        total_words = len([w for w in words if w.isalpha()])
        if total_words == 0:
            total_words = 1
        vulgarity_percentage = round((offensive_word_count / total_words) * 100, 2)
        if offensive_word_count == 0:
            vulgarity_label = "Clean"
        elif vulgarity_percentage < 10:
            vulgarity_label = "Low"
        elif vulgarity_percentage < 30:
            vulgarity_label = "Medium"
        else:
            vulgarity_label = "High"
        vulgarity = f"{vulgarity_label} ({vulgarity_percentage}%)"

        # Highlight offensive words in input text
        import re
        def highlight_offensive_words(text):
            def replacer(match):
                word = match.group(0).lower()
                if word in OFFENSIVE_WORDS_LIST:
                    return f'<span style="color: red; font-weight: bold;">{match.group(0)}</span>'
                return match.group(0)
            pattern = re.compile(r'\b\w+\b', re.IGNORECASE)
            return pattern.sub(replacer, text)
        highlighted_input = highlight_offensive_words(input_text)

        # --- Sentiment & Hate Speech Prediction ---
        sentiment_result = predict(input_text, mode='sentiment')
        hate_result = predict(input_text, mode='hate')
        sentiment = str(sentiment_result)
        hate_speech = str(hate_result)

        # --- Sentiment Emoji ---
        if sentiment.lower().startswith("positive"):
            sentiment_emoji = "😊"
            sentiment_score["Positive"] += 1
        elif sentiment.lower().startswith("neutral"):
            sentiment_emoji = "😐"
            sentiment_score["Neutral"] += 1
        elif sentiment.lower().startswith("negative"):
            sentiment_emoji = "😠"
            sentiment_score["Negative"] += 1
        else:
            sentiment_emoji = ""

        if hate_speech.lower().startswith("hate speech"):
            hate_score["Hate Speech"] += 1
        else:
            hate_score["None"] += 1

        # --- Charts ---
        # Pie chart for sentiment
        labels = ['Positive', 'Neutral', 'Negative']
        values = [sentiment_score['Positive'], sentiment_score['Neutral'], sentiment_score['Negative']]
        fig_pie = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.3)])
        pie_chart_div = pio.to_html(fig_pie, full_html=False)

        # Bar chart for offensive word frequency
        # Count frequency of each offensive word in input
        from collections import Counter
        offensive_freq = Counter([w for w in words if w in OFFENSIVE_WORDS_LIST])
        bar_labels = list(offensive_freq.keys()) if offensive_freq else OFFENSIVE_WORDS_LIST[:5]
        bar_values = list(offensive_freq.values()) if offensive_freq else [0]*5
        fig_bar = go.Figure(data=[go.Bar(x=bar_labels, y=bar_values)])
        fig_bar.update_layout(title='Offensive Word Frequency', xaxis_title='Word', yaxis_title='Count')
        bar_chart_div = pio.to_html(fig_bar, full_html=False)

        # Line chart (optional, same data)
        fig_line = go.Figure(data=[go.Scatter(x=bar_labels, y=bar_values, mode='lines+markers')])
        fig_line.update_layout(title='Offensive Word Frequency Trend', xaxis_title='Word', yaxis_title='Count')
        line_chart_div = pio.to_html(fig_line, full_html=False)

        # --- Render results on same page ---
        return render_template(
            'input.html',
            sentiment=sentiment,
            hate_speech=hate_speech,
            user_input=input_text,
            sentiment_score=sentiment_score,
            hate_score=hate_score,
            offensive_word_count=offensive_word_count,
            vulgarity=vulgarity,
            pie_chart_div=pie_chart_div,
            bar_chart_div=bar_chart_div,
            line_chart_div=line_chart_div,
            highlighted_input=highlighted_input,
            sentiment_emoji=sentiment_emoji,
            offensive_words_found=offensive_found
        )

    return render_template(
        'input.html',
        sentiment=sentiment,
        hate_speech=hate_speech,
        user_input=input_text,
        sentiment_score=sentiment_score,
        hate_score=hate_score,
        offensive_word_count=offensive_word_count,
        vulgarity=vulgarity,
        pie_chart_div=pie_chart_div,
        bar_chart_div=bar_chart_div,
        line_chart_div=line_chart_div,
        highlighted_input=highlighted_input,
        sentiment_emoji=sentiment_emoji,
        offensive_words_found=[]
    )

@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')

@app.route('/blog', methods=['GET'])
def blog():
    return render_template('blog.html')

@app.route('/contact', methods=['GET'])
def contact():
    return render_template('contact.html')

@app.route('/dashboard', methods=['GET'])
def dashboard():
    return render_template('dashboard.html')

@app.route('/export', methods=['GET'])
def export():
    return render_template('export.html')

if __name__ == '__main__':
    app.run(debug=True)
