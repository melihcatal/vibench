import os
from openai import OpenAI


def moderate_transcript_text(text: str) -> dict:
    """
    Moderates a piece of text using OpenAI's Moderation API.

    Args:
        text: The text to moderate.

    Returns:
        A dictionary containing the moderation results.
    """
    # The OPENAI_API_KEY environment variable is used by default by the client.
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    response = client.moderations.create(input=text, model="text-moderation-latest")
    
    result = response.results[0]
    
    return result.model_dump()


# Example usage:
# if __name__ == '__main__':
#     clean_text = "This is a perfectly normal transcript."
#     flagged_text = "I am going to threaten to do something bad."

#     print("--- Moderating clean text ---")
#     clean_result = moderate_transcript_text(clean_text)
#     print(f"Flagged: {clean_result['flagged']}")
#     for category, flagged in clean_result['categories'].items():
#         if flagged:
#             print(f"  - {category}: {clean_result['category_scores'][category]}")

#     print("\n--- Moderating flagged text ---")
#     flagged_result = moderate_transcript_text(flagged_text)
#     print(f"Flagged: {flagged_result['flagged']}")
#     for category, flagged in flagged_result['categories'].items():
#         if flagged:
#             print(f"  - {category}: {flagged_result['category_scores'][category]}")
