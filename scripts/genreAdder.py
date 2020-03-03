#@title           Genre Adder
#@author          Aaron Jauregui
#@description     Read in a JSON file with artist and their genres
#                 Also read in csv file with more genres for artist
#                 Write new JSON file with more genres

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
def createArtistsJSON(artists, genres):
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

#Function to load CSV file and return JSON obj with artists and their genres
def loadGenresCSV():
    GENRES_CSV_FILE = os.path.join(YOUR_PATH, "data//genreAdder.csv")

    data = {}
    data["artists"] = []
    
    content = open(GENRES_CSV_FILE, "r")

    for line in content:
        cols = line.split(",")
        artist = cols[0]
        genres = []
        index = 1
        while index < len(cols):
            genre = cols[index].strip().upper()
            if genre != '':
                genres.append(genre)
            index += 1
        print("{} : {}".format(artist, genres))
        
    return data

#Function to load and return JSON obj with artists and their genres
def loadArtistsJSON():
    ARTIST_JSON_FILE = os.path.join(YOUR_PATH, "data//artistsGenresJSON.txt")

    with open(ARTIST_JSON_FILE) as f:
        data = json.load(f)

    return data

def main():
    print("Starting Genre Adder Program")
    start_time = time.time()
    #Loads JSON obj with artists and their genres
    artists = loadArtistsJSON()

    #Loads CSV file with artist and genres to be added
    genres = loadGenresCSV()
    
    #Creates a JSON obj with genres and their artists
    #newArtists = createArtistsJSON(artists, genres)

    #Dumps JSON obj to a file
    #GENRES_JSON_FILE = os.path.join(YOUR_PATH, "data//genresJSON.txt")
    #dumpJSON(GENRES_JSON_FILE, genres)


    print("Program took " + str(time.time() - start_time) + " seconds")

if __name__ == '__main__':
    main()
