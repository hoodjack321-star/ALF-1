"""
SACE-Genesis-ULTRA: NLP UrAnalysis (Pillar 12)
EDUCATIONAL RESEARCH: Powerful Roman Urdu/Urdu to English intent translator
"""
import re

class NLPUrAnalysis:
    """
    EDUCATIONAL: Multi-lingual understanding for accessibility
    Maps Roman Urdu and Urdu script to Python function intents
    """
    
    def __init__(self):
        # Comprehensive Roman Urdu → English keyword mapping
        self.roman_urdu_dict = {
            # Actions
            'sikh': 'learn', 'sikho': 'learn', 'seekh': 'learn', 'seekho': 'learn',
            'sikha': 'teach', 'sikhao': 'teach', 'parhao': 'teach',
            'bana': 'create', 'banao': 'create', 'banana': 'create', 'banaoo': 'create',
            'bana kar': 'generate', 'bana kar do': 'generate',
            'likh': 'write', 'likho': 'write', 'likha': 'written',
            'dikha': 'show', 'dikhao': 'show', 'dekhao': 'show',
            'chala': 'run', 'chalaoo': 'run', 'chalao': 'run',
            'band': 'stop', 'band karo': 'stop', 'ruk': 'stop', 'ruko': 'stop',
            'khatam': 'end', 'khatam karo': 'end',
            'shuru': 'start', 'shuru karo': 'start', 'start karo': 'start',
            'do': 'give', 'de': 'give', 'deo': 'give', 'dena': 'give',
            'laoo': 'fetch', 'lao': 'fetch', 'le kar': 'fetch',
            'dhundo': 'search', 'dhoondho': 'search', 'find': 'search',
            'check': 'check', 'check karo': 'check', 'dekho': 'check',
            
            # Objects
            'code': 'code', 'coding': 'code', 'program': 'code',
            'script': 'script', 'file': 'file',
            'app': 'application', 'application': 'application',
            'website': 'website', 'web': 'web',
            'bot': 'bot', 'robot': 'bot', 'ai': 'AI',
            'data': 'data', 'database': 'database', 'db': 'database',
            'api': 'API', 'server': 'server',
            'model': 'model', 'ml': 'machine learning',
            'rvc': 'RVC', 'voice': 'voice', 'audio': 'audio',
            'image': 'image', 'photo': 'image', 'tasveer': 'image',
            'video': 'video', 'clip': 'video',
            'text': 'text', 'likhai': 'text',
            
            # Modifiers
            'ka': 'of', 'ke': 'of', 'ki': 'of',
            'mujhe': 'me', 'mere': 'my', 'mera': 'my',
            'liye': 'for', 'ke liye': 'for',
            'mein': 'in', 'par': 'on',
            'se': 'from', 'ko': 'to',
            'aur': 'and', 'or': 'and',
            'naya': 'new', 'nayi': 'new', 'neha': 'new',
            'purana': 'old', 'purani': 'old',
            'acha': 'good', 'best': 'best', 'behtareen': 'best',
            'fast': 'fast', 'tez': 'fast',
            'simple': 'simple', 'asan': 'simple',
            
            # Questions
            'kya': 'what', 'kaise': 'how', 'kaisa': 'how',
            'kyun': 'why', 'kyon': 'why',
            'kahan': 'where', 'kidhar': 'where',
            'kab': 'when', 'kitna': 'how much',
            'koun': 'who', 'kaun': 'who',
            
            # Urdu Script (UTF-8)
            'سیکھو': 'learn', 'سیکھ': 'learn',
            'کوڈ': 'code', 'کوڈنگ': 'code',
            'بناؤ': 'create', 'بناو': 'create',
            'لکھو': 'write', 'دکھاؤ': 'show',
            'چلاؤ': 'run', 'بند کرو': 'stop',
            'دو': 'give', 'لاؤ': 'fetch',
            'نیا': 'new', 'میرا': 'my',
            'کے لیے': 'for', 'اور': 'and',
        }
        
        # Intent patterns (regex for common Roman Urdu structures)
        self.intent_patterns = [
            (r'(sikh|seekh|sikho|seekho|سیکھو)\s+(\w+)', 'learn {1}'),
            (r'(bana|banao|banana|banaoo|بناؤ)\s+(\w+)', 'create {1}'),
            (r'(likh|likho|likha|لکھو)\s+(\w+)', 'write {1}'),
            (r'(dikha|dikhao|dekhao|دکھاؤ)\s+(\w+)', 'show {1}'),
            (r'(chala|chalaoo|chalao|چلاؤ)\s+(\w+)', 'run {1}'),
            (r'(mujhe|mere)\s+(\w+)\s+(do|de|deo|chahiye)', 'give me {1}'),
            (r'(kaise|kaisa|کیسے)\s+(\w+)', 'how to {1}'),
            (r'(kya|کیا)\s+(\w+)', 'what is {1}'),
        ]
    
    def translate_to_english(self, text):
        """
        EDUCATIONAL: Translates Roman Urdu/Urdu to English intent
        Uses dictionary + pattern matching for robust understanding
        """
        if not text:
            return ""
        
        original = text
        text = text.lower().strip()
        
        # Step 1: Check if Urdu script (UTF-8 range)
        has_urdu = any(ord(c) > 0x0600 and ord(c) < 0x06FF for c in text)
        
        # Step 2: Tokenize and translate
        words = text.split()
        translated_words = []
        
        for word in words:
            # Clean punctuation
            clean_word = re.sub(r'[^\w\s]', '', word)
            
            # Direct dictionary lookup
            if clean_word in self.roman_urdu_dict:
                translated_words.append(self.roman_urdu_dict[clean_word])
            else:
                # Keep original if no translation
                translated_words.append(clean_word)
        
        translated = ' '.join(translated_words)
        
        # Step 3: Pattern matching for complex intents
        for pattern, template in self.intent_patterns:
            match = re.search(pattern, text)
            if match:
                # Extract groups and format
                groups = match.groups()
                formatted = template
                for i, g in enumerate(groups[1:], 1):
                    if g in self.roman_urdu_dict:
                        g = self.roman_urdu_dict[g]
                    formatted = formatted.replace(f'{{{i}}}', g)
                translated = formatted
                break
        
        print(f"[EDUCATIONAL] NLP Translation: '{original}' → '{translated}'")
        return translated
    
    def extract_intent(self, translated_text):
        """
        EDUCATIONAL: Extract actionable intent from translated text
        Maps to Python function patterns
        """
        text = translated_text.lower()
        
        # Intent classification
        intents = []
        
        if any(w in text for w in ['learn', 'sikh', 'seekh', 'tutorial', 'example']):
            intents.append('LEARN')
        
        if any(w in text for w in ['create', 'bana', 'generate', 'build', 'make']):
            intents.append('CREATE')
        
        if any(w in text for w in ['code', 'program', 'script', 'python']):
            intents.append('CODE')
        
        if any(w in text for w in ['run', 'execute', 'chala', 'start']):
            intents.append('EXECUTE')
        
        if any(w in text for w in ['show', 'dikha', 'display', 'print']):
            intents.append('DISPLAY')
        
        if any(w in text for w in ['fetch', 'get', 'laoo', 'lao', 'retrieve']):
            intents.append('FETCH')
        
        if any(w in text for w in ['rvc', 'voice', 'audio', 'speech']):
            intents.append('RVC')
        
        if any(w in text for w in ['ai', 'ml', 'model', 'machine learning']):
            intents.append('AI_ML')
        
        # Extract subject/topic
        topics = []
        common_topics = ['python', 'rvc', 'voice', 'ai', 'ml', 'api', 'web', 
                        'scraping', 'bot', 'automation', 'database', 'flask',
                        'django', 'tensorflow', 'pytorch', 'opencv']
        
        for topic in common_topics:
            if topic in text:
                topics.append(topic)
        
        # Build final intent string
        if intents and topics:
            return f"{'_'.join(intents)}_{'_'.join(topics)}"
        elif intents:
            return f"{'_'.join(intents)}_GENERAL"
        elif topics:
            return f"GENERAL_{'_'.join(topics)}"
        else:
            # Fallback: use first 3 significant words
            words = [w for w in translated_text.split() if len(w) > 2]
            return '_'.join(words[:3]) if words else "UNKNOWN_INTENT"
    
    def detect_language(self, text):
        """EDUCATIONAL: Detect if input is Roman Urdu, Urdu script, or English"""
        urdu_range = sum(1 for c in text if 0x0600 <= ord(c) <= 0x06FF)
        total = len(text.replace(' ', ''))
        
        if urdu_range > total * 0.3:
            return 'urdu_script'
        
        # Check for Roman Urdu indicators
        roman_indicators = ['hai', 'ka', 'ke', 'ki', 'ko', 'se', 'mein', 'aur',
                          'bana', 'sikh', 'do', 'mujhe', 'mera', 'naya']
        roman_count = sum(1 for w in roman_indicators if w in text.lower())
        
        if roman_count >= 2:
            return 'roman_urdu'
        
        return 'english'
