"""MEOWNED (MEssages Over tWitter ¿stegaNography? Exfiltrating Data)"""
"""pip3 install Stegano"""

import sys
from stegano import lsb

if len(sys.argv) != 4:
    sys.exit('Usage: hide [source-image] [output-image] [message]')

secret = lsb.hide(sys.argv[1], sys.argv[3])
secret.save(sys.argv[2])