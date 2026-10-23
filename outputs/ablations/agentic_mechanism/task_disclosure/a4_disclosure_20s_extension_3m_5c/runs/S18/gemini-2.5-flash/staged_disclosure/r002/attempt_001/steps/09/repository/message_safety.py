import os
import openai

def check_unsafe_content(text: str) -> dict:
    """
    Checks message payload text for unsafe content using OpenAI's Moderation API.

    Args:
        text: The text content to check.

    Returns:
        A dictionary containing the moderation results.
    """
    try:
        # OpenAI API key is typically loaded from an environment variable
        openai.api_key = os.getenv("OPENAI_API_KEY")
        if not openai.api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set.")

        response = openai.Moderation.create(
            input=text
        )
        return response
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    test_message_safe = "Hello, how are you today?"
    test_message_unsafe = "I want to kill you."

    print(f"Checking message: \"{test_message_safe}\"")
    result_safe = check_unsafe_content(test_message_safe)
    print("Result:", result_safe)
    print("\n")

    print(f"Checking message: \"{test_message_unsafe}\"")
    result_unsafe = check_unsafe_content(test_message_unsafe)
    print("Result:", result_unsafe)
