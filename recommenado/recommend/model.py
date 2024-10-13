from typing import List
import numpy as np

import google.generativeai as genai
from recommenado.recommend.db import read_db

# Configure genai with api key https://aistudio.google.com/app/apikey
# TODO: provide docs on how to securely store key elsewhere
# TODO: provide docs on how to generate one's own key
genai.configure(api_key="")

# Embed article text using the SAME model that embeddeded original article
# README links out to example docs (https://ai.google.dev/gemini-api/docs/embeddings) using 
# `models/text-embedding-004`, so I will assume that's the correct model
# Setting this with "constant" case since we probably won't be storing embeddings from multiple models
MODEL: str = 'models/text-embedding-004'

def semantic_match(text: str) -> List[int]:
    """
    Given an article text, identify semantic matches for an article:
    1. Leverage a google genai model and a 'semantic_similarity' task type to generate embeddings for input
    3. Compare generated embeddings to db embeddings using cosine distance calculation
    4. Return the 2 most similar matches

    Implementation notes: 
    * I am noticing that the vectors from the text-embedding-004 model are not the same length
    as the vectors from the articlesembeds.csv database. This makes me skeptical of the accuracy of my distance calc
    * I've used cosine distance to calculate the similarity of short vectorized phrases before, but I am not sure
    if it represents the best algorithm for this use case
    """    

    # Data structures that houses semantic matches
    distances = []

    # Generate embedding from article input
    embedding = genai.embed_content(model=MODEL, content=text, task_type='semantic_similarity')['embedding']
    
    # For each article in the database, calculate semantic distance to input article
    csvfile, articlereader = read_db()
    for row in articlereader:
        article = row[0]
        comparison_embedding: List[float] = list(map(float, row[1].split(","))) # Cast to a list of floats
        # Calculate distance to the incoming article
        distance = cosine_distance(embedding, comparison_embedding)
        distances.append({"article": article, "distance": distance})
    # Close csv file
    csvfile.close()

    # Sort results by distance, ascending order
    distances.sort(key=lambda x: x['distance'])
    
    # Return the top 2 semantic matches
    return distances[:2]
    

def cosine_distance(vec1: np.array, vec2: np.array) -> float:
    """
    Calculate cosine distance between two vectors

    TODO: this can likely be optimized
    """
    dot_product = np.dot(vec1, vec2)
    norm_a = np.linalg.norm(vec1)
    norm_b = np.linalg.norm(vec2)

    cosine_similarity = dot_product / (norm_a * norm_b)

    cosine_distance = 1 - cosine_similarity

    return cosine_distance

def embed_text(text: str) -> List[float]:
