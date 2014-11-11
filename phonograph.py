import requests
import bs4
import logging
import re
import datetime
import json
import utils
from py2neo import Graph


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Beck
starting_id = "3vbKDsSS70ZX9D2OcvbZmS"

logger.info("Starting!")

#with open('spotify_client_secret.txt', 'r') as spotify_client_secret_file:
#    spotify_client_secret = spotify_client_secret_file.read()

logger.info("Getting info for Beck...")

graph = Graph()

# Get artist info
artist_json = utils.getArtistJson(starting_id)
artist_node = utils.createArtistNode(graph, artist_json)
graph.create(artist_node)

# Get related artist info
related_artist_json = utils.getRelatedArtistJson(artist_node.properties["spotify_id"])
utils.createRelatedArtistNodes(graph, artist_node, related_artist_json)


logger.info("Done!")


