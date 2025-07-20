# app.py

from flask import Flask, render_template, request
import nltk
from model.predict import predict

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

    if request.method == 'POST':
        import logging
        input_text = request.form['user_input']
        sentiment_result = predict(input_text, mode='sentiment')
        hate_result = predict(input_text, mode='hate')
        results = {
            "sentiment": sentiment_result,
            "hate_speech": hate_result,
            "input": input_text
        }
        if isinstance(results, dict):
            sentiment = results.get("sentiment", "")
            hate_speech = results.get("hate_speech", "")
        else:
            logging.error(f"Unexpected results type: {type(results)} with value: {results}")
            sentiment = ""
            hate_speech = ""

        # Convert to string to avoid AttributeError
        sentiment_str = str(sentiment)
        hate_speech_str = str(hate_speech)

        # Optionally update scores if needed
        if sentiment_str.startswith("Positive"):
            sentiment_score["Positive"] += 1
        elif sentiment_str.startswith("Neutral"):
            sentiment_score["Neutral"] += 1
        elif sentiment_str.startswith("Negative"):
            sentiment_score["Negative"] += 1

        if hate_speech_str.startswith("Hate Speech"):
            hate_score["Hate Speech"] += 1
        else:
            hate_score["None"] += 1

        return render_template(
            'input.html',
            sentiment=sentiment,
            hate_speech=hate_speech,
            user_input=input_text,
            sentiment_score=sentiment_score,
            hate_score=hate_score
        )

    return render_template(
        'input.html',
        sentiment=sentiment,
        hate_speech=hate_speech,
        user_input=input_text,
        sentiment_score=sentiment_score,
        hate_score=hate_score
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
