# RxNorm Drug-Disease Relationship Harvesting and Corpus Generation

## Overview

This repository contains two main scripts that interact with the RxNorm APIs to harvest drug-disease relationships and 
convert them into a natural language corpus for language modeling.

1. **Graph Harvesting**:
   - **Description**: Given a list of drug names, this script retrieves their ingredients, interactions among those 
   ingredients, and their hierarchical relationships with associated diseases.
   - **Output**: A graph representation of the relationships and a lookup table for annotations.
   - **Script**: `run.py`

2. **Corpus Generation**:
   - **Description**: This script converts the harvested graph into a plain text corpus by translating the relationships 
   into natural language sentences.
   - **Output**: A shuffled text file containing the natural language descriptions of the relationships.
   - **Script**: `graph2corpus.py`


## Authors

- **Author**: [hw56@indiana.edu](mailto:hw56@indiana.edu)
- **Version**: 0.0.1
- **License**: 0BSD
