from google.cloud import translate_v3 as translate
import os
from typing import List, Dict

def translate_narration_script(
    texts: List[str],
    target_language_code: str,
    project_id: str
) -> List[Dict]:
    """Translates a list of narration scripts using Google Cloud Translation.
    
    Args:
        texts: A list of strings, where each string is a narration script segment.
        target_language_code: The ISO 639-1 language code for the target language (e.g., "es").
        project_id: Your Google Cloud Project ID.
        
    Returns:
        A list of dictionaries, each containing 'original_text' and 'translated_text'.
    """
    client = translate.TranslationServiceClient()
    parent = f"projects/{project_id}/locations/global"
    
    response = client.translate_text(
        parent=parent,
        contents=texts,
        target_language_code=target_language_code,
        # Optional: Specify source_language_code if known
        # source_language_code="en", 
        mime_type="text/plain"  # Can also be "text/html"
    )
    
    translated_results = []
    for i, translation in enumerate(response.translations):
        translated_results.append({
            "original_text": texts[i],
            "translated_text": translation.translated_text
        })
        
    return translated_results

if __name__ == '__main__':
    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set for authentication
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/credentials.json"
    
    # Replace with your actual Google Cloud Project ID
    YOUR_PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT_ID", "your-gcp-project-id")
    
    if YOUR_PROJECT_ID == "your-gcp-project-id":
        print("Please set the GOOGLE_CLOUD_PROJECT_ID environment variable or replace 'your-gcp-project-id' with your actual GCP project ID.")
    else:
        sample_scripts = [
            "Welcome to our new audio experience.",
            "This segment will discuss advanced integration patterns.",
            "Please enjoy the rest of the presentation."
        ]
        target_lang = "es" # Spanish
        
        print(f"Translating scripts to {target_lang}...")
        translations = translate_narration_script(sample_scripts, target_lang, YOUR_PROJECT_ID)
        
        for result in translations:
            print(f"Original: {result['original_text']}")
            print(f"Translated: {result['translated_text']}\n")
