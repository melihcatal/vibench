import os
from openai import OpenAI

def check_text_safety(text: str) -> dict:
    # Initialize OpenAI client
    # It expects OPENAI_API_KEY environment variable to be set.
    client = OpenAI()

    try:
        response = client.moderations.create(input=text)
        moderation_result = response.results[0]
        return moderation_result.model_dump()
    except Exception as e:
        return {"error": f"Error checking text safety: {e}"}

if __name__ == "__main__":
    # Example usage
    safe_text = "This is a perfectly safe and benign statement."
    unsafe_text = "I will harm you."

    # Ensure OPENAI_API_KEY environment variable is set.
    if "OPENAI_API_KEY" not in os.environ:
        print("Please set the OPENAI_API_KEY environment variable to run this example.")
    else:
        print(f"Checking safe text: '{safe_text}'")
        safety_result_safe = check_text_safety(safe_text)
        print(f"Safety Result (Safe): {safety_result_safe}\n")

        print(f"Checking unsafe text: '{unsafe_text}'")
        safety_result_unsafe = check_text_safety(unsafe_text)
        print(f"Safety Result (Unsafe): {safety_result_unsafe}")
