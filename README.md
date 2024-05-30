# RxNorm Drug-Disease Relationship Harvesting and Corpus Generation

## Overview

This repository contains two main scripts that interact with the RxNorm APIs to harvest drug-disease relationships and 
convert them into a natural language corpus for language modeling.

1. **Graph Harvesting**:
   - **Description**: Given a list of drug names, this script retrieves their ingredients, interactions among those 
   ingredients, and their hierarchical relationships with associated diseases.
   - **Output**: A graph representation of the relationships and a lookup table for annotations.
   - **Script**: `harvest_graph.py`

2. **Corpus Generation**:
   - **Description**: This script converts the harvested graph into a plain text corpus by translating the relationships 
   into natural language sentences.
   - **Output**: A shuffled text file containing the natural language descriptions of the relationships.
   - **Script**: `generate_corpus.py`

## Resulting Corpora
1. [Ada version](https://github.com/Su-informatics-lab/drug_disease_graph/tree/cb704af6e1012e4e32acfedcb6658af8397eda95) 
is obtained by using the most recent three drugs from the population of the AUDIT-C scoring task. It has 3.6M tokens.
2. [Babbage version](https://github.com/Su-informatics-lab/drug_disease_graph/tree/3a598cb9d55ffbb52d2f16e61eafff4dfefaf5b1) 
is obtained by using all the drugs found on the Aou platform. It has 8.8M tokens.

## Authors

- **Author**: [hw56@indiana.edu](mailto:hw56@indiana.edu)
- **Version**: 0.0.1
- **License**: 0BSD
