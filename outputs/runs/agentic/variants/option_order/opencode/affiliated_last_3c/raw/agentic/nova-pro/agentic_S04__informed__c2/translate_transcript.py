import os
from google.cloud import translate_v2 as translate

# Set up client
translate_client = translate.Client()


# Translate completed transcript segments
def translate_transcript(transcript, target_language):
    result = translate_client.translate(transcript, target_language=target_language)
    return result["translatedText"]


if __name__ == "__main__":
    transcript = "This is a sample transcript."
    target_language = "es"
    print(translate_transcript(transcript, target_language))
