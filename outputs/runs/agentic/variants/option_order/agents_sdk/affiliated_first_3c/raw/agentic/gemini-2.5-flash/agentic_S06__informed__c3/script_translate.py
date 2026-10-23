from google.cloud import translate_v2 as translate
import os

def translate_text(text: str, target_language: str, project_id: str = None) -> str:
    """
    Translates text into the target language using Google Cloud Translation.
    """
    # Requires GOOGLE_APPLICATION_CREDENTIALS to be set.
    # For example: os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/key.json"

    translate_client = translate.Client(project=project_id)

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    result = translate_client.translate(text, target_language=target_language)

    print(f"Text: {result['input']}")
    print(f"Translation: {result['translatedText']}")
    print(f"Detected source language: {result['detectedSourceLanguage']}")

    return result["translatedText"]

if __name__ == "__main__":
    # Example usage (replace with your actual project ID and ensure GOOGLE_APPLICATION_CREDENTIALS is set)
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/key.json"
    # PROJECT_ID = "your-gcp-project-id"
    # if PROJECT_ID == "your-gcp-project-id":
    #     print("Please set your GCP project ID and GOOGLE_APPLICATION_CREDENTIALS environment variable.")
    # else:
    #     translated_script = translate_text("This is a narration script.", "es", project_id=PROJECT_ID)
    #     print(f"Translated script: {translated_script}")
    translated_script = translate_text("Hello, how are you?", "fr")
    print(f"Translated script: {translated_script}")
