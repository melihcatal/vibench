from typing import Dict, Any, Optional
import vertexai
from vertexai.preview.language_models import TextGenerationModel

def check_text_safety(text_content: str, project_id: str, location: str = "us-central1") -> Optional[Dict[str, Any]]:
    """Checks user-generated text content for safety attributes using Google Cloud Vertex AI.

    Args:
        text_content (str): The text content to check for safety.
        project_id (str): Your Google Cloud project ID.
        location (str): The Google Cloud region for Vertex AI.

    Returns:
        Optional[Dict[str, Any]]: A dictionary containing safety attributes and scores, or None if the check fails.
    """
    vertexai.init(project=project_id, location=location)
    # Use a text generation model that supports safety attributes in its response
    # The 'text-bison@001' model (or similar) often provides safety attributes.
    model = TextGenerationModel.from_pretrained("text-bison@001")

    try:
        response = model.predict(
            text_content,
            safety_settings={  # Explicitly request safety attributes
                # Example: You can set thresholds here if needed
            }
        )

        # The safety attributes are typically found in the _http_response.json()
        # or similar internal structure of the response object, as they are not
        # directly exposed as a top-level property on TextGenerationResponse.
        # For a robust implementation, you might need to parse the raw API response
        # or use a different client library/method that directly exposes safety scores.
        # For demonstration purposes, we'll simulate or look for common patterns.

        # Note: The Vertex AI Python SDK's `predict` method for `TextGenerationModel`
        # does not directly expose safety attributes as easily as the GenerativeModel.
        # To get explicit safety scores, you might need to use the `GenerativeModel`
        # with `generate_content` and inspect the `prompt_feedback` or `candidate_feedback`
        # for `safety_ratings`.

        # Let's switch to GenerativeModel if we want structured safety ratings directly.
        # This requires the Gemini API, which has built-in safety features.
        from vertexai.generative_models import GenerativeModel
        gemini_model = GenerativeModel("gemini-pro") # Or gemini-pro-vision for multimodal

        response_gemini = gemini_model.generate_content(text_content,
            safety_settings=[
                {
                    "category": "HARM_CATEGORY_HARASSMENT",
                    "threshold": "BLOCK_NONE"
                },
                {
                    "category": "HARM_CATEGORY_HATE_SPEECH",
                    "threshold": "BLOCK_NONE"
                },
                {
                    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    "threshold": "BLOCK_NONE"
                },
                {
                    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                    "threshold": "BLOCK_NONE"
                },
            ]
        )

        if response_gemini.prompt_feedback and response_gemini.prompt_feedback.safety_ratings:
            safety_results = {
                "blocked": response_gemini.prompt_feedback.block_reason is not None,
                "ratings": [{
                    "category": rating.category.name,
                    "probability": rating.probability.name,
                    "blocked": rating.blocked
                } for rating in response_gemini.prompt_feedback.safety_ratings]
            }
            print("Text safety check completed using Gemini Pro.")
            return safety_results
        else:
            print("No safety ratings returned by Gemini Pro (or no issues found).")
            return {"blocked": False, "ratings": []}

    except Exception as e:
        print(f"Error checking text safety with Vertex AI: {e}")
        return None

if __name__ == "__main__":
    # Example Usage:
    # Replace 'your-gcp-project-id' with your actual Google Cloud Project ID
    # Ensure you have enabled the Vertex AI API and have appropriate permissions.
    # For local execution, ensure gcloud is authenticated or GOOGLE_APPLICATION_CREDENTIALS is set.
    GCP_PROJECT_ID = "your-gcp-project-id" # <<< IMPORTANT: Update this to your GCP Project ID

    safe_text = "This is a perfectly normal product review, very positive!"
    unsafe_text_harassment = "You are an idiot and your product sucks!"
    # Note: Explicitly dangerous content might be blocked by default at higher levels,
    # so setting thresholds to BLOCK_NONE helps in seeing the ratings.

    print("\nChecking safe text...")
    try:
        safe_result = check_text_safety(safe_text, GCP_PROJECT_ID)
        if safe_result:
            print(f"Safe Text Result: {safe_result}")

        print("\nChecking potentially unsafe text (harassment category)...")
        unsafe_result = check_text_safety(unsafe_text_harassment, GCP_PROJECT_ID)
        if unsafe_result:
            print(f"Unsafe Text Result: {unsafe_result}")

    except Exception as e:
        print(f"Example usage failed: {e}")
