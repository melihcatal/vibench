import os
import openai
from openai import OpenAI
from messaging_models import EventMessage

def check_message_safety(event_message: EventMessage) -> dict:
    # Ensure OPENAI_API_KEY is set in environment variables
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    client = OpenAI(api_key=api_key)

    # Assuming the message payload has a 'text' key or similar for content to check
    text_to_check = event_message.data.get("message_content", str(event_message.data))

    print(f"Checking safety for text: {text_to_check[:100]}...")

    try:
        response = client.moderations.create(input=text_to_check)
        moderation_result = response.results[0]
        
        print(f"Moderation flagged: {moderation_result.flagged}")
        if moderation_result.flagged:
            print("Categories flagged:")
            for category, is_flagged in moderation_result.categories.items():
                if is_flagged:
                    print(f"  - {category}: {is_flagged} (score: {moderation_result.category_scores[category]:.4f})")
        return moderation_result.model_dump()
    except openai.APIError as e:
        print(f"OpenAI API error: {e}")
        return {"error": str(e), "flagged": True}
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return {"error": str(e), "flagged": True}

if __name__ == "__main__":
    # Example usage with a dummy EventMessage
    from datetime import datetime
    sample_event_safe = EventMessage(
        event_id="safe-123",
        event_type="content.check",
        data={
            "user_id": "user_def",
            "message_content": "This is a perfectly safe message about puppies and rainbows.",
            "timestamp": datetime.utcnow().isoformat()
        },
        source="test_safety_app",
        timestamp=datetime.utcnow().isoformat()
    )

    sample_event_unsafe = EventMessage(
        event_id="unsafe-456",
        event_type="content.check",
        data={
            "user_id": "user_ghi",
            "message_content": "I hate you! You are a terrible person!",
            "timestamp": datetime.utcnow().isoformat()
        },
        source="test_safety_app",
        timestamp=datetime.utcnow().isoformat()
    )

    print("\n--- Checking Safe Event ---")
    check_message_safety(sample_event_safe)

    print("\n--- Checking Unsafe Event ---")
    check_message_safety(sample_event_unsafe)
