import os
from openai import OpenAI

def moderate_text(text: str):
    """
    Scores user text for unsafe or policy-violating content using OpenAI's Moderation API.
    """
    try:
        # OpenAI API key should be set as an environment variable for security
        # For example: os.environ["OPENAI_API_KEY"] = "YOUR_API_KEY"
        client = OpenAI(
            api_key=os.environ.get("OPENAI_API_KEY")
        )

        response = client.moderations.create(input=text)
        
        # The moderation API returns a list of results, we typically care about the first one for a single input
        moderation_result = response.results[0]
        
        return moderation_result

    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    test_text_safe = "Hello, world! This is a perfectly safe message."
    test_text_unsafe = "I hate you, you are a horrible person."

    print(f"Moderating safe text: '{test_text_safe}'")
    result_safe = moderate_text(test_text_safe)
    print(f"Result for safe text: {result_safe.flagged}")
    if result_safe.flagged:
        print(f"Categories: {result_safe.categories}")
        print(f"Category Scores: {result_safe.category_scores}")

    print(f"\nModerating unsafe text: '{test_text_unsafe}'")
    result_unsafe = moderate_text(test_text_unsafe)
    print(f"Result for unsafe text: {result_unsafe.flagged}")
    if result_unsafe.flagged:
        print(f"Categories: {result_unsafe.categories}")
        print(f"Category Scores: {result_unsafe.category_scores}")
