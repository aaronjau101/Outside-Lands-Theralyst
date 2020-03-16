#@title           Genre Info
#@author          Aaron Jauregui
#@description     Given a genre, will print artists with genre

#@input           None
#@output          Prints info on genre (artists)

import os
import json
import sys

YOUR_PATH = os.path.dirname(os.getcwd())

def getArtists(target):
    inFile = os.path.join(YOUR_PATH, "data//genresJSON.txt")

    with open(inFile) as f:
        data = json.load(f)

    for genre in data["genres"]:
        if genre["name"] == target:
            return genre["artists"]

    return None

def main():

    while True:
        genreName = input("Please enter the name of a genre:\n")
    
        SELECTED_GENRE = genreName.upper()
        
        artists = getArtists(SELECTED_GENRE)

        print("Genre Artists:")
        if artists == None:
            print("Not Found")
        else:
            print(", ".join(artists))

        repeat = ""
        while repeat != "y" and repeat != "n":
            repeat = input("Search for another genre? (y/n)")
        if repeat == "n":
            break
        
    print("Exiting Program")

if __name__ == '__main__':
    main()
