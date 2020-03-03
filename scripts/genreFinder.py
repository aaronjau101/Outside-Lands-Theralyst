#@title           Artist Frequency
#@author          Aaron Jauregui
#@description     Program to search Google for artist genres using Selenium

#@dev             Because Google CAPTCHA, each browser session searches set number of names
#@dev             Roughly takes 30 mins total

#@input           None
#@output          JSON file with artist name and array of genres

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import json

YOUR_PATH = os.path.dirname(os.getcwd())
SEARCHES_PER_BROWSER = 10

#Function to dump JSON obj to file
def dumpJSON(outfile, obj):
    with open(outfile, 'w') as oFile:
        json.dump(obj, oFile, ensure_ascii=False)

#Finds a text input and then searches for genres for given artist
#Notes:
    #Assumes the first text input found is the Google Search bar
def searchArtist(driver, artistName):
    inputs = driver.find_elements_by_tag_name("input")
    for i in inputs:
        if(i.get_attribute("type") == "text"):
            i.clear()
            i.send_keys("Genres " + artistName, Keys.ENTER)
            return

#Searches for any elements that may be holding genre names
def searchGenres(driver):
    genres = []
    #Looks for RL-Feature Method
    RL = driver.find_elements_by_class_name("rl_feature")
    if(len(RL) > 0):
        links = RL[0].find_elements_by_tag_name("a")
        for link in links:
            titles = link.find_elements_by_class_name("title")
            if(len(titles) > 0):
                title = titles[0].text.upper()
                genres.append(title)
    #Looks for Knowledge-Panel Method
    KP = driver.find_elements_by_class_name("knowledge-panel")
    if(len(KP) > 0):
        headers = KP[0].find_elements_by_class_name("kp-header")
        if(len(headers) > 0):
            links = headers[0].find_elements_by_tag_name("a")
            if(len(links) > 0):
                title = links[0].text.upper()
                if title != "":
                    genres.append(title)
        else:
            headers = KP[0].find_elements_by_class_name("kp-hc")
            if(len(headers) > 0):
                links = headers[0].find_elements_by_tag_name("a")
                if(len(links) > 0):
                    title = links[0].text.upper()
                    if title != "":
                        genres.append(title)
    #Looks for Knowledge-Panel Block Method
    KP = driver.find_elements_by_class_name("kp-blk")
    if(len(KP) > 0):
        headers = KP[0].find_elements_by_class_name("kp-header")
        if(len(headers) > 0):
            links = headers[0].find_elements_by_tag_name("a")
            if(len(links) > 0):
                title = links[0].text.upper()
                if title != "":
                    genres.append(title)
    #Looks for WebAnswers Table Method
    WA = driver.find_elements_by_class_name("webanswers-webanswers_table__webanswers-table")
    if len(WA) > 0:
        table = WA[0].find_element_by_tag_name("table")
        table_rows = table.find_elements_by_tag_name("tr")
        for tr in table_rows:
            cols = tr.find_elements_by_tag_name("td")
            if len(cols) > 1:
                category = cols[0].find_elements_by_tag_name("b")
                if len(category)>0 and category[0].text.upper() == "GENRES":
                    title = cols[1].text.upper()
                    genres.append(title)
    return genres

#Searches Google for the genres of an artist
def getArtistGenres(driver, artist):
    wait = WebDriverWait(driver, 5)
    searchArtist(driver, artist)
    wait.until(EC.title_contains(artist))
    return searchGenres(driver)

#Opens and returns a new Chrome browser driver
def openChrome():
    options = webdriver.ChromeOptions()
    prefs = {"profile.default_content_setting_values.notifications" : 2}
    options.add_experimental_option("prefs",prefs)
    driver = webdriver.Chrome(options=options)
    return driver

#Opens new browser with Google
def openGoogle():
    driver = openChrome()
    wait = WebDriverWait(driver, 5)
    driver.get("https://www.google.com/")
    wait.until(EC.title_contains("Google"))
    return driver

#Searches Google for the genres of an artist from a list of artists
#Returns JSON obj with artists and their genres
#Notes:
    #Each browser does a certain number of searches to avoid Google CAPTCHCA
def getAllArtistsGenres(artists):
    data = {}
    data["artists"] = []
    
    startIndex = 0
    finishIndex = len(artists)
    
    while startIndex < finishIndex:
    #
        driver = openGoogle()
        for i in range(SEARCHES_PER_BROWSER):
        #
            index = startIndex + i
            if index < finishIndex:
                artist = artists[index]
                genres = getArtistGenres(driver, artist)
                data["artists"].append({
                    "name": artist,
                    "genres": genres
                })
        #        
        driver.close()
        startIndex += SEARCHES_PER_BROWSER
    #    
    return data

#Returns array of all artists
def getArtists():
    ARTIST_FILE = os.path.join(YOUR_PATH, "data//allArtists.txt")
    return [line.rstrip('\n').strip().upper() for line in open(ARTIST_FILE)]

def main():
    print("Starting Genre Finder Program")
    start_time = time.time()

    #Array of all artist names
    artists = getArtists()

    #JSON obj with all artists genres
    artistsGenres = getAllArtistsGenres(artists)

    #Dumps JSON obj to a file
    JSON_FILE = os.path.join(YOUR_PATH, "data//artistsGenresJSON.txt")
    dumpJSON(JSON_FILE, artistsGenres)
    
    print("Program took " + str(time.time() - start_time) + " seconds")


if __name__ == '__main__':
    main()
