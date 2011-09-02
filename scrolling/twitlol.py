#! /usr/bin/env python
import re,time,twitter, random, sys
import lolscroll

def group(string, n):
    """Splits a string into smaller substrings of character length n
    From: http://snippets.dzone.com/posts/show/5641 """
    return [string[i:i+n] for i in xrange(0, len(string), n)]

con_secret=       ''
con_secret_key=   ''
token=            ''
token_key=        ''

lasttweet=1
tweets={}
tweetrating={}
tweetsrefresh=0

def gettweets():
    global tweetsrefresh
    global tweets
    global lasttweet
    if time.time()-tweetsrefresh > 600:
        tweetsrefresh=time.time()
        twitt=twitter.Twitter(auth=twitter.OAuth(token, token_key, con_secret,\
                con_secret_key))
        ht=twitt.statuses.home_timeline(since_id=lasttweet,count=50)
        if ht:
            print len(ht)
            lasttweet=ht[0]['id']
            for tweet in ht:
                tweetid=tweet['id']
                if tweetid not in tweetrating:
                    tweetrating[tweetid]=(tweetsrefresh,1)
                    tweets[tweetid]='@%s %s' % (tweet['user']['screen_name'], \
                            tweet['text'])
            #tweets=['@%s %s' % (tweet['user']['screen_name'], tweet['text']) for \
            #        tweet in ht[:10]]
            print 'refreshed'
            for key in tweetrating.keys()[:]:
                if time.time()-tweetrating[key][0]>86400:
                    del tweetrating[key]
                    del tweets[key]
        else:
            print 'no new tweets'



def getonetweet():
    #return ''.join([random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ') \
    #        for dontcare in xrange(4)])
    gettweets()
    now=time.time()
    penalty=[(key,(now-value[0])*value[1]**2) \
            for key,value in tweetrating.iteritems()]
    penalty.sort(key=lambda item: (item[1],-item[0]))
    tweetid=penalty[0][0]
    print len(penalty),penalty[0][1],penalty[-1][1]
    timerecv,showntimes = tweetrating[tweetid]
    tweetrating[tweetid]=(timerecv,showntimes+1)
    retstr='%s   '%tweets[tweetid]
    #retstr='%s\n'%random.choice(tweets).encode('latin1','replace')
    #print retstr
    #return 'test'#tweets[0]
    return retstr

def getmessage():
    def remove_html_tags(data):
        p = re.compile(r'<.*?>')
        return p.sub('', data)

    import feedparser
    while True:
        tagesschau=['Tagesschau: %s: %s'%(entry['title'],remove_html_tags(\
                entry['summary'])) for entry in feedparser.parse(\
                'http://www.tagesschau.de/newsticker.rdf').entries]
        heisent=['Heise: %s'%entry['title'] for entry in feedparser.parse(\
                'http://www.heise.de/newsticker/heise.rdf').entries]
        sztopthemen=['SZ: %s: %s'%(entry['title'],remove_html_tags(\
                entry['summary'])) for entry in feedparser.parse(\
                'http://rss.feedsportal.com/795/f/449002/index.rss').entries]
        allentries=zip(tagesschau,heisent,sztopthemen)
        for entrytuple in allentries:
            for entry in entrytuple:
                yield '%s   ' % entry
                yield getonetweet()

def loop():
    lol=lolscroll.Lolscroll()
    genmessage=getmessage()
    gettweets()
    while True:
        message=genmessage.next()
        try:
            lol.write(message)
            print message
        except UnicodeError:
            print 'ERROR %s'%message

if __name__ == '__main__':
    loop()
