from google.cloud import translate_v3 as translate
import os

def translate_platform_output(text: str, target_language_code: str, project_id: str) -> dict:
    """
    Translates platform model output for another locale using Google Cloud Translation.
    
    Args:
        text: The text output from the model.
        target_language_code: The BCP-47 language code to translate the text into (e.g., "es" for Spanish).
        project_id: Your Google Cloud project ID.
        
    Returns:
        A dictionary containing the translated text and source/target language codes.
    """
    client = translate.TranslationServiceClient()
    location = "global"  # Or specify a region like "us-central1"
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language_code,
        }
    )
    
    translation_result = {
        "translated_text": "",
        "source_language_code": None,
        "target_language_code": target_language_code
    }

    if response.translations:
        translation = response.translations[0]
        translation_result["translated_text"] = translation.translated_text
        translation_result["source_language_code"] = translation.detected_language_code
        
    return translation_result

if __name__ == '__main__':
    # Example usage
    project_id = os.environ.get("GCP_PROJECT_ID", "your-gcp-project-id")
    
    if project_id == "your-gcp-project-id":
        print("Please set the GCP_PROJECT_ID environment variable or replace 'your-gcp-project-id' with your actual project ID.")
    else:
        # print("Translating text to Spanish...")
        # try:
        #     english_text = "Hello, how are you today? This is a test."
        #     spanish_translation = translate_platform_output(english_text, "es", project_id)
        #     print("Original English:", english_text)
        #     print("Translated Spanish:", spanish_translation.get("translated_text"))
        #     print("Source Language:", spanish_translation.get("source_language_code"))
        #     
        #     print("\nTranslating text to French...")
        #     german_text = "Guten Tag, wie geht es Ihnen?"
        #     french_translation = translate_platform_output(german_text, "fr", project_id)
        #     print("Original German:", german_text)
        #     print("Translated French:", french_translation.get("translated_text"))
        #     print("Source Language:", french_translation.get("source_language_code"))
        # except Exception as e:
        #     print(f"Error during translation: {e}")
