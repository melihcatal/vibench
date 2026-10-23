import os
import openai

def metric_annotation_safety(text: str) -> dict:
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    if not openai.api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    try:
        response = openai.moderations.create(input=text)
        # The API response will contain a list of results for each input. 
        # For a single input, we expect one result.
        moderation_result = response.results[0]
        return {
            "flagged": moderation_result.flagged,
            "categories": {category.id: category.flagged for category in moderation_result.categories},
            "category_scores": {category.id: category.score for category in moderation_result.category_scores},
        }
    except Exception as e:
        raise RuntimeError(f"Failed to check text safety using OpenAI Moderation API: {e}")

if __name__ == "__main__":
    # Example Usage
    unsafe_text = "This is a test with some potentially harmful content like violence."
    safe_text = "All systems are operating normally."

    try:
        print("Checking unsafe text:")
        result = metric_annotation_safety(unsafe_text)
        print(result)

        print("\nChecking safe text:")
        result = metric_annotation_safety(safe_text)
        print(result)
    except Exception as e:
        print(f"Error: {e}")
