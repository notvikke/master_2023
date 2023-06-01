from flask import Flask, render_template
import spacy
from collections import Counter

# Load the English language model
nlp = spacy.load('en_core_web_sm')

# Initialize the Flask application
app = Flask(__name__)

# Route for the home page
@app.route('/')
def home():
    # Read the text from the .txt file
    with open('great_gatsby.txt', 'r', encoding='utf-8') as file:
        text = file.read()

    # Process the text with spaCy
    doc = nlp(text)

    # Set of suffixes to exclude
    suffixes = {'ly', 'ing', 'ed', 's'}

    # Identify the characters using named entity recognition
    characters = []
    for entity in doc.ents:
        if entity.label_ == 'PERSON':
            # Normalize the character name to title case
            character = entity.text.title()
            # Split the character name into words and pass through spaCy's pipeline for POS tagging
            words = nlp(character)
            # Filter out words that have less than three characters, exclude adjectives, pronouns, verbs, conjunctions, nouns, names of cities, and words with suffixes
            valid_words = [word.text for word in words if len(word.text) >= 3 and word.pos_ != 'ADJ' and word.pos_ != 'PRON' and word.pos_ != 'VERB' and word.pos_ != 'CCONJ' and word.pos_ != 'NOUN' and word.text.lower() not in cities and not any(word.text.endswith(suffix) for suffix in suffixes)]
            # Limit the character name to two words
            if len(valid_words) == 2:
                character = ' '.join(valid_words)
                characters.append(character)

    # Count the occurrences of each character
    character_counts = Counter(characters)

    # Sort the characters by frequency
    sorted_characters = sorted(character_counts.items(), key=lambda x: x[1], reverse=True)

    # Render the template with the identified characters and their frequencies
    return render_template('index.html', characters=sorted_characters)

if __name__ == '__main__':
    app.run(debug=True)