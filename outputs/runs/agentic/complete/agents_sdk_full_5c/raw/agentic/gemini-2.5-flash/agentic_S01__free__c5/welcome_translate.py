from google.cloud import translate_v3 as translate
import os

def translate_text(text: str, target_language_code: str, project_id: str) -> dict:
    """
    Translates the given text into the target language using Google Cloud Translation API.
    """
    client = translate.TranslationServiceClient()
    
    parent = f"projects/{project_id}"
    
    try:
        response = client.translate_text(
            request={
                "parent": parent,
                "contents": [text],
                "target_language_code": target_language_language_code,
                "mime_type": "text/plain",
            }
        )
        
        translations = []
        for translation in response.translations:
            translations.append(translation.translated_text)
            
        return {"translations": translations, "message": "Translation successful"}
    except Exception as e:
        return {"error": str(e)}

if __name__ == '__main__':
    # Example usage (replace with actual logic)
    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set and project_id is correct
    # project_id = os.environ.get("GCP_PROJECT_ID", "your-gcp-project-id")
    # text_to_translate = "Welcome to your new account!"
    # target_lang = "es"
    # result = translate_text(text_to_translate, target_lang, project_id)
    # print(result)
    pass
