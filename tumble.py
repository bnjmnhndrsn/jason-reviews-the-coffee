import pytumblr
import datetime
import dateutil.tz
import hypchat
import re
import os
from time import sleep


def get_history_before(hypchat, room_id, endtime):
    result = []
    fetch_again = True
    date = 'recent'
    while fetch_again:
        print 'fetching for for this date: {0}'.format(date)
        latest_fetch = hypchat.get_room(room_id).history(date=date)
        sleep(3)
        for item in reversed(latest_fetch['items']):
            date = item['date']
            if date < endtime:
                fetch_again = False
                break
            else:
                result.append(item)
    return result

def filter_results(list, functions):
    result = []
    
    for item in list:
        passes = True
        try:
            for fn in functions:
                passes = fn(item)
                if not passes:
                    break 
        except:
            passes = False
        
        if passes:
            result.append(item)
            
    return result
    
def filter_by_id(item):
    return item['from']['id'] in USER_IDS

def filter_by_text(item):
    for regex in REGEXES:
        if re.search(regex, item['message'].lower()):
            return True 
    return False
    
def post_to_tumblr(client, params):
    client.create_quote("jasonreviewscoffee", **params)         
    

hc = hypchat.HypChat(os.environ['HIPCHAT_TOKEN'])

ROOM_ID = 44415
USER_IDS = (79780,)
REGEXES = (
    r'make(s)* (the )*coffee',
    r'made (the )*coffee',
    r'coffee is',
    r'coffee was', 
    r'^(the )*coffee',
    r'this coffee',
)

one_hour_ago = (datetime.datetime.now() - datetime.timedelta(hours=1)).replace(tzinfo=dateutil.tz.tzutc())
history = get_history_before(hc, ROOM_ID, one_hour_ago)
filtered = filter_results(history, [filter_by_id, filter_by_text])

print "messages retrieved after filtering: {0}".format(len(filtered))

client = pytumblr.TumblrRestClient(
    os.environ['TUMBLR_CONSUMER_KEY'],
    os.environ['TUMBLR_SECRET_KEY'],
    os.environ['TUMBLR_OAUTH_TOKEN'],
    os.environ['TUMBLR_OAUTH_SECRET'],
)

for item in filtered:
    print 'posting quote: "{0}"'.format(item['message'])
    
    post_to_tumblr(client, {
        'state': 'published',
        'tags': ['jasonreviewsthecoffee'],
        'date': str(item['date']),
        'quote': item['message'],
        'source': 'Jason'
    })
