import os
import openai
from openai import OpenAI
from messaging_models import EventMessage

def summarize_message_data(event_message: EventMessage) -> str:
    # Ensure OPENAI_API_KEY is set in environment variables
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    client = OpenAI(api_key=api_key)

    message_content = str(event_message.data)
    prompt = f"Summarize the following event data in one concise sentence: {message_content}"

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Or any other suitable model like "gpt-4"
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes event data."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=50
        )
        summary = response.choices[0].message.content.strip()
        print(f"Summary: {summary}")
        return summary
    except openai.APIError as e:
        print(f"OpenAI API error: {e}")
        return f"Error summarizing message: {e}"
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return f"Error summarizing message: {e}"

if __name__ == "__main__":
    # Example usage with a dummy EventMessage
    from datetime import datetime
    sample_event = EventMessage(
        event_id="test-123",
        event_type="test.summary",
        data={
            "user_id": "user_abc",
            "action": "item_added_to_cart",
            "item_id": "product-xyz",
            "quantity": 2,
            "price": 25.99,
            "cart_total": 51.98,
            "timestamp": datetime.utcnow().isoformat()
        },
        source="test_app",
        timestamp=datetime.utcnow().isoformat()
    )
    print("\n--- Summarizing Sample Event ---")
    summarize_message_data(sample_event)
