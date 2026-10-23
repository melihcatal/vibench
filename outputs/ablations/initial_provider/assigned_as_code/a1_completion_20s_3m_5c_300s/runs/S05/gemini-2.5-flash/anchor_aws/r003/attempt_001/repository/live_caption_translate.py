import os
from google.cloud import translate_v2 as translate

# Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
# For example: os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/keyfile.json"

class LiveCaptionTranslator:
    def __init__(self):
        self.client = translate.Client()

    def translate_caption(self, text, target_language, source_language=None):
        if not text:
            return ""
        
        result = self.client.translate(text, target_language=target_language, source_language=source_language)
        return result['translatedText']
