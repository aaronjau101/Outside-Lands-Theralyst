#@title           Genre Counter
#@author          Aaron Jauregui
#@description     Read in a JSON file with artist and their genres
#                 Write files with genre information

#@input           None
#@output          1)JSON file with genre name, number of artists with genre, array of artist names
#                 2)File with list of all genres (alphabetical)
#                 3)File with list of all artists (alphabetical) without a genre

import os
import json
import time

YOUR_PATH = os.path.dirname(os.getcwd())

#Function to dump JSON obj to file
def dumpJSON(outfile, obj):
    with open(outfile, 'w') as oFile:
        json.dump(obj, oFile, ensure_ascii=False)

#Function to write a sorted list to file 
def writeSortedArray(outfile, array):
    oFile = open(outfile, 'w')
    for i in sorted (array):
        oFile.write("{}\n".format(i))
    oFile.close()

#Function to read JSON artist genres info and create JSON object for genres
def createGenresJSON(artists):
    data = {}
    data["genres"] = []

    for artist in artists["artists"]:
        for genre in artist["genres"]:
            genres = [g["name"] for g in data["genres"]]
            if genre not in genres:
                data["genres"].append({
                    "name": genre,
                    "artists": [artist["name"]]
                })
            else:
                index = next((i for (i, d) in enumerate(data["genres"]) if d["name"] == genre), None)
                if index != None:
                    data["genres"][index]["artists"].append(artist["name"])
    return data

#Function to load and return JSON obj with artists and their genres
def loadArtistsJSON():
    ARTIST_JSON_FILE = os.path.join(YOUR_PATH, "data//artistsGenresJSON.txt")

    with open(ARTIST_JSON_FILE) as f:
        data = json.load(f)

    return data

def main():
    print("Starting Genre Counter Program")
    start_time = time.time()
    #Loads JSON obj with artists and their genres
    artists = loadArtistsJSON()
    
    #Creates a JSON obj with genres and their artists
    genres = createGenresJSON(artists)

    #Dumps JSON obj to a file
    GENRES_JSON_FILE = os.path.join(YOUR_PATH, "data//genresJSON.txt")
    dumpJSON(GENRES_JSON_FILE, genres)

    #List of (alphabetically sorted) genres written to a file
    ALL_FILE = os.path.join(YOUR_PATH, "data//allGenres.txt")
    allGenres = [genre["name"] for genre in genres["genres"]]
    writeSortedArray(ALL_FILE, allGenres)

    #List of (alphabetically sorted) artist with no genres written to a file
    NOGENRE_FILE = os.path.join(YOUR_PATH, "data//noGenreArtists.txt")
    noGenreArtists = [artist["name"] for artist in artists["artists"] if len(artist["genres"]) == 0]
    writeSortedArray(NOGENRE_FILE, noGenreArtists)
    print("Program took " + str(time.time() - start_time) + " seconds")

if __name__ == '__main__':
    main()
