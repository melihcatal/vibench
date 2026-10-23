import os
from openai import OpenAI

def moderate_text_claims(text_to_moderate: str) -> dict:
    """
    Moderates free-text claims or notes using OpenAI's moderation API.
    """
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    try:
        response = client.moderations.create(input=text_to_moderate)
        moderation_result = response.results[0]
        return moderation_result.model_dump()
    except Exception as e:
        print(f"Error calling OpenAI moderation API: {e}")
        raise

if __name__ == "__main__":
    # Ensure OPENAI_API_KEY environment variable is set
    sample_claim_good = "This is a legitimate claim about user preferences."
    sample_claim_bad = "I hate this new feature, it's terrible and offensive!"

    print("Moderating a good claim...")
    try:
        result_good = moderate_text_claims(sample_claim_good)
        print("Good claim moderation result:")
        print(result_good)
    except Exception as e:
        print(f"Failed to moderate good claim: {e}")
        print("Ensure 'OPENAI_API_KEY' environment variable is set.")

    print("\nModerating a bad claim...")
    try:
        result_bad = moderate_text_claims(sample_claim_bad)
        print("Bad claim moderation result:")
        print(result_bad)
    except Exception as e:
        print(f"Failed to moderate bad claim: {e}")
        print("Ensure 'OPENAI_API_KEY' environment variable is set.")
