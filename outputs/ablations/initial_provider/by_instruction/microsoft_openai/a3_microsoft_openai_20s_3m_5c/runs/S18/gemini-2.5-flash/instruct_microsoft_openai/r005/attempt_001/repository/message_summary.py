import os
import openai
from messaging_models import PubSubEvent

def summarize_message(event: PubSubEvent) -> str:
    try:
        # Ensure you have AZURE_OPENAI_API_KEY, AZURE_OPENAI_ENDPOINT, and AZURE_OPENAI_DEPLOYMENT_NAME set in your environment variables
        openai.api_type = "azure"
        openai.api_base = os.environ.get("AZURE_OPENAI_ENDPOINT")
        openai.api_version = "2023-05-15"
        openai.api_key = os.environ.get("AZURE_OPENAI_API_KEY")
        deployment_name = os.environ.get("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-35-turbo") # Default deployment name

        message_content = f"Event ID: {event.id}\nEvent Type: {event.type}\nEvent Data: {event.data}"

        response = openai.ChatCompletion.create(
            engine=deployment_name,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes event messages."},
                {"role": "user", "content": f"Please summarize the following event message:\n\n{message_content}"}
            ]
        )
        summary = response.choices[0].message.content.strip()
        print(f"Message summarized successfully: {summary}")
        return summary
    except Exception as e:
        print(f"Error summarizing message with Azure OpenAI: {e}")
        return f"Summary generation failed: {e}"

if __name__ == "__main__":
    # Example usage: Ensure relevant Azure OpenAI environment variables are set.
    example_event = PubSubEvent(
        id="test-123",
        source="/test/app",
        type="com.example.test.v1",
        specversion="1.0",
        time="2023-01-01T12:00:00Z",
        data={
            "action": "user_login",
            "user_id": "user_001",
            "ip_address": "192.168.1.1",
            "timestamp": "2023-01-01T11:59:59Z",
            "details": "User successfully logged in from a new device. Multi-factor authentication was used."
        }
    )
    summarize_message(example_event)
