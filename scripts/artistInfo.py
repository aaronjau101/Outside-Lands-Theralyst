#@title           Artist Info
#@author          Aaron Jauregui
#@description     Given an artist name, will print artist info if found

#@input           None
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

def getSuggestions(target):
    inFile = os.path.join(YOUR_PATH, "data//artistsGenresJSON.txt")
    
    with open(inFile) as f:
        data = json.load(f)

    suggestions = []
    
    for artist in data["artists"]:
        name = artist["name"]
        if getDifferences(name, target) < 3:
            suggestions.append(name)

    return suggestions

def getDifferences(word1, word2):
    diff = 0
    array1 = [char for char in word1]
    array2 = [char for char in word2]
    
    for letter in array1:
        if letter in array2:
            array2.remove(letter)
        else:
            diff += 1

    diff += len([i for i in array2 if i != " "])
    return diff

def main():

    while True:
        artistName = input("Please enter the name of an artist:\n")
    
        SELECTED_ARTIST = artistName.upper()
        
        years = getYears(SELECTED_ARTIST)

        print("Artist Years:")
        if years == None:
            print("Not Found")
            suggestions = getSuggestions(SELECTED_ARTIST)
            if len(suggestions) > 0:
                print("Suggestions:")
                print(*suggestions, sep = ", ")
                input("Did you mean one of the following? (y/n)")
                
        else:
            print(", ".join(years))

        genres = getGenres(SELECTED_ARTIST)

        print("Artist Genres:")
        if genres == None or len(genres) == 0:
            print("Not Found")
        else:
            print(", ".join(genres))
            
        repeat = ""
        while repeat != "y" and repeat != "n":
            repeat = input("Search for another artist? (y/n)")
        if repeat == "n":
            break
    print("Exiting Program")

if __name__ == '__main__':
    main()
