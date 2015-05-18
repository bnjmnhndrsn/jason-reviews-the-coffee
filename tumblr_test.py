import pytumblr
import os

def post_to_tumblr(client, params):
    return client.create_quote("jasonreviewscoffee", **params)         
    
client = pytumblr.TumblrRestClient(
    os.environ['TUMBLR_CONSUMER_KEY'],
    os.environ['TUMBLR_SECRET_KEY'],
    os.environ['TUMBLR_OAUTH_TOKEN'],
    os.environ['TUMBLR_OAUTH_SECRET'],
)

obj = post_to_tumblr(client, {
    'state': 'published',
    'tags': ['jasonreviewsthecoffee'],
    'quote': "TEST TEST TEST",
    'source': 'Jason'
})

print obj
