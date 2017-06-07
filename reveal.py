#!/usr/bin/env python3
"""MEOWNED (MEssages Over tWitter ¿stegaNography? Exfiltrating Data)"""
"""pip3 install python-twitter"""
"""pip3 install Stegano"""

import sys
from stegano import lsb

if len(sys.argv) != 2:
    sys.exit('Usage: reveal <image>')

clear_message = lsb.reveal("./output-imgs/" + sys.argv[1])

print (clear_message)