from collections import defaultdict
import random 

markov = defaultdict(list)
STOP_WORD = "\n"

def cleanList(list):
    ret = []
    for l in list:
        l = l.replace(";,!?", "\n")
        if l.strip() == "":
            continue
        ret.append(l)
    return ret
    

def learn(msg, chainLen, saveOnDisk = True):
    if saveOnDisk:
        f = open("markovmind.data", 'a')
        f.write(msg + "\n")
        f.close
    buf = [STOP_WORD] * chainLen
    for word in msg.split():
        markov[tuple(buf)].append(word)
        del buf[0]
        buf.append(word)
    markov[tuple(buf)].append(STOP_WORD)

def talk(msg, chainLen, maxWords = 10000):
    buf = msg.split()[:chainLen]
    if len(msg.split()) > chainLen:
        
        message = buf[:]
    else:
        message = []
        for i in xrange(chainLen):
            message.append(random.choice(
                    markov[random.choice(markov.keys())]).strip())
        for x in xrange(maxWords):
            try:
                nWord = random.choice(markov[tuple(buf)]).strip()
            except IndexError: 
                continue
            if nWord == STOP_WORD:
                break
            message.append(nWord)
            del buf[0]
            buf.append(nWord)
            
        print("-|" + ",".join(message) + "|-")
        message = cleanList(message)
        print("-|" + ",".join(message) + "|-")        
        return ' '.join(message)
                

