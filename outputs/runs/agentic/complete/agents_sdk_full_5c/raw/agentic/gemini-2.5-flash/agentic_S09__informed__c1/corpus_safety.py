from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory
from azure.core.credentials import AzureKeyCredential
import os
from typing import List, Dict

def check_corpus_safety(texts: List[str]) -> Dict[str, Dict]:
    """Checks the safety of a corpus of text using Azure AI Content Safety.

    Args:
        texts: A list of text strings to check for safety issues.

    Returns:
        A dictionary where keys are original texts and values are dictionaries
        containing safety analysis results (e.g., severity scores for categories).
    """
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables must be set.")

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    results = {}
    for text in texts:
        try:
            request = AnalyzeTextOptions(text=text)
            response = client.analyze_text(request)
            category_scores = {}
            if response.categories_analysis:
                for category in response.categories_analysis:
                    category_scores[category.category.value] = {
                        "severity": category.severity
                    }
            results[text] = category_scores
        except Exception as e:
            results[text] = {"error": str(e)}

    return results

if __name__ == '__main__':
    sample_texts = [
        "This is a perfectly safe sentence.",
        "I hate you and want to hurt you.",
        "Some explicit content here."
    ]

    print("Checking corpus safety...")
    try:
        safety_results = check_corpus_safety(sample_texts)
        for text, result in safety_results.items():
            print(f"\nText: \"{text}\"")
            if "error" in result:
                print(f"  Error: {result["error"]}")
            else:
                for category, score_info in result.items():
                    print(f"  Category: {category}, Severity: {score_info["severity"]}")
    except ValueError as e:
        print(f"Configuration Error: {e}")
        print("Please set AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
