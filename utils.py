import requests
import logging
import json
from py2neo import Node, Relationship

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


spotify_api_url = "https://api.spotify.com/v1/"
artists_endpoint = "artists/"
related_artists_endpoint = "/related-artists"


def getArtistJson(artist_id):
	""" Returns a json representation of the artist response for an artist_id """
	request_url = spotify_api_url + artists_endpoint + artist_id
	return getJsonResponse(request_url)	

def getRelatedArtistJson(artist_id):
	""" Returns a json representation of the related_artists response for an artist_id """	
	request_url = spotify_api_url + artists_endpoint + artist_id + related_artists_endpoint	
	return getJsonResponse(request_url)	

def getJsonResponse(request_url):
	logger.info("Getting json: " + request_url)
	response = requests.get(request_url)
	return json.loads(response.text)	

def createArtistNode(graph, artist_json):
	artist_node = Node(artist_json["type"])
	artist_node.properties["name"] = artist_json["name"]
	artist_node.properties["href"] = artist_json["href"]
	artist_node.properties["external_href"] = artist_json["external_urls"]["spotify"]
	artist_node.properties["spotify_id"] = artist_json["id"]
	artist_node.properties["href"] = artist_json["href"]

	# Insert into the db
	graph.create(artist_node)

	# return the node
	return artist_node

def createRelatedArtistNodes(graph, artist_node, related_artist_json):
	for related_artist_json in related_artist_json["artists"]:
		related_artist_node = createArtistNode(graph, related_artist_json)

		relationship = Relationship(artist_node, "RELATED TO", related_artist_node)
		graph.create(relationship)

