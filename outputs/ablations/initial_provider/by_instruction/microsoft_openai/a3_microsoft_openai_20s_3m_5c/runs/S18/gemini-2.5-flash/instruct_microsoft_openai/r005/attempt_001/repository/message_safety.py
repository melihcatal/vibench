import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory
from azure.core.credentials import AzureKeyCredential
from messaging_models import PubSubEvent

def check_message_safety(event: PubSubEvent) -> dict:
    try:
        # Ensure AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY are set in environment variables
        endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
        key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

        if not endpoint or not key:
            raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT or AZURE_CONTENT_SAFETY_KEY environment variable not set.")

        client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

        # For simplicity, let's check the string representation of event data.
        # In a real scenario, you might want to specifically target text fields within event.data.
        text_to_analyze = str(event.data)

        request = AnalyzeTextOptions(
            text=text_to_analyze,
            categories=[TextCategory.HATE, TextCategory.VIOLENCE, TextCategory.SELF_HARM, TextCategory.SEXUAL]
        )

        response = client.analyze_text(request)

        safety_results = {
            "hate": response.hate_result.severity if response.hate_result else -1,
            "violence": response.violence_result.severity if response.violence_result else -1,
            "self_harm": response.self_harm_result.severity if response.self_harm_result else -1,
            "sexual": response.sexual_result.severity if response.sexual_result else -1
        }

        print(f"Content safety check for event {event.id}: {safety_results}")
        return safety_results

    except Exception as e:
        print(f"Error checking message safety with Azure Content Safety: {e}")
        return {"error": str(e)}

if __name__ == "__main__":
    # Example usage: Ensure relevant Azure Content Safety environment variables are set.
    safe_event = PubSubEvent(
        id="safe-msg-1",
        source="/test/app",
        type="com.example.chat.v1",
        specversion="1.0",
        time="2023-01-01T12:00:00Z",
        data={
            "user": "Alice",
            "message": "Hello everyone, how are you doing today?"
        }
    )

    unsafe_event = PubSubEvent(
        id="unsafe-msg-1",
        source="/test/app",
        type="com.example.chat.v1",
        specversion="1.0",
        time="2023-01-01T12:01:00Z",
        data={
            "user": "Bob",
            "message": "I hate this! This is terrible!"
        }
    )

    check_message_safety(safe_event)
    check_message_safety(unsafe_event)
