"""
SACE-Genesis-ULTRA: Memory Vault (Pillar 2)
EDUCATIONAL RESEARCH: SQLite-based persistent memory with auto-pruning
"""
import sqlite3
import json
import gzip
import base64
import os
from datetime import datetime

class MemoryVault:
    """EDUCATIONAL: Self-managing knowledge database"""
    
    def __init__(self, db_path='memory_vault.db', max_entries=1000):
        self.db_path = db_path
        self.max_entries = max_entries
        self._init_db()
    
    def _init_db(self):
        """EDUCATIONAL: Initialize SQLite schema"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS knowledge (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                query TEXT UNIQUE,
                compressed_response BLOB,
                status TEXT,
                timestamp TEXT,
                access_count INTEGER DEFAULT 0
            )
        ''')
        conn.commit()
        conn.close()
    
    def save_knowledge(self, query, data, status="LEARNED"):
        """EDUCATIONAL: Compress and store knowledge"""
        # Compress data using gzip + base85
        json_data = json.dumps(data).encode('utf-8')
        compressed = gzip.compress(json_data)
        encoded = base64.b85encode(compressed).decode('ascii')
        
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        try:
            c.execute('''
                INSERT OR REPLACE INTO knowledge 
                (query, compressed_response, status, timestamp, access_count)
                VALUES (?, ?, ?, ?, 0)
            ''', (query, encoded, status, datetime.now().isoformat()))
            
            conn.commit()
            print(f"[EDUCATIONAL] Memory Vault: Saved '{query}' ({len(encoded)} chars compressed)")
            
            # Auto-prune if over limit
            self._auto_prune(conn)
            
        except Exception as e:
            print(f"[EDUCATIONAL] Vault error: {e}")
        finally:
            conn.close()
    
    def retrieve_knowledge(self, query):
        """EDUCATIONAL: Retrieve and decompress knowledge"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        c.execute('SELECT compressed_response, status FROM knowledge WHERE query=?', (query,))
        row = c.fetchone()
        
        if row and row[1] != "FAILED":
            encoded, status = row
            # Decompress
            compressed = base64.b85decode(encoded.encode('ascii'))
            json_data = gzip.decompress(compressed)
            data = json.loads(json_data.decode('utf-8'))
            
            # Update access count
            c.execute('UPDATE knowledge SET access_count = access_count + 1 WHERE query=?', (query,))
            conn.commit()
            conn.close()
            
            return data
        
        conn.close()
        return None
    
    def _auto_prune(self, conn):
        """PILLAR 2 Extension: Auto-prune old entries"""
        c = conn.cursor()
        c.execute('SELECT COUNT(*) FROM knowledge')
        count = c.fetchone()[0]
        
        if count > self.max_entries:
            # Remove oldest, least accessed entries
            c.execute('''
                DELETE FROM knowledge WHERE id IN (
                    SELECT id FROM knowledge 
                    ORDER BY access_count ASC, timestamp ASC 
                    LIMIT ?
                )
            ''', (count - self.max_entries,))
            conn.commit()
            print(f"[EDUCATIONAL] Memory Vault: Auto-pruned to {self.max_entries} entries")
    
    def nuclear_wipe(self):
        """PILLAR 8: Nuclear Protocol - Complete data destruction"""
        try:
            os.remove(self.db_path)
            print("[EDUCATIONAL] Nuclear Protocol: memory_vault.db destroyed")
            self._init_db()  # Recreate empty
            return True
        except Exception as e:
            print(f"[EDUCATIONAL] Nuclear error: {e}")
            return False
    
    def get_stats(self):
        """EDUCATIONAL: Return vault statistics"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('SELECT COUNT(*), SUM(access_count) FROM knowledge')
        total, accesses = c.fetchone()
        conn.close()
        return {"entries": total or 0, "total_accesses": accesses or 0}
