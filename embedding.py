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



def main(target, allString):

    embeddings = [embedding_from_string(string, model="text-embedding-3-small") for string in allString]
    query_embedding = embedding_from_string(target, model="text-embedding-3-small")

    distances = distance_from_embeddings(query_embedding, embeddings, distance_metric="cosine")

    return indicies_of_nearest_neighbors_from_distances(distances)


#################### TESTING ####################
allString = ["testing", "another", "maybe", "this", "a lot"]
target = "much"

main(target, allString)


# response = client.embeddings.create(
#     input="Your text string goes here",
#     model="text-embedding-3-small"
# )
# 
# print(response.data[0].embedding)

