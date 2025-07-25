import re
import csv
from collections import Counter

# Load offensive words from labeled_data.csv and categorize them
def load_offensive_words(filepath='data/hated speech/labeled_data.csv'):
    import logging
    categories = {
        'slurs': set(),
        'insults': set(),
        'profanities': set()
    }
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                word = row.get('word', '').strip().lower()
                category = row.get('category', '').strip().lower()
                if word and category in categories:
                    categories[category].add(word)
        logging.info(f"Loaded offensive words from {filepath}: { {k: len(v) for k,v in categories.items()} }")
    except Exception as e:
        logging.error(f"Error loading offensive words from {filepath}: {e}")
    return categories

# Preload offensive words once
OFFENSIVE_WORDS = load_offensive_words()

def count_offensive_words(text):
    """
    Count offensive words in text by category.
    Returns a dict with counts per category and total count.
    """
    text = text.lower()
    words = re.findall(r'\b\w+\b', text)
    counts = {cat: 0 for cat in OFFENSIVE_WORDS}
    for word in words:
        for category, word_set in OFFENSIVE_WORDS.items():
            if word in word_set:
                counts[category] += 1
    total = sum(counts.values())
    counts['total'] = total
    return counts

def calculate_vulgarity_level(offensive_counts):
    """
    Calculate vulgarity level as percentage and label.
    Percentage = (total offensive words / total words) * 100
    Labels:
      0-30%: Mild
      31-70%: Moderate
      71-100%: Severe
    """
    total_offensive = offensive_counts.get('total', 0)
    total_words = sum(offensive_counts.values()) - total_offensive  # sum of categories excluding total
    # To avoid division by zero, count total words from text length if needed
    # Here, approximate total words as total_offensive + 100 (fallback)
    total_words = total_words + total_offensive if total_words > 0 else total_offensive + 100
    percentage = (total_offensive / total_words) * 100 if total_words > 0 else 0

    if percentage <= 30:
        label = "Mild"
    elif percentage <= 70:
        label = "Moderate"
    else:
        label = "Severe"

    return round(percentage, 2), label
