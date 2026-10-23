import os
from google.cloud import translate_v2 as translate
from messaging_models import EventMessage

def translate_message_payload(event_message: EventMessage, target_language: str = "es") -> dict:
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # or that the environment has appropriate Google Cloud authentication.
    
    # The text to translate should be extracted from the event_message.data
    # For this example, let's assume a key 'customer_facing_text' or similar exists.
    text_to_translate = event_message.data.get("customer_facing_text")
    
    if not text_to_translate:
        print("No 'customer_facing_text' found in event data for translation.")
        return {"error": "No translatable text found", "original_data": event_message.data}

    print(f"Translating text to {target_language}: {text_to_translate[:50]}...")

    translate_client = translate.Client()

    try:
        result = translate_client.translate(text_to_translate, target_language=target_language)
        translated_text = result["translatedText"]
        
        translated_payload = event_message.data.copy()
        translated_payload["customer_facing_text_translated"] = translated_text
        translated_payload["translation_target_language"] = target_language

        print(f"Translated text: {translated_text}")
        return translated_payload
    except Exception as e:
        print(f"Error during translation: {e}")
        return {"error": str(e), "original_data": event_message.data}

if __name__ == "__main__":
    # Example usage with a dummy EventMessage
    from datetime import datetime
    sample_event = EventMessage(
        event_id="trans-123",
        event_type="user.notification",
        data={
            "user_id": "user_jkl",
            "notification_type": "order_confirmation",
            "customer_facing_text": "Your order has been successfully placed. Thank you for your purchase!",
            "timestamp": datetime.utcnow().isoformat()
        },
        source="test_translate_app",
        timestamp=datetime.utcnow().isoformat()
    )

    print("\n--- Translating Sample Event to Spanish ---")
    translated_data = translate_message_payload(sample_event, "es")
    print(f"Translated data: {translated_data}")

    print("\n--- Translating Sample Event to French ---")
    translated_data_fr = translate_message_payload(sample_event, "fr")
    print(f"Translated data: {translated_data_fr}")
