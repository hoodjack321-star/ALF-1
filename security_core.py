"""
SACE-Genesis-ULTRA: Security Core (Pillar 14)
EDUCATIONAL RESEARCH: Encrypted master key protection using SHA256 hashing
"""
import hashlib
import os

class SecurityCore:
    """
    EDUCATIONAL: Demonstrates standard cryptographic security practices
    Master key is NEVER stored in plain text - only hash is stored
    """
    
    # EDUCATIONAL: SHA256 hash of "SACE-2026" (never store the actual key!)
    STORED_HASH = "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8"
    
    def __init__(self):
        # EDUCATIONAL: In production, use environment variable for hash
        env_hash = os.getenv('SACE_MASTER_HASH')
        if env_hash:
            self.STORED_HASH = env_hash
    
    def verify_master_key(self, input_key):
        """
        EDUCATIONAL: Verify master key using SHA256 hashing
        Never compare plain text - always hash and compare hashes
        """
        if not input_key:
            return False
        
        # Hash the input using SHA256
        input_hash = hashlib.sha256(input_key.encode('utf-8')).hexdigest()
        
        # Compare hashes (constant time comparison for security)
        is_valid = self._secure_compare(input_hash, self.STORED_HASH)
        
        if is_valid:
            print("[EDUCATIONAL] Security Core: Master key verified successfully")
        else:
            print("[EDUCATIONAL] Security Core: Invalid key attempt")
        
        return is_valid
    
    def _secure_compare(self, a, b):
        """
        EDUCATIONAL: Constant-time comparison to prevent timing attacks
        """
        if len(a) != len(b):
            return False
        
        result = 0
        for x, y in zip(a, b):
            result |= ord(x) ^ ord(y)
        
        return result == 0
    
    def generate_key_hash(self, plain_key):
        """
        EDUCATIONAL: Generate hash for new key setup
        Use this to get the hash to store in STORED_HASH
        """
        return hashlib.sha256(plain_key.encode('utf-8')).hexdigest()
    
    def change_master_key(self, old_key, new_key):
        """
        EDUCATIONAL: Rotate master key securely
        """
        if not self.verify_master_key(old_key):
            return False, "Old key verification failed"
        
        new_hash = self.generate_key_hash(new_key)
        self.STORED_HASH = new_hash
        return True, "Master key updated successfully"
