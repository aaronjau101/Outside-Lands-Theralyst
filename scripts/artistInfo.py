#@title           Artist Info
#@author          Aaron Jauregui
#@description     Given an artist name, will print artist info if found

#@input           Artist Name
#@output          Prints info on artist (OL years, genres)

import os
import json
import sys

YOUR_PATH = os.path.dirname(os.getcwd())

def getYears(target):
    inFile = os.path.join(YOUR_PATH, "data//artistFrequencyJSON.txt")

    with open(inFile) as f:
        data = json.load(f)

    for artist in data["artists"]:
        if artist["name"] == target:
            return artist["years"]

    return None

def getGenres(target):
    inFile = os.path.join(YOUR_PATH, "data//artistsGenresJSON.txt")

    with open(inFile) as f:
        data = json.load(f)

    for artist in data["artists"]:
        if artist["name"] == target:
            return artist["genres"]

    return None

def main():
    if(len(sys.argv) < 2):
        print("Program requires an artist name")
        print("For example:")
        print("python artistInfo.py \"Foo Fighters\"")
        return;

    SELECTED_ARTIST = sys.argv[1].upper()
    
    years = getYears(SELECTED_ARTIST)

    print("Artist Years:")
    if years == None:
        print("Not Found")
    else:
        print(", ".join(years))

    genres = getGenres(SELECTED_ARTIST)

    print("Artist Genres:")
    if genres == None or len(genres) == 0:
        print("Not Found")
    else:
        print(", ".join(genres))
    

if __name__ == '__main__':
    main()
