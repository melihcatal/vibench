import os
import cohere
from typing import List


def check_text_for_safety(text_inputs: List[str]) -> List[dict]:
    """
    Checks secret labels and notes for unsafe text using Cohere's moderate endpoint.
    """
    api_key = os.environ.get("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable not set.")

    co = cohere.Client(api_key)

    try:
        results = co.moderate(
            texts=text_inputs,
            model="moderate-english-v3.0",
        )
        return results.results
    except Exception as e:
        print(f"Error with Cohere moderation API: {e}")
        return []


if __name__ == "__main__":
    unsafe_texts = [
        "This is a perfectly fine label.",
        "This label contains hate speech and profanity.",
        "notes with personally identifiable information like user@example.com",
    ]
    safety_ratings = check_text_for_safety(unsafe_texts)
    for i, rating in enumerate(safety_ratings):
        print(f"Text: '{unsafe_texts[i]}'")
        print(f"  Toxic: {rating.toxic}")
        print(f"  Hate Speech: {rating.hate_speech}")
