#@title           Artist Frequency
#@author          Aaron Jauregui
#@description     Read in all OL years list of artists
#                 Write files with artist information

#@input           None
#@output          1)JSON file with artist name, number of years artist came to OL, array of years
#                 2)File with list of all artists (alphabetical)
#                 3)File with list of all artists with multiple years

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

#Function to read all OL year files and create JSON object for artists
def createArtistJSON():
    TEXT_DIR = os.path.join(YOUR_PATH, "text//")

    data = {}
    data["artists"] = []
    
    for filename in os.listdir(TEXT_DIR):
        content = open(os.path.join(TEXT_DIR, filename), 'r')
        for lines in content:
            artist = lines.strip().upper()
            year = filename[:-4]
            artists = [a["name"] for a in data["artists"]]
            if artist in artists:
                index = next((i for (i, d) in enumerate(data["artists"]) if d["name"] == artist), None)
                data["artists"][index]["years"].append(year)
            else:
                data["artists"].append({
                    "name": artist,
                    "years": [year]
                })
    return data

#Function to neatly display artist info
def displayArtist(artist):
    name = artist["name"]
    numberOfYears = len(artist["years"])
    years = ", ".join(artist["years"])
    return "{}, {} years, {}".format(name, numberOfYears, years)

def main():
    print("Starting Artist Frequency Program")
    start_time = time.time()
    #Creates a JSON obj with artist and their years attended
    artists = createArtistJSON()

    #Dumps JSON obj to a file
    JSON_FILE = os.path.join(YOUR_PATH, "data//artistFrequencyJSON.txt")
    dumpJSON(JSON_FILE, artists)

    #List of (alphabetically sorted) artist names written to a file
    ALL_FILE = os.path.join(YOUR_PATH, "data//allArtists.txt")
    allArtists = [artist["name"] for artist in artists["artists"]]
    writeSortedArray(ALL_FILE, allArtists)

    #List of artist (and their years) with duplicate years written to a file
    DUPE_FILE = os.path.join(YOUR_PATH, "data//duplicateYears.txt")
    dupeArtists = [displayArtist(artist) for artist in artists["artists"] if len(artist["years"]) > 1]
    writeSortedArray(DUPE_FILE, dupeArtists)
    print("Program took " + str(time.time() - start_time) + " seconds")

if __name__ == '__main__':
    main()
