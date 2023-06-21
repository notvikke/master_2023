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

def choose_relationship(node1,token,dif,relationship,dependancy):
    difference = abs(node1.i - token[1])
    if difference < dif:
        relationship = token[0]
        dependancy = token[2]
        dif = difference
    return relationship,dependancy,dif

def create_full_graph(doc):
    graph = nx.Graph()
    
    for entity in doc.ents:
        if entity.label_ == 'PERSON':
            graph.add_node(entity.text)

    # Iterate over the sentences and extract the connections between characters
    for sentence in doc.sents:
        sentence_characters = []

        for entity in sentence.ents:
            if entity.label_ == 'PERSON':
                sentence_characters.append(entity.text)

    for sent in doc.sents:
        sent_ents = [ent.text for ent in sent.ents if ent.label_ == 'PERSON']
        for i in range(len(sent_ents)):
            for j in range(i + 1, len(sent_ents)):
                node1 = sent_ents[i]
                node2 = sent_ents[j]
                
                if graph.has_edge(node1, node2):
                    graph[node1][node2]['weight'] += 1
                else:
                    graph.add_edge(node1, node2, weight=1)

                node1_token = None
                node2_token = None

                # Find the tokens corresponding to node1 and node2
                for token in sent:
                    if token.text == node1.split()[0]:
                        node1_token = token
                    if token.text == node2.split()[0]:
                        node2_token = token
                    if node1_token and node2_token:
                        break
                
                if graph.has_edge(node1, node2):
                    # Increment the weight of the edge if it already exists
                    graph[node1][node2]['weight'] += 1
                else:
                    # Add a new edge with weight 1 if it doesn't exist
                    graph.add_edge(node1, node2, weight=1)

                # Extract the relationship between the characters from the sentence
                relationship = ''
                dependancy = ''
                sent_token=[]

                for token in sent:
                    if  ((token.dep_ == 'attr'and token.text == 'son') or
                        (token.dep_ == 'nsubj'and token.pos_ == 'NOUN') or
                        (token.dep_ == 'poss'and token.pos_ == 'NOUN') or
                        (token.dep_ == 'conj'and token.pos_ == 'NOUN') or
                        (token.dep_ == 'appos'and token.pos_ == 'NOUN')):
                        sent_token.append([token.text,token.i,token.dep_])
                
                if (node1_token != None) & (node2_token != None):
                    dif = 100
                    for k in sent_token:
                        if (k[1] > node1_token.i) & (k[1] < node2_token.i):
                            relationship, dependancy, dif = choose_relationship(node1_token,k,dif,relationship,dependancy)
                    
                    dif = 100
                    if relationship == "":
                        for k in sent_token:
                            relationship, dependancy, dif = choose_relationship(node1_token,k,dif,relationship,dependancy)

                # Assign the relationship name as an edge attribute
                graph[node1][node2]['relationship'] = relationship

    # Get a list of nodes without edges
    isolated_nodes = [node for node, degree in dict(graph.degree()).items() if degree == 0]
    graph.remove_nodes_from(isolated_nodes)

    return graph

def create_subgraph(graph, chosen_person):
    # Get the neighbors of the chosen_person
    neighbors = list(graph.neighbors(chosen_person))
    neighbors.append(chosen_person)
    
    subgraph = graph.subgraph(neighbors)

    node_colors = ['#6fa8dc' if node != chosen_person else 'red' for node in subgraph.nodes]

    return subgraph, node_colors

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

G = create_full_graph(doc)

isolated_nodes = [node for node, degree in dict(G.degree()).items() if degree == 0]
G.remove_nodes_from(isolated_nodes)

def main():
    # Streamlit app
    st.image("images/logo.png", width=600)

    chosen_node = st.selectbox("Choose or type a character's name: ", list(G.nodes))

    st.markdown("(If unsure who to check, try Wolf, Gunnhillda, King Brian or Gunnar)")
    st.markdown("After choosing, please be patient, it will take around two minutes or so...")

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

    subgraph, node_colors = create_subgraph(G, chosen_node)

    if style == "weight":
        # Get edge weights
        edge_weights = [subgraph[u][v]['weight'] for u, v in subgraph.edges()]

        # Normalize the edge weights to be within a specific range
        min_weight = min(edge_weights)
        max_weight = max(edge_weights)
        edge_weights_normalized = [(weight - min_weight) / (max_weight - min_weight) for weight in edge_weights]

        edge_widths = [1 + 3 * weight for weight in edge_weights_normalized]
    else:   
        edge_widths = 1
    
    pos = nx.spring_layout(subgraph, seed=0)  # Adjust layout algorithm as needed

    plt.figure(figsize=(12, 8))
    nx.draw_networkx(subgraph, pos, with_labels=True, node_size=1000, font_size=10,width=edge_widths, node_color=node_colors)
    edge_labels = nx.get_edge_attributes(subgraph, style)
    nx.draw_networkx_edge_labels(subgraph, pos, edge_labels=edge_labels, font_size=8)
    plt.title(f'{chosen_node} Relations Network Graph')
    plt.axis('off')
    plt.tight_layout()
    st.pyplot(plt.gcf())

if __name__ == "__main__":
    main()
