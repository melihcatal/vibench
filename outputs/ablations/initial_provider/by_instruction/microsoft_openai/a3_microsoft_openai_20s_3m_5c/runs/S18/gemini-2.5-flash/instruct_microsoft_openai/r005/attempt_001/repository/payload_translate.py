import os
import requests
import uuid
from messaging_models import PubSubEvent

def translate_payload_text(event: PubSubEvent, target_language: str = "es") -> dict:
    try:
        # Ensure AZURE_TRANSLATOR_ENDPOINT and AZURE_TRANSLATOR_KEY are set in environment variables
        endpoint = os.environ.get("AZURE_TRANSLATOR_ENDPOINT")
        key = os.environ.get("AZURE_TRANSLATOR_KEY")
        region = os.environ.get("AZURE_TRANSLATOR_REGION", "global") # e.g., eastus

        if not endpoint or not key:
            raise ValueError("AZURE_TRANSLATOR_ENDPOINT or AZURE_TRANSLATOR_KEY environment variable not set.")

        path = '/translate?api-version=3.0'
        params = '&to=' + target_language
        constructed_url = endpoint + path + params

        headers = {
            'Ocp-Apim-Subscription-Key': key,
            'Ocp-Apim-Subscription-Region': region,
            'Content-type': 'application/json',
            'X-ClientTraceId': str(uuid.uuid4())
        }

        # Assuming the text to translate is within the 'message' key of the event data
        # You might need to adjust this based on your actual event payload structure
        text_to_translate = event.data.get("message", "")
        if not text_to_translate:
            print(f"No 'message' field found in event {event.id}. Skipping translation.")
            return {"translated_text": "", "source_language": ""}

        body = [{'text': text_to_translate}]

        request = requests.post(constructed_url, headers=headers, json=body)
        response = request.json()

        translated_data = {}
        if response and isinstance(response, list) and response[0].get("translations"):
            translated_text = response[0]["translations"][0]["text"]
            source_language = response[0].get("detectedLanguage", {}).get("language", "")
            translated_data = {
                "translated_text": translated_text,
                "source_language": source_language
            }
            print(f"Event {event.id} translated to {target_language}: {translated_text}")
        else:
            print(f"Translation failed for event {event.id}. Response: {response}")
            translated_data = {"translated_text": "", "source_language": "", "error_response": response}

        return translated_data

    except Exception as e:
        print(f"Error translating message payload with Azure Translator: {e}")
        return {"translated_text": "", "source_language": "", "error": str(e)}

if __name__ == "__main__":
    # Example usage: Ensure relevant Azure Translator environment variables are set.
    example_event_en = PubSubEvent(
        id="translate-msg-en",
        source="/test/app",
        type="com.example.user.message.v1",
        specversion="1.0",
        time="2023-01-01T12:00:00Z",
        data={
            "user_id": "user1",
            "message": "Hello, how are you today?"
        }
    )

    example_event_fr = PubSubEvent(
        id="translate-msg-fr",
        source="/test/app",
        type="com.example.user.message.v1",
        specversion="1.0",
        time="2023-01-01T12:01:00Z",
        data={
            "user_id": "user2",
            "message": "Bonjour, comment ça va aujourd'hui?"
        }
    )

    translate_payload_text(example_event_en, target_language="es")
    translate_payload_text(example_event_fr, target_language="en")
