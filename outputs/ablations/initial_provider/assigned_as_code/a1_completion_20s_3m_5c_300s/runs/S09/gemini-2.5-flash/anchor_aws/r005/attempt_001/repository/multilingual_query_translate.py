import os
from google.cloud import translate_v2 as translate

def multilingual_query_translate(text, target_language, config=None):
    config = config or {}
    # Google Cloud Translation API typically uses GOOGLE_APPLICATION_CREDENTIALS for authentication
    # Ensure the environment variable is set or pass credentials explicitly if needed.
    # For this example, we assume GOOGLE_APPLICATION_CREDENTIALS is set up.
    
    translate_client = translate.Client()

    # Text can also be a sequence of strings, in which case this method
    # will return a list of results for each text. 
    response = translate_client.translate(text, target_language=target_language)

    translated_text = response["translatedText"]
    source_language = response["detectedSourceLanguage"]
    
    return {"translated_text": translated_text, "source_language": source_language, "target_language": target_language}
