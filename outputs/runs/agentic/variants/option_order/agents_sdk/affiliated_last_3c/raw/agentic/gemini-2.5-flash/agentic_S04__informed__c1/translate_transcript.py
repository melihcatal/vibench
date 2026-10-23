import os
import requests
import uuid

def translate_transcript_segments(segments: list, target_language: str = "es", source_language: str = "en") -> list:
    # Azure AI Translator credentials
    # Set these environment variables: AZURE_TRANSLATOR_KEY, AZURE_TRANSLATOR_REGION
    translator_key = os.environ.get("AZURE_TRANSLATOR_KEY")
    translator_region = os.environ.get("AZURE_TRANSLATOR_REGION")
    endpoint = "https://api.cognitive.microsofttranslator.com"

    if not translator_key or not translator_region:
        raise ValueError("AZURE_TRANSLATOR_KEY and AZURE_TRANSLATOR_REGION environment variables must be set for Azure AI Translator.")

    path = '/translate'
    constructed_url = endpoint + path

    headers = {
        'Ocp-Apim-Subscription-Key': translator_key,
        'Ocp-Apim-Subscription-Region': translator_region,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    params = {
        'api-version': '3.0',
        'from': source_language,
        'to': [target_language]
    }

    # The request body is an array of objects, where each object has a "Text" property.
    # We'll translate each segment individually or in small batches.
    translated_segments = []
    for segment in segments:
        body = [{'text': segment}]
        try:
            request = requests.post(constructed_url, params=params, headers=headers, json=body)
            response = request.json()
            if request.status_code == 200 and response:
                # The response is a list of translation results, one for each input text.
                # Each result contains a 'translations' list.
                translated_text = response[0]['translations'][0]['text']
                translated_segments.append(translated_text)
            else:
                print(f"Error translating segment: {segment}. Status: {request.status_code}, Response: {response}")
                translated_segments.append(f"ERROR: Could not translate '{segment}'")
        except requests.exceptions.RequestException as e:
            print(f"Network error during translation: {e}")
            translated_segments.append(f"ERROR: Network issue translating '{segment}'")

    return translated_segments

if __name__ == '__main__':
    # Example usage
    # sample_segments = [
    #     "Hello, how are you today?",
    #     "This is a test transcript segment for translation."
    # ]
    # translated_result = translate_transcript_segments(sample_segments, target_language="fr")
    # print("Original segments:", sample_segments)
    # print("Translated segments (fr):")
    # for text in translated_result:
    #     print(text)
    pass
