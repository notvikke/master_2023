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
    st.image("images/logo.png", width=600)
    # Streamlit app
    st.subheader("Demo")

    characters = ["King Brian","Gunnhillda","Thorgrim"]

    chosen_character = st.selectbox("Choose or type a character's name: ", characters)

    col1,col2 = st.columns(2)
    with col1:
        relationship_button = st.button("Relationship")
    with col2:
        weight_button = st.button("Frequency")

    style = "relationship"

    if relationship_button:
        style = "relationship"
    if weight_button:
        style = "weight"

    st.image(f"graphs/{chosen_character}_{style}.png")

    descriptions = {"King Brian":{"Born":"c. 941 Kincora, Cill Dalua, Kingdom of Munster","Died":"23 April 1014 Cluain Tarbh, Kingdom of Leinster","summary":"King Brian was an Irish king who ended the domination of the High Kingship of Ireland by the Uí Néill, and probably ended Viking invasions of Ireland.[2] Brian built on the achievements of his father, Cennétig mac Lorcain, and especially his elder brother, Mathgamain. Brian first made himself king of Munster, then subjugated Leinster, eventually becoming High King of Ireland. He was the founder of the O'Brien dynasty, and is widely regarded as one of the most successful and unifying monarchs in medieval Ireland."},
                    "Gunnhillda":{"Born":"c. 910 \n Jutland, Denmark","Died":"c. 980 Orkney, Scotland","summary":"Gunnhildr konungamóðir (mother of kings) or Gunnhildr Gormsdóttir,[1] whose name is often Anglicised as Gunnhild (c. 910 - c. 980) is a quasi-historical figure who appears in the Icelandic Sagas, according to which she was the wife of Eric Bloodaxe (king of Norway 930–34, 'King' of Orkney c. 937–54, and king of Jórvík 948–49 and 952–54). She appears prominently in sagas such as Fagrskinna, Egils saga, Njáls saga, and Heimskringla. The sagas relate that Gunnhild lived during a time of great change and upheaval in Norway. Her father-in-law Harald Fairhair had recently united much of Norway under his rule.[2] Shortly after his death, Gunnhild and her husband Eric Bloodaxe were overthrown and exiled. She spent much of the rest of her life in exile in Orkney, Jorvik and Denmark. A number of her many children with Eric became co-rulers of Norway in the late tenth century."},
                    "Thorgrim":{"Born":"n/a","Died":"n/a","summary":"n/a"}}

    st.sidebar.subheader(f"{chosen_character}")
    st.sidebar.image(f"images/{chosen_character}.jpg",width=200)
    
    st.sidebar.subheader("Born")
    st.sidebar.write(descriptions.get(chosen_character).get("Born"))
    st.sidebar.subheader("Died")
    st.sidebar.write(descriptions.get(chosen_character).get("Died"))
    st.sidebar.subheader("Summary")
    st.sidebar.write(descriptions.get(chosen_character).get("summary"))


if __name__ == "__main__":
    main()
