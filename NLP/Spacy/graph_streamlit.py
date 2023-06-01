import streamlit as st
import spacy
import networkx as nx
import matplotlib.pyplot as plt
from collections import Counter
import joblib

nlp = spacy.load('en_core_web_sm')

# Check if processed data is cached, otherwise process the data
try:
    doc = joblib.load('processed_data.joblib')
except FileNotFoundError:
    with open('brennu-njals_saga_en.txt', 'r', encoding='utf-8') as file:
        book_text = file.read()

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

# Construct the graph
character_pairs = Counter()
for sentence in doc.sents:
    sentence_characters = [entity.text for entity in sentence.ents if entity.label_ == 'PERSON']
    character_pairs.update([(character1, character2) for i, character1 in enumerate(sentence_characters) for character2 in sentence_characters[i + 1:]])

for (character1, character2), weight in character_pairs.items():
    if G.has_edge(character1, character2):
        G[character1][character2]['weight'] += weight
    else:
        G.add_edge(character1, character2, weight=weight)

# Get a list of nodes without edges
isolated_nodes = [node for node, degree in dict(G.degree()).items() if degree == 0]
G.remove_nodes_from(isolated_nodes)

def main():
    # Streamlit app
    st.title("Character Relations Network Graph")

    chosen_node = st.selectbox("Choose Character: ", list(G.nodes))

    subgraph_nodes = set(nx.single_source_shortest_path_length(G, chosen_node, cutoff=1))
    subgraph = G.subgraph(subgraph_nodes)

    # Get edge weights
    edge_weights = [subgraph[u][v]['weight'] for u, v in subgraph.edges()]

    # Normalize the edge weights to be within a specific range
    min_weight = min(edge_weights)
    max_weight = max(edge_weights)
    edge_weights_normalized = [(weight - min_weight) / (max_weight - min_weight) for weight in edge_weights]

    # Define the widths of the edges based on the normalized weights
    edge_widths = [1 + 3 * weight for weight in edge_weights_normalized]

    pos = nx.circular_layout(subgraph)  # Adjust layout algorithm as needed

    plt.figure(figsize=(12, 8))
    nx.draw_networkx(subgraph, pos, with_labels=True, node_size=500, font_size=10, width=edge_widths)
    edge_labels = nx.get_edge_attributes(subgraph, 'weight')
    nx.draw_networkx_edge_labels(subgraph, pos, edge_labels=edge_labels, font_size=8)

    plt.title(f'Character Relations Network Graph (Nodes within 1 Degrees of {chosen_node})')
    plt.axis('off')
    plt.tight_layout()
    st.pyplot(plt.gcf())

if __name__ == "__main__":
    main()
