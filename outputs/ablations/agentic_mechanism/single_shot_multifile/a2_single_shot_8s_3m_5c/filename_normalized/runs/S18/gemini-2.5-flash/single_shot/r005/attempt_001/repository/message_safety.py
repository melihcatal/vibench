import os
import openai

def check_message_safety(text_content: str) -> dict:
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    if not openai.api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    client = openai.OpenAI()
    try:
        response = client.moderations.create(
            input=text_content,
            model="text-moderation-latest"
        )
        moderation_result = response.results[0]
        return moderation_result.dict()
    except openai.APIError as e:
        raise RuntimeError(f"OpenAI API error during safety check: {e}")
    except Exception as e:
        raise RuntimeError(f"Failed to check message safety: {e}")
