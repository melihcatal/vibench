import os
import openai

def moderate_text(text: str) -> dict:
    """
    Moderates free-text claims or notes using OpenAI's moderation API.

    Args:
        text: The free-text claim or note to moderate.

    Returns:
        A dictionary containing the moderation results.
    """
    try:
        # Ensure your OpenAI API key is set as an environment variable
        # For example: export OPENAI_API_KEY='sk-...'
        if not os.environ.get("OPENAI_API_KEY"):
            raise ValueError("OPENAI_API_KEY environment variable not set.")

        client = openai.OpenAI(
            api_key=os.environ.get("OPENAI_API_KEY")
        )
        response = client.moderations.create(input=text)
        return response.model_dump()
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    # Example usage:
    claim1 = "I hate this product so much!"
    moderation_result1 = moderate_text(claim1)
    print(f"Moderation result for '{claim1}':")
    print(moderation_result1)

    claim2 = "This is a wonderful product, I highly recommend it."
    moderation_result2 = moderate_text(claim2)
    print(f"Moderation result for '{claim2}':")
    print(moderation_result2)

    claim3 = "I will harm anyone who uses this."
    moderation_result3 = moderate_text(claim3)
    print(f"Moderation result for '{claim3}':")
    print(moderation_result3)
