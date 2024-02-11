# Description: This file contains the code for the embedding of the text and the distance calculation between the embeddings.

# importing library
from openai import OpenAI
import numpy as np
from scipy import spatial
import numpy as np
from scipy import spatial

# setting up client
userAPI = input("Enter your API key: ")
client = OpenAI(api_key = userAPI)

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
# input: distance - np.ndarray, allString - list of strings
# output: list of strings
def nearest_neighbors(distance, allString):
    nearNeighbor = []
    # select the smallest 5 distance
    distance = distance[0:5]
    for i in distance:
        nearNeighbor.append(allString[i])
    return nearNeighbor

# target is the target string
# allString is the list of all the string embeddings lists
# all embeddings is the list of all the embeddings
def main(target, allString, allEmbeddings):

    targetEmbedding = embeddingDict[target]

    distances = distance_from_embeddings(targetEmbedding, allEmbeddings, distance_metric="cosine")

    index =  indicies_of_nearest_neighbors_from_distances(distances)

    return nearest_neighbors(index, allString)


#################### Embedding ####################

#  outputDict = {}
#  
#  embeddingFile = open("embedding.txt", "w", encoding='utf-8')
#  
#  company = {}
#  companyEmbedding = {}
#  
#  testing = {"aapl": "testing with appl", "msft": "testing with msft", "goog": "testing with goog"}
#  testingEmbedding = {}
#  
#  inputFile = open("output.txt", "r")
#  allString = inputFile.readlines()
#  for i in allString:
#      company[i.split("\t")[0]] = i.split("\t")[1]
#  
#  for key in testing:
#      testingEmbedding[key] = embedding_from_string(company[key], model="text-embedding-3-small")
#      embeddingFile.write(key + "\t" + str(testingEmbedding[key]) + "\n")
#  
#  for key in testingEmbedding:
#      outputDict[key] = main(testingEmbedding[key], list(testingEmbedding.values()))
#  
#  
#  print(outputDict)

##################### TESTING ####################

# simulating input 
# input format - dictionary of company ticker and company description
# testing = {"aapl": "testing with appl", "msft": "testing with msft", "goog": "testing with goog"}

# loading the input file
inputFile = open("output.txt", "r")

# get the input to be a dictionary
testing = {}

for i in inputFile.readlines():
    testing[i.split("\t")[0]] = i.split("\t")[1]


# loop through the dictionary to get a dictionary of embeddings
embeddingDict = {}

for key in testing:
    embeddingDict[key] = embedding_from_string(testing[key], model="text-embedding-3-small")

# get the list of all the embeddings
allTickers = list(embeddingDict.keys())
allEmbeddings = list(embeddingDict.values())

# loop through the dictionary to get the nearest neighbor
outputDict = {}
for key in embeddingDict:
    outputDict[key] = main(key, allTickers, allEmbeddings)

# list of all the values
allNightbors = list(outputDict.values())
finalOutput = {}
for x in range(len(allNightbors)):
    current = allNightbors[x]
    finalOutput[current[0]] = current[1:]


# writing to files
finalFile = open("finalOutput.txt", "w", encoding='utf-8')
for key in finalOutput:
    finalFile.write(key + "\t" + str(finalOutput[key]) + "\n")