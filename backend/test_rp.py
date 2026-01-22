from RestrictedPython import compile_restricted

code = "print('hello'" # Syntax error
try:
    byte_code = compile_restricted(code, filename='<string>', mode='exec')
    print(f"Type: {type(byte_code)}")
    print(f"Has errors attr: {hasattr(byte_code, 'errors')}")
except SyntaxError as e:
    print(f"Caught SyntaxError: {e}")
except Exception as e:
    print(f"Caught Exception: {type(e).__name__}: {e}")
