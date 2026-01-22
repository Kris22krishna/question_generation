import signal
import random
import math
from typing import Any, Dict, Optional
from RestrictedPython import compile_restricted, safe_globals
from RestrictedPython.Guards import guarded_iter_unpack_sequence, guarded_unpack_sequence
from config import settings


class TimeoutException(Exception):
    """Raised when code execution times out."""
    pass


def timeout_handler(signum, frame):
    """Signal handler for execution timeout."""
    raise TimeoutException("Execution timed out")


class PythonSandbox:
    """Secure Python code execution sandbox."""
    
    def __init__(self, timeout: int = None):
        """
        Initialize the sandbox.
        
        Args:
            timeout: Maximum execution time in seconds (default from settings)
        """
        self.timeout = timeout or settings.EXECUTION_TIMEOUT
        self.safe_builtins = self._create_safe_builtins()
    
    def _create_safe_builtins(self) -> Dict[str, Any]:
        """Create a safe set of builtins for code execution."""
        # Start with RestrictedPython's safe globals
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
        
        return builtins
    
    def execute(self, code: str) -> Dict[str, Any]:
        """
        Execute Python code in a restricted environment.
        
        Args:
            code: Python code to execute
            
        Returns:
            Dictionary with 'result', 'error', and 'error_type' keys
        """
        result = {
            'result': None,
            'error': None,
            'error_type': None
        }
        
        try:
            # Compile the code with RestrictedPython
            byte_code = compile_restricted(
                code,
                filename='<user_code>',
                mode='exec'
            )
            
            # Set up execution environment
            exec_globals = self.safe_builtins.copy()
            exec_locals = {}
            
            # Set up timeout (Unix-based systems)
            # Note: signal.alarm doesn't work on Windows
            # For Windows, we'll use a simple execution without timeout
            # Production use should consider multiprocessing or threading alternatives
            try:
                # Try to set alarm (works on Unix/Linux/Mac)
                signal.signal(signal.SIGALRM, timeout_handler)
                signal.alarm(self.timeout)
                has_alarm = True
            except (AttributeError, ValueError):
                # Windows doesn't support SIGALRM
                has_alarm = False
            
            try:
                # Execute the code
                exec(byte_code, exec_globals, exec_locals)
                
                # Look for return value in locals
                # Check for common return patterns
                if 'result' in exec_locals:
                    result['result'] = exec_locals['result']
                elif 'answer' in exec_locals:
                    result['result'] = exec_locals['answer']
                elif 'question' in exec_locals:
                    result['result'] = exec_locals['question']
                else:
                    # Get the last assigned variable if any
                    if exec_locals:
                        result['result'] = list(exec_locals.values())[-1]
                
            finally:
                # Cancel alarm
                if has_alarm:
                    signal.alarm(0)
        
        except SyntaxError as e:
            result['error'] = f"Syntax Error: {e}"
            result['error_type'] = 'SyntaxError'

        except TimeoutException:
            result['error'] = f"Code execution exceeded {self.timeout} second timeout"
            result['error_type'] = 'TimeoutError'
        
        except Exception as e:
            result['error'] = str(e)
            result['error_type'] = type(e).__name__
        
        return result


def execute_code(code: str, timeout: Optional[int] = None) -> Dict[str, Any]:
    """
    Convenience function to execute code in sandbox.
    
    Args:
        code: Python code to execute
        timeout: Optional custom timeout
        
    Returns:
        Execution result dictionary
    """
    sandbox = PythonSandbox(timeout=timeout)
    return sandbox.execute(code)
