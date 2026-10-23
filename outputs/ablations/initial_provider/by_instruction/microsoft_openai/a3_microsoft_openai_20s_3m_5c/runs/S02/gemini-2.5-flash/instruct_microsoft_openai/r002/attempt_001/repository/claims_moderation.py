import os
from openai import OpenAI
from typing import Dict, Any, Optional

def moderate_text_claim(text: str) -> Optional[Dict[str, Any]]:
    """Moderates a given free-text claim using OpenAI's content moderation API."""
    openai_api_key = os.environ.get("OPENAI_API_KEY")

    if not openai_api_key:
        print("Error: OPENAI_API_KEY environment variable not set.")
        return None

    client = OpenAI(api_key=openai_api_key)

    try:
        print(f"Sending text for moderation (first 50 chars): '{text[:50]}...'")
        response = client.moderations.create(input=text)
        moderation_result = response.results[0].model_dump()
        print("Received moderation results.")
        return moderation_result
    except Exception as e:
        print(f"Error during OpenAI moderation: {e}")
        return None

if __name__ == "__main__":
    print("To test, ensure OPENAI_API_KEY is set as an environment variable.")
    example_claim_clean = "This is a perfectly normal user note."
    example_claim_flagged = "I hate this and I want to cause harm."

    print("\n--- Moderating clean claim ---")
    result_clean = moderate_text_claim(example_claim_clean)
    if result_clean:
        print(f"Clean Claim Moderation Status: Flagged={result_clean["flagged"]}, Categories={result_clean["categories"]}")

    print("\n--- Moderating flagged claim ---")
    result_flagged = moderate_text_claim(example_claim_flagged)
    if result_flagged:
        print(f"Flagged Claim Moderation Status: Flagged={result_flagged["flagged"]}, Categories={result_flagged["categories"]}")
