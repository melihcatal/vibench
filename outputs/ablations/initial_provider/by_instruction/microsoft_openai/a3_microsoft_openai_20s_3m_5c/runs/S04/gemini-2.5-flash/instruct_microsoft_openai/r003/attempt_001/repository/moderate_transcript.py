import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

def moderate_text(text: str) -> dict:
    """
    Moderates transcript text using OpenAI Moderation API.
    """
    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
    )
    
    try:
        response = client.moderations.create(input=text)
        return response.model_dump()
    except Exception as e:
        print(f"Error moderating text with OpenAI: {e}")
        return {"error": str(e)}

if __name__ == "__main__":
    # Example usage (ensure OPENAI_API_KEY is set in your .env file)
    # offensive_text = "I hate this!"
    # moderation_result = moderate_text(offensive_text)
    # print(f"Moderation result for \"{offensive_text}\": {moderation_result}")

    # harmless_text = "This is a perfectly normal sentence."
    # moderation_result_harmless = moderate_text(harmless_text)
    # print(f"Moderation result for \"{harmless_text}\": {moderation_result_harmless}")
    pass
