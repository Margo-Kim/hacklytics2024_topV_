# Description: This file contains the code for the embedding of the text and the distance calculation between the embeddings.

# importing library
from openai import OpenAI
import numpy as np
from scipy import spatial

# setting up client
client = OpenAI(api_key = "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")

# parent function of getting embedding from strings
# input: string - string
# output: embedding - embedding object
def embedding_from_string(string: str, model="text-embedding-3-small"):
    response = client.embeddings.create(input=string, model=model)
    return response.data[0].embedding

# def distances_from_embeddings(
#     query_embedding: List[float],
#     embeddings: List[List[float]],
#     distance_metric="cosine",
# ) -> List[List]:
#     """Return the distances between a query embedding and a list of embeddings."""

def distance_from_embeddings(query_embedding, embeddings, distance_metric="cosine"):
    distance_metrics = {
        "cosine": spatial.distance.cosine,
        "L1": spatial.distance.cityblock,
        "L2": spatial.distance.euclidean,
        "Linf": spatial.distance.chebyshev,
    }
    distances = [distance_metrics[distance_metric](query_embedding, embedding) for embedding in embeddings]
    return distances


# def indices_of_nearest_neighbors_from_distances(distances) -> np.ndarray:
#     """Return a list of indices of nearest neighbors from a list of distances."""
#     return np.argsort(distances)

def indicies_of_nearest_neighbors_from_distances(distances):
    return np.argsort(distances)

# define a function that match the index of the nearest neighbor with the original string
# input: target - string, allString - list of strings
# output: list of strings
def nearest_neighbors(distance, allString):
    nearNeighbor = []
    # select the smallest 5 distances
    for i in distance:
        if i < 5:
            nearNeighbor.append(allString[i])
    return nearNeighbor



def main(target, allString):

    embeddings = [embedding_from_string(string, model="text-embedding-3-small") for string in allString]
    query_embedding = embedding_from_string(target, model="text-embedding-3-small")

    distances = distance_from_embeddings(query_embedding, embeddings, distance_metric="cosine")

    index =  indicies_of_nearest_neighbors_from_distances(distances)

    return [target] + nearest_neighbors(index, allString)


#################### TESTING ####################
allString = ["testing", "another", "maybe", "this", "a lot", "much", "very", "so", "many", "more"]
target = "much"

print(main(target, allString))

# [5 4 9 6 8 3 2 1 7 0]

