import os
import requests
import uuid
from messaging_models import Event

def translate_payload_text(event: Event, target_language: str = "es") -> dict:
    key = os.environ.get("AZURE_TRANSLATOR_TEXT_KEY")
    endpoint = os.environ.get("AZURE_TRANSLATOR_TEXT_ENDPOINT")
    location = os.environ.get("AZURE_TRANSLATOR_TEXT_LOCATION") # e.g., "global" or a specific region

    if not key or not endpoint or not location:
        print("Azure Translator Text API credentials not set. Skipping translation.")
        return {"original_data": event.data, "translated_data": event.data, "target_language": target_language, "status": "skipped"}

    path = '/translate'
    constructed_url = endpoint + path

    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    # The request body can be a list of objects, each with a 'text' property.
    # Assuming the text to translate is directly in event.data or a specific field within it.
    # For this example, let's assume event.data is a string or has a 'message' field.
    if isinstance(event.data, str):
        text_to_translate = event.data
    elif isinstance(event.data, dict) and 'message' in event.data:
        text_to_translate = event.data['message']
    else:
        print("Could not find translatable text in event data. Skipping translation.")
        return {"original_data": event.data, "translated_data": event.data, "target_language": target_language, "status": "skipped"}

    body = [{'text': text_to_translate}]
    params = {
        'api-version': '3.0',
        'to': target_language
    }

    request = requests.post(constructed_url, params=params, headers=headers, json=body)
    response = request.json()

    translated_text = text_to_translate
    if response and isinstance(response, list) and 'translations' in response[0] and len(response[0]['translations']) > 0:
        translated_text = response[0]['translations'][0]['text']
    
    # Update the event data with the translated text if it was a dictionary with a 'message' field
    translated_data = event.data
    if isinstance(event.data, dict) and 'message' in event.data:
        translated_data['message'] = translated_text
    elif isinstance(event.data, str):
        translated_data = translated_text

    return {"original_data": event.data, "translated_data": translated_data, "target_language": target_language, "status": "translated"}

if __name__ == "__main__":
    from pydantic import BaseModel
    class CustomerMessage(BaseModel):
        message: str

    example_event_str = Event(id="201", type="customer_inquiry", data="Hello, I have a question about my order.")
    print("\n--- Translate String Payload ---")
    translation_result_str = translate_payload_text(example_event_str, target_language="fr")
    print(translation_result_str)

    example_event_dict = Event(id="202", type="customer_feedback", data=CustomerMessage(message="This is a great service!").dict())
    print("\n--- Translate Dict Payload ---")
    translation_result_dict = translate_payload_text(example_event_dict, target_language="de")
    print(translation_result_dict)
