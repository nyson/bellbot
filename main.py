import sys
import os
from CMBellbot import *
import Markov
from twisted.internet import reactor

if __name__ == "__main__":
    chLen = 2
    try: 
        chan = sys.argv[1]
    except IndexError:
        print "Please specify a channel name."
        print "Example; \n$ python main.py bellman"
        exit()

    if os.path.exists("markovmind.data"):
        f = open("markovmind.data")
        i = 0
        for row in f:
            i += 1
            Markov.learn(row, chLen, False)
        f.close()
        print "Mind is up again and %i rows loaded!" % (i,)

    
    reactor.connectTCP('se.quakenet.org', 
                       6667, 
                       CMBellbotFactory('#' + chan))
    reactor.run()

