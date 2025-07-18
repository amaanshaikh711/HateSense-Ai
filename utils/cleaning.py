import re
import pandas as pd
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords

stop_words = set(stopwords.words('english'))

def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"http\S+", "", text)  # remove links
    text = re.sub(r"@\w+", "", text)     # remove mentions
    text = re.sub(r"#\w+", "", text)     # remove hashtags
    text = re.sub(r"[^a-zA-Z\s]", "", text)  # remove emojis/symbols
    words = text.split()
    words = [w for w in words if w not in stop_words and len(w) > 2]
    return " ".join(words)


def load_and_clean_sentiment_data(filepath):
    df = pd.read_csv(filepath)
    df = df[['text', 'sentiment']]  # adjust column names if different
    df = df.dropna()
    df['clean_text'] = df['text'].apply(clean_text)
    return df


def load_and_clean_hate_data(filepath):
    df = pd.read_csv(filepath)
    df = df[['tweet', 'class']]  # adjust column names if different
    df = df.dropna()
    df['clean_text'] = df['tweet'].apply(clean_text)
    return df
