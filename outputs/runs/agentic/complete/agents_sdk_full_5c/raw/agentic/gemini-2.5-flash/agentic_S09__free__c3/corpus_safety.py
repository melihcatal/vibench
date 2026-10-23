import openai
from embeddings_client import get_openai_client
from typing import List, Dict, Any

def check_corpus_safety(texts: List[str]) -> List[Dict[str, Any]]:
    """Checks a list of text strings for safety using OpenAI's Moderation API.

    Args:
        texts: A list of text strings to check.

    Returns:
        A list of dictionaries, where each dictionary contains the moderation
        results for the corresponding text string.
    """
    client = get_openai_client()

    # OpenAI Moderation API can take a list of texts
    response = client.moderations.create(input=texts)

    results = []
    for result in response.results:
        results.append({
            "flagged": result.flagged,
            "categories": {
                cat.name: cat.violated for cat in result.categories.model_fields.values()
            },
            "category_scores": {
                score.name: score.score for score in result.category_scores.model_fields.values()
            },
        })

    return results

if __name__ == '__main__':
    # Example usage (for testing, not part of final submission requirements)
    # from dotenv import load_dotenv
    # load_dotenv()

    # corpus_texts = [
    #     "I love fluffy kittens!",
    #     "I hate you and want to hurt you.",
    #     "This is a neutral statement."
    # ]

    # safety_checks = check_corpus_safety(corpus_texts)
    # for i, check in enumerate(safety_checks):
    #     print(f"\nText {i+1}: '{corpus_texts[i]}'")
    #     print(f"Flagged: {check['flagged']}")
    #     if check['flagged']:
    #         print(f"Categories violated: { {k: v for k, v in check['categories'].items() if v} }")
    pass
