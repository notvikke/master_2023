import streamlit as st
import spacy
import networkx as nx
import matplotlib.pyplot as plt
from collections import Counter
import joblib

def install_spacy_model():
    try:
        nlp = spacy.load("en_core_web_sm")
    except OSError:
        # Model not found, download and install
        from spacy.cli import download
        download("en_core_web_sm")
        spacy.prefer_gpu()

install_spacy_model()

# Check if processed data is cached, otherwise process the data
try:
    doc = joblib.load('processed_data.joblib')
except FileNotFoundError:
    with open('NLP/Spacy/brennu-njals_saga_en.txt', 'r', encoding='utf-8') as file:
        book_text = file.read()

    nlp = spacy.load("en_core_web_sm")
    doc = nlp(book_text)
    joblib.dump(doc, 'processed_data.joblib')

# Preprocess data
characters = []
for entity in doc.ents:
    if entity.label_ == 'PERSON':
        characters.append(entity.text)

counter = Counter(characters)

# Create the graph
G = nx.Graph()
G.add_nodes_from(characters)


def main():
    # Streamlit app
    st.title("Character Relations Network Graph")

    chosen_node = st.selectbox("Choose or type a character's name: ", list(G.nodes))

    st.markdown("After choosing, please be patient, it will take a minute or so...")


if __name__ == "__main__":
    main()
