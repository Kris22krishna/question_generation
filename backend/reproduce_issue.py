import dis
import random
import math
import traceback
from typing import Any, Dict, Optional
from RestrictedPython import compile_restricted, safe_globals
from RestrictedPython.Guards import guarded_iter_unpack_sequence, guarded_unpack_sequence

def reproduce():
    # Setup builtins exactly as in sandbox.py
    builtins = safe_globals.copy()
    
    # Add math and random modules (safe for math questions)
    builtins['random'] = random
    builtins['math'] = math
    
    # Add safe built-in functions
    builtins['range'] = range
    builtins['len'] = len
    builtins['str'] = str
    builtins['int'] = int
    builtins['float'] = float
    builtins['list'] = list
    builtins['dict'] = dict
    builtins['tuple'] = tuple
    builtins['set'] = set
    builtins['abs'] = abs
    builtins['min'] = min
    builtins['max'] = max
    builtins['sum'] = sum
    builtins['round'] = round
    
    # Add RestrictedPython guards
    builtins['_iter_unpack_sequence_'] = guarded_iter_unpack_sequence
    builtins['_unpack_sequence_'] = guarded_unpack_sequence
    builtins['_getattr_'] = getattr
    builtins['_getitem_'] = lambda obj, key: obj[key]
    
    def safe_import(name, globals=None, locals=None, fromlist=(), level=0):
        if name in ['random', 'math']:
            return __import__(name, globals, locals, fromlist, level)
        raise ImportError(f"Import of {name} is not allowed")
        
    builtins['__import__'] = safe_import

    # Block dangerous functions
    # builtins['__import__'] = None # Replaced by safe_import
    builtins['open'] = None
    builtins['eval'] = None
    builtins['exec'] = None
    builtins['compile'] = None
    builtins['__builtins__'] = builtins


    # The code that caused the error (copied from user screenshot/context)
    code = """
import random

a = random.randint(1, 10)
b = random.randint(1, 10)

question = f"What is {a} + {b}?"
"""
    
    try:
        print("Compiling...")
        byte_code = compile_restricted(code, filename='<user_code>', mode='exec')
        
        exec_globals = builtins.copy()
        exec_locals = {}
        
        print("Executing...")
        exec(byte_code, exec_globals, exec_locals)
        print("Execution successful")
        print("Locals:", exec_locals.keys())
        
    except Exception as e:
        print(f"Caught Exception: {type(e).__name__}: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    import sys
    with open('reproduce_output.txt', 'w') as f:
        sys.stdout = f
        sys.stderr = f
        reproduce()
