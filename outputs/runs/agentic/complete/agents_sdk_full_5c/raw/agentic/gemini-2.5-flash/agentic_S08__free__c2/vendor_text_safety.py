import os
from typing import Dict, Any
from google.cloud import aiplatform
from google.cloud.aiplatform_v1beta1 import types
from document_client import DocumentClients, PROJECT_ID, LOCATION

# Vertex AI model ID for Gemini Pro (for text generation with safety features)
GEMINI_PRO_MODEL_ID = os.environ.get("GEMINI_PRO_MODEL_ID", "gemini-pro")

def moderate_vendor_notes(text: str) -> Dict[str, Any]:
    """Moderates vendor notes or memo fields using Google Cloud Vertex AI's safety features.

    Args:
        text: The text content to moderate.

    Returns:
        A dictionary containing moderation results, including safety attributes.
    """
    client = DocumentClients.get_vertex_ai_prediction_client()

    # Prepare the prompt for the generative model. We're not asking it to *generate* here,
    # but rather using its internal safety filters on the input.
    # For direct content moderation, you would typically use a dedicated moderation API.
    # However, for this task, using the safety features of a generative model is a valid integration.
    # A more direct moderation tool would be Google Cloud Perspective API or OpenAI Moderation.
    # Let's frame it as asking the model to process the text, and its response will include safety attributes.

    # The actual safety scores are part of the `Citation` or `SafetyAttributes` in the response,
    # which might not be directly exposed in a simple predict() call depending on how it's wrapped.
    # A more robust solution for explicit safety scores would involve the dedicated Vertex AI Safety API
    # or using the `GenerateContent` method which exposes safety ratings more clearly.
    # For `PredictionServiceClient.predict`, safety attributes might be in `metadata` or implicitly handled.

    # A workaround for `predict` with safety: We'll construct a dummy generation task.
    # The goal is to get the system to evaluate the input's safety.
    prompt_for_safety = f"Evaluate the safety of the following text: '''{text}'''\n"
    instance = types.Instance(content=prompt_for_safety)

    # Setting a low temperature and max_output_tokens since we don't care about the generated text
    # as much as the implicit safety check by the model.
    parameters = types.PredictRequest.Parameter(
        temperature=0.0,
        max_output_tokens=10,
        # It's challenging to directly access safety scores from `PredictionServiceClient.predict`
        # in the same way as `GenerateContent` for `gemini-pro` where safety_ratings are explicit.
        # A more direct approach for safety evaluation would be to use a dedicated moderation API like Perspective API.
        # For this example, we will assume an internal mechanism of Vertex AI flags unsafe inputs.
        # If the model refuses to respond due to safety, that's a signal.
    )

    moderation_result = {"is_safe": True, "reasons": []}
    try:
        # When using `gemini-pro` via `PredictionServiceClient`, if the input violates safety policies,
        # the prediction might be empty or raise an error, or the response object might have safety attributes.
        # The specific structure to check for safety varies slightly across SDK versions and methods.
        response = client.predict(
            endpoint=f"projects/{PROJECT_ID}/locations/{LOCATION}/publishers/google/models/{GEMINI_PRO_MODEL_ID}",
            instances=[instance],
            parameters=parameters,
        )

        # In practice, for explicit safety scores, you'd use a different API or method like `GenerativeModel.generate_content`
        # and inspect `safety_ratings`. Since `PredictionServiceClient.predict` doesn't directly expose `safety_ratings` in a simple way,
        # we'll infer safety from the presence of predictions or lack thereof.
        # A more direct integration for safety would be Google Cloud's Perspective API.

        # Let's adjust to use a more concrete provider: Google Cloud Perspective API.
        # This offers explicit content moderation scores.
        # Since the problem statement doesn't strictly enforce Vertex AI for *all* LLM related tasks.

        # --- Re-aligning to use Google Cloud Perspective API for explicit moderation ---
        # Google Cloud Perspective API requires an API key and a call to a REST endpoint.
        # The `google.cloud.language_v1` client is not for Perspective API.
        # I need to use `requests` for Perspective API or find an SDK.
        # The Perspective API is a public API hosted at `commentanalyzer.googleapis.com`.

        # The structure is: https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze
        # I will use `requests` for this.

        # This means I need to adjust `document_client.py` if I want to centralize it, but for a single file, `requests` is fine.

        # Re-writing this part to use Perspective API.
        API_KEY = os.environ.get("PERSPECTIVE_API_KEY", "YOUR_PERSPECTIVE_API_KEY")
        PERSPECTIVE_API_ENDPOINT = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

        analyze_request = {
            'comment': {'text': text},
            'requestedAttributes': {
                'TOXICITY': {}, # Example attributes, can add others like INSULT, PROFANITY, FLIRTATION
                'SEXUALLY_EXPLICIT': {},
                'THREAT': {},
                'IDENTITY_ATTACK': {},
            },
            'languages': ["en"],
            'doNotStore': True # Optional: Helps with privacy by not storing the text
        }

        perspective_response = requests.post(PERSPECTIVE_API_ENDPOINT + '?key=' + API_KEY, json=analyze_request)
        perspective_response.raise_for_status()
        analysis = perspective_response.json()

        # Check for high scores in any attribute
        threshold = 0.7 # Example threshold
        for attribute, scores in analysis.get('attributeScores', {}).items():
            score = scores.get('summaryScore', {}).get('value', 0.0)
            if score > threshold:
                moderation_result["is_safe"] = False
                moderation_result["reasons"].append({"attribute": attribute, "score": score})

        moderation_result["full_analysis"] = analysis
        return moderation_result

    except Exception as e:
        print(f"Error moderating with Perspective API: {e}")
        moderation_result["error"] = str(e)
        moderation_result["is_safe"] = False # Mark as unsafe if moderation fails
        return moderation_result
