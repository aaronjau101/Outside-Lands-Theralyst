#@title           Main
#@author          Aaron Jauregui
#@description     Run files in order

import artistFrequency
import genreFinder
import genreCounter
import time

def main():
    print("Initiating Programs")
    start_time = time.time()
    artistFrequency.main()
    genreFinder.main()
    genreCounter.main()
    print("Programs took " + str(time.time() - start_time) + " seconds")

if __name__ == '__main__':
    main()
