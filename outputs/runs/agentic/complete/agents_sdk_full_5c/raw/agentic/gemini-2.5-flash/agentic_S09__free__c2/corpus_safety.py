from google.cloud import aiplatform
from typing import List, Dict, Any

def check_corpus_safety(project_id: str, location: str, texts: List[str]) -> Dict[str, List[Dict[str, Any]]]:
    """Checks the safety attributes of a corpus of text using Vertex AI's Gemini Pro model.

    This function sends text inputs to a generative model and retrieves safety attribute scores.

    Args:
        project_id: Your Google Cloud project ID.
        location: The region for the Vertex AI endpoint (e.g., "us-central1").
        texts: A list of text strings to check for safety.

    Returns:
        A dictionary where keys are the original texts and values are lists of safety attributes
        and scores returned by the model for that text.
    """
    aiplatform.init(project=project_id, location=location)
    model = aiplatform.GenerativeModel("gemini-pro") # Gemini Pro for content moderation/safety attributes

    results = {}
    for i, text in enumerate(texts):
        # For safety checking, we generally just send the text and inspect the response's safety_attributes.
        # The prompt itself can be simple as we're interested in the inherent safety of the text.
        try:
            response = model.generate_content(text, safety_settings=None)
            safety_attrs = []
            if response.prompt_feedback and response.prompt_feedback.safety_ratings:
                for rating in response.prompt_feedback.safety_ratings:
                    safety_attrs.append({"category": rating.category.name, "probability": rating.probability.name})
            results[text] = safety_attrs
        except Exception as e:
            results[text] = [{"error": str(e), "message": "Could not get safety attributes."}]

    return results

if __name__ == '__main__':
    # Example usage:
    # from google.cloud.aiplatform_v1beta1.types import HarmCategory, SafetyRating

    # # Replace with your actual project_id and location
    # PROJECT_ID = "your-project-id"
    # LOCATION = "us-central1"

    # sample_corpus = [
    #     "This is a perfectly safe sentence.",
    #     "I will harm you.", # Example of potentially unsafe content
    #     "The weather is nice today."
    # ]

    # safety_checks = check_corpus_safety(
    #     project_id=PROJECT_ID,
    #     location=LOCATION,
    #     texts=sample_corpus
    # )
    # for text, ratings in safety_checks.items():
    #     print(f"Text: \"{text}\"\n  Safety Ratings: {ratings}\n")
    pass
