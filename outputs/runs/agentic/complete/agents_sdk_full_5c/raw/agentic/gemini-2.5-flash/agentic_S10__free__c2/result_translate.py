from google.cloud import translate_v3 as translate
from model_models import LLM_Output

# Google Cloud Translation provider-identifying signal: google.cloud.translate_v3 import, translate.TranslationServiceClient

def translate_text(text: str, target_language_code: str, project_id: str) -> LLM_Output:
    """
    Translates generated model output using Google Cloud Translation API.
    """
    client = translate.TranslationServiceClient()
    location = "global" # Translation API is often global or regional

    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",
            "target_language_code": target_language_code,
        }
    )

    translated_text = response.translations[0].translated_text if response.translations else ""
    return {"translated_text": translated_text, "detected_language": response.translations[0].detected_language_code if response.translations else None}

if __name__ == '__main__':
    # Example usage (replace with your actual project ID)
    sample_text_en = "Hello, how are you? This is a test."
    
    # Replace 'your-gcp-project-id' with your actual Google Cloud Project ID
    # For demonstration, using a placeholder.
    translation_result_es = translate_text(sample_text_en, "es", project_id="your-gcp-project-id")
    print(f"Original: {sample_text_en}")
    print(f"Translated to Spanish: {translation_result_es['translated_text']} (Detected: {translation_result_es['detected_language']})")

    sample_text_fr = "Bonjour, comment ça va?"
    translation_result_en = translate_text(sample_text_fr, "en", project_id="your-gcp-project-id")
    print(f"Original: {sample_text_fr}")
    print(f"Translated to English: {translation_result_en['translated_text']} (Detected: {translation_result_en['detected_language']})")
