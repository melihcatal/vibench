import os
from google.cloud import translate_v2 as translate

# Set up the API key
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path/to/your-google-credentials.json"


# Function to translate text
def translate_text(text, target_language="en"):
    translate_client = translate.Client()
    result = translate_client.translate(text, target_language=target_language)
    return result["translatedText"]
