"""
This module converts the harvested graph into a plain text corpus.
"""

import networkx as nx

__author__ = "hw56@indiana.edu"
__version__ = "0.0.1"
__license__ = "0BSD"


def read_graph(graphml_file):
    return nx.read_graphml(graphml_file)


def relationship_to_natural_language(relation, object):
    relation_mapping = {
        "is_a": f"is a type of {object}",
        "isa_therapeutic": f"is used as a therapeutic agent for {object}",
        "isa_disposition": f"has the disposition of {object}",
        "isa_structure": f"contains structural components of {object}",
        "may_treat": f"may be used to treat {object}",
        "ci_with": f"is contraindicated with {object}",
        "has_ingredient": f"contains the ingredient {object}",
        "has_pe": f"has the physiological effect of {object}",
        "has_moa": f"has the mechanism of action {object}",
        "has_epc": f"has the established pharmacologic class {object}"
    }
    return relation_mapping.get(relation, f"has an unknown relationship with {object}")


def create_sentences(graph):
    sentences = []
    missing_relationships = 0
    for node in graph.nodes(data=True):
        node_id = node[0]
        node_label = node[1].get('label', node_id)

        for neighbor in graph.neighbors(node_id):
            edge_data = graph.get_edge_data(node_id, neighbor)
            relation = edge_data.get('relation', 'unknown')
            neighbor_label = graph.nodes[neighbor].get('label', neighbor)

            sentence = f"{node_label} {relationship_to_natural_language(relation, neighbor_label)}."
            sentences.append(sentence)

            if relation == 'unknown':
                missing_relationships += 1

    return sentences, missing_relationships


def save_sentences(sentences, filename):
    with open(filename, 'w') as f:
        for sentence in sentences:
            f.write(sentence + '\n')


if __name__ == "__main__":
    graph_file = "drug_disease_graph.graphml"

    # read the graph
    graph = read_graph(graph_file)
    result = create_sentences(graph)
    sentences = result[0]
    missing_relationships = result[1]

    # save sentences to a text file
    save_sentences(sentences, "rxnorm.txt")
    print(f"Sentences saved to rxnorm.txt")
    print(f"Number of sentences: {len(sentences)}")
    print(f"Number of missing relationships: {missing_relationships}")
