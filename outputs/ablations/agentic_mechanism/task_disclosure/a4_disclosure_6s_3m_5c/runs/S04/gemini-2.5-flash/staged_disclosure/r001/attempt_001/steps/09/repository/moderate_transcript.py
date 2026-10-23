import os
import openai

def moderate_transcript(text):
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    if not openai.api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    try:
        response = openai.moderation.create(
            input=text
        )
        return response.results[0]
    except Exception as e:
        print(f"Error during moderation: {e}")
        return None
