from twisted.words.protocols import irc
from twisted.internet import protocol
import Markov
import re


## Bot interface
class CMBellbot(irc.IRCClient):
    def _get_nickname(self):
        return self.factory.nickname
    nickname = property(_get_nickname)

    def signedOn(self):
        self.join(self.factory.channel)
        print "Signed on as %s. " % (self.nickname,)
    
    def joined(self, channel):
        print "Joined %s" % (channel,)
        
    def privmsg(self, user, channel, msg):
        # terminate if command not given by a user
        if not user:
            return

        # try a keyword match
        keyword = re.match("!(\w*)", msg)
        if keyword != None:
            print "I should be doing something with keyword %s" % (keyword.groups()[0],)

            args = re.match("!\w* (.*)", msg)
            if args != None:
                print "and something with arguments %s" % (args.groups()[0])
            return

        m = re.match(self.nickname + "[:,]{0,1} (.*)",msg)
        
        if self.nickname in msg and m != None and m.groups()[0]:
            msg = m.groups()[0]
            Markov.learn(msg, self.factory.chainLen)
            sentence = Markov.talk(msg, 
                                   self.factory.chainLen, 
                                   self.factory.maxWords)
            if sentence == None:
                print sentence
            
            
            self.msg(self.factory.channel, 
                     user.split('!', 1)[0] + ": " + sentence)
        
        
## Bot factory
class CMBellbotFactory(protocol.ClientFactory):
    protocol = CMBellbot
    
    def __init__(self, channel, 
                 nickname = "CM_Bellbot",
                 chainLen = 10,
                 maxWords = 10000):
        self.channel = channel
        self.nickname = nickname
        self.chainLen = chainLen
        self.maxWords = maxWords

    def clientConnectionLost(self, connector, reason):
        print "Lost connection (%s), reconnecting... " % (reason,)
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        print "Could not connect! (%s)" % (reason,)
    
            
