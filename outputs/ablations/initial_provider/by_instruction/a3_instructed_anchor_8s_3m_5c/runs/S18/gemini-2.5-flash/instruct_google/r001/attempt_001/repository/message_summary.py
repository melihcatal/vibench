import os
from openai import OpenAI
from messaging_models import PubSubEvent

def summarize_message(event: PubSubEvent) -> str:
    openai_api_key = os.environ.get("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    client = OpenAI(api_key=openai_api_key)

    message_content = event.to_json() # Assuming event.data is the content to summarize

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes technical messages."},
                {"role": "user", "content": f"Please summarize the following message: {message_content}"}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error summarizing message with OpenAI: {e}")
        return ""
