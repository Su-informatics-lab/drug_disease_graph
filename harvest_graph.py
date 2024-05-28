"""
Given a list of drug names as strings, this module retrieves their ingredients,
the interactions among those ingredients, and their hierarchical relationships
associated with diseases using the RxNorm APIs.
"""

__author__ = "hw56@indiana.edu"
__version__ = "0.0.1"
__license__ = "0BSD"

import json
import requests
import networkx as nx
import time
from tqdm import tqdm

def get_rxcui_by_name(drug_name):
    base_url = "https://rxnav.nlm.nih.gov/REST/rxcui.json"
    params = {"name": drug_name}
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        if 'idGroup' in data and 'rxnormId' in data['idGroup']:
            return data['idGroup']['rxnormId'][0]
    return None

def get_classes_by_rxcui(rxcui):
    base_url = f"https://rxnav.nlm.nih.gov/REST/rxclass/class/byRxcui.json"
    params = {"rxcui": rxcui}
    response = requests.get(base_url, params=params)
    classes = []
    if response.status_code == 200:
        data = response.json()
        if 'rxclassDrugInfoList' in data:
            for item in data['rxclassDrugInfoList']['rxclassDrugInfo']:
                class_id = item['rxclassMinConceptItem']['classId']
                class_name = item['rxclassMinConceptItem']['className']
                relation = item.get('rela', 'related_to')
                classes.append((class_id, class_name, relation))
    return classes

def get_class_contexts(class_id):
    base_url = f"https://rxnav.nlm.nih.gov/REST/rxclass/classContext.json"
    params = {"classId": class_id}
    response = requests.get(base_url, params=params)
    contexts = []
    if response.status_code == 200:
        data = response.json()
        if 'classPathList' in data:
            for path in data['classPathList']['classPath']:
                context = [(concept['classId'], concept['className'])
                           for concept in path['rxclassMinConcept']]
                contexts.append(context)
    return contexts

def get_class_members(class_id):
    base_url = f"https://rxnav.nlm.nih.gov/REST/rxclass/classMembers.json"
    params = {"classId": class_id}
    response = requests.get(base_url, params=params)
    members = []
    if response.status_code == 200:
        data = response.json()
        if 'drugMemberGroup' in data:
            for member in data['drugMemberGroup']['drugMember']:
                members.append((member['minConcept']['rxcui'],
                                member['minConcept']['name'],
                                member.get('rela', 'related_to')))
    return members

def dfs(graph, class_id, visited, lookup):
    if class_id in visited:
        return
    visited.add(class_id)
    members = get_class_members(class_id)
    time.sleep(.1)  # delay to avoid overwhelming the API
    for rxcui, name, relation in members:
        graph.add_node(rxcui, label=name)
        graph.add_edge(class_id, rxcui, relation=relation)
        lookup[rxcui] = name
    contexts = get_class_contexts(class_id)
    time.sleep(.1)  # delay to avoid overwhelming the API
    for context in contexts:
        for sub_class_id, sub_class_name in context:
            if sub_class_id not in visited:
                graph.add_node(sub_class_id, label=sub_class_name)
                graph.add_edge(class_id, sub_class_id, relation='is_a')
                lookup[sub_class_id] = sub_class_name
                dfs(graph, sub_class_id, visited, lookup)

if __name__ == "__main__":
    drugs = json.load(open('audit_c_threeDrugs_deduplicated.json'))
    no_matches = []
    visited = set()
    graph = nx.DiGraph()
    lookup = {}  # lookup table for annotations

    for drug in tqdm(drugs):
        for d in drug.split(' / '):
            rxcui = get_rxcui_by_name(d)
            time.sleep(.1)  # delay to avoid overwhelming the API
            if rxcui:
                classes = get_classes_by_rxcui(rxcui)
                time.sleep(.1)  # delay to avoid overwhelming the API
                graph.add_node(rxcui, label=d)
                lookup[rxcui] = d
                for class_id, class_name, relation in classes:
                    graph.add_node(class_id, label=class_name)
                    graph.add_edge(rxcui, class_id, relation=relation)
                    lookup[class_id] = class_name
                    dfs(graph, class_id, visited, lookup)
            else:
                no_matches.append(d)

    # save the graph to a GraphML file
    nx.write_graphml(graph, "drug_disease_graph.graphml")
    print(f"Graph of {graph.number_of_nodes()} nodes and {graph.number_of_edges()} "
          f"edges saved to drug_disease_graph.graphml")

    # save the lookup table to a JSON file
    json.dump(lookup, open("lookup_table.json", "w"))
    print(f"Lookup table of {len(lookup)} mappings saved to lookup_table.json")

    # save no matches to a JSON file
    json.dump(no_matches, open("no_matches.json", "w"))
    print(f"{len(no_matches)} drugs with no matches saved to no_matches.json")