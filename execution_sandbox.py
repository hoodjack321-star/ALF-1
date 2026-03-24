"""
SACE-Genesis-ULTRA: Execution Sandbox (Pillar 13)
EDUCATIONAL RESEARCH: Safe, isolated testing environment for code validation
"""
import subprocess
import tempfile
import os
import signal
import sys

class ExecutionSandbox:
    """
    EDUCATIONAL: Tests code in isolated subprocess before saving to memory
    Prevents broken/unsafe code from entering the knowledge vault
    """
    
    def __init__(self, timeout=5):
        self.timeout = timeout
        self.allowed_modules = [
            'os', 'sys', 'json', 're', 'math', 'random', 'datetime',
            'collections', 'itertools', 'functools', 'typing',
            'requests', 'flask', 'numpy', 'pandas'
        ]
    
    def test_code_in_sandbox(self, code_snippet):
        """
        EDUCATIONAL: Run code in isolated subprocess with timeout
        Returns (success: bool, result: str)
        """
        if not code_snippet or len(code_snippet.strip()) < 10:
            return False, "Code too short or empty"
        
        # EDUCATIONAL: Pre-scan for dangerous patterns
        danger_patterns = [
            'os.system', 'subprocess.call', 'eval(', 'exec(',
            '__import__', 'open("/etc', 'open(\'/', 'socket.',
            'import socket', 'import subprocess'
        ]
        
        for pattern in danger_patterns:
            if pattern in code_snippet:
                return False, f"Blocked pattern detected: {pattern}"
        
        # Create temporary file for code
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            # Wrap code in safe context
            safe_wrapper = f'''
# EDUCATIONAL: Sandbox wrapper
import sys
sys.path = [p for p in sys.path if 'site-packages' not in p]

# Restricted execution
{code_snippet}

# Success marker
print("\\n[SANDBOX_SUCCESS]")
'''
            f.write(safe_wrapper)
            temp_file = f.name
        
        try:
            # Run in isolated subprocess with timeout
            result = subprocess.run(
                [sys.executable, temp_file],
                capture_output=True,
                text=True,
                timeout=self.timeout,
                env={'PYTHONPATH': ''}  # Restrict imports
            )
            
            stdout = result.stdout
            stderr = result.stderr
            
            # Check for success marker
            success = "[SANDBOX_SUCCESS]" in stdout and result.returncode == 0
            
            if success:
                return True, stdout[:500]  # Truncate for storage
            else:
                error_msg = stderr[:200] if stderr else "Execution failed"
                return False, error_msg
                
        except subprocess.TimeoutExpired:
            return False, f"Code execution exceeded {self.timeout}s timeout"
        except Exception as e:
            return False, f"Sandbox error: {str(e)}"
        finally:
            # Cleanup
            try:
                os.remove(temp_file)
            except:
                pass
    
    def auto_debug(self, code_snippet, error):
        """
        EDUCATIONAL: Attempt to fix common code errors
        """
        fixes = [
            # Fix 1: Add missing imports
            (r'(\w+)\s*\(', lambda m: f"import {m.group(1)}\\n{m.group(0)}" 
             if m.group(1) in ['requests', 'json', 'os'] else m.group(0)),
            
            # Fix 2: Fix indentation
            (r'^def\s+(\w+):$', r'def \\1():\\n    pass'),
        ]
        
        debugged_code = code_snippet
        for pattern, replacement in fixes:
            import re
            debugged_code = re.sub(pattern, replacement, debugged_code)
        
        # Test the debugged version
        is_safe, result = self.test_code_in_sandbox(debugged_code)
        
        if is_safe:
            return True, debugged_code
        return False, code_snippet
    
    def validate_syntax(self, code_snippet):
        """EDUCATIONAL: Quick syntax check without execution"""
        try:
            compile(code_snippet, '<string>', 'exec')
            return True, "Syntax valid"
        except SyntaxError as e:
            return False, f"Syntax error: {e}"
