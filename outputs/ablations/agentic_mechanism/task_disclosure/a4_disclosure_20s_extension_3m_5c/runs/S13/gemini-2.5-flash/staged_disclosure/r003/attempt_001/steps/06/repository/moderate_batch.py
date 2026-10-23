import os
from openai import OpenAI

def moderate_batch(messages: list[str]) -> list[dict]:
    """
    Moderates a batch of user messages using OpenAI's moderation API.

    Args:
        messages: A list of user messages (strings) to moderate.

    Returns:
        A list of dictionaries, where each dictionary contains the moderation
        decision for the corresponding message.
    """
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    
    # OpenAI's moderation endpoint expects a single string or a list of strings
    # For batch moderation, pass the list directly.
    response = client.moderations.create(input=messages)
    
    moderation_results = []
    for result in response.results:
        moderation_results.append({
            "flagged": result.flagged,
            "categories": {category.category: category.triggered for category in result.categories},
            "category_scores": {category.category: category.score for category in result.category_scores}
        })
    return moderation_results

if __name__ == "__main__":
    # Example usage:
    user_messages = [
        "I love this product!",
        "I will kill you!",
        "This is a test message.",
        "Let's talk about some illegal stuff."
    ]

    print("Moderating messages...")
    results = moderate_batch(user_messages)

    for i, message in enumerate(user_messages):
        print(f"\nMessage: "{message}"")
        print(f"  Flagged: {results[i]['flagged']}")
        if results[i]['flagged']:
            print("  Categories Triggered:")
            for category, triggered in results[i]['categories'].items():
                if triggered:
                    print(f"    - {category}: True (Score: {results[i]['category_scores'][category]:.4f})")
    print("\nNote: Ensure OPENAI_API_KEY environment variable is set for this to work.")
