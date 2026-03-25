import os
from main import app # یہ آپ کی main.py فائل سے Flask کو جوڑے گا

if __name__ == "__main__":
    # ہگنگ فیس کے لیے پورٹ 7860 ہونا ضروری ہے
    port = int(os.environ.get("PORT", 7860))
    app.run(host="0.0.0.0", port=port)
