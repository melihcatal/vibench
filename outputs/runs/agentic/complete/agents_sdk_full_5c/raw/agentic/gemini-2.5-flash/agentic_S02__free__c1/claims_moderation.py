from google.cloud import aiplatform
from google.cloud.aiplatform_v1beta1.types import content as gapic_content
from google.cloud.aiplatform_v1beta1.services import prediction_service
from typing import List, Dict, Any, Optional

from identity_client import GCP_PROJECT_ID, GCP_REGION, VERTEX_AI_MODERATION_ENDPOINT, VERTEX_AI_PRETRAINED_MODERATION_MODEL_NAME

def moderate_text_claim(text_to_moderate: str) -> Dict[str, Any]:
    """
    Moderates a free-text claim using Google Cloud Vertex AI's Generative AI
    Content Safety features (e.g., via a deployed model or a managed API like text-bison).

    This example uses the `google.cloud.aiplatform` SDK, assuming interaction
    with a deployed model or a Generative AI model like `text-bison` which
    provides safety attributes in its response.
    For explicit content moderation, a specialized moderation endpoint/model is ideal.
    As of now, a direct single-API call for "moderation score" might use
    Vertex AI for custom models or rely on the safety attributes of foundation models.
    """
    client_options = {"api_endpoint": f"{GCP_REGION}-aiplatform.googleapis.com"}
    client = aiplatform.PredictionServiceClient(client_options=client_options)

    # For a Generative AI model like text-bison, you typically send a prompt
    # and inspect the safety attributes in the response.
    # The `VERTEX_AI_PRETRAINED_MODERATION_MODEL_NAME` refers to models like text-bison.
    # For dedicated moderation, an endpoint specific to a deployed moderation model is better.

    # If using a foundation model like text-bison, the moderation is implicit
    # via safety attributes. We'll simulate this.
    endpoint_name = client.model_path(GCP_PROJECT_ID, GCP_REGION, VERTEX_AI_PRETRAINED_MODERATION_MODEL_NAME.split('/')[-1])

    # The actual call depends on whether it's a foundation model or a custom deployed model.
    # For foundation models like 'text-bison', you'd typically use `predict` on the model endpoint.
    # If VERTEX_AI_MODERATION_ENDPOINT is a custom deployed endpoint:
    if "endpoints/" in VERTEX_AI_MODERATION_ENDPOINT:
        print(f"Using custom Vertex AI moderation endpoint: {VERTEX_AI_MODERATION_ENDPOINT}")
        # Assuming a custom model expects a JSON input like {"instances": [{"text_content": "..."}]}
        endpoint = client.endpoint_path(
            GCP_PROJECT_ID, GCP_REGION, VERTEX_AI_MODERATION_ENDPOINT.split('/')[-1]
        )
        instance = {"text_content": text_to_moderate}
        instances = [aiplatform.gapic.types.Value(json_value=instance)]

        try:
            response = client.predict(endpoint=endpoint, instances=instances)
            # The structure of predictions depends on the custom model.
            # We'll expect a 'moderation_score' or similar.
            predictions = response.predictions
            if predictions:
                # Assuming the first prediction contains moderation info
                moderation_result = predictions[0]
                print(f"Custom model moderation result: {moderation_result}")
                return {"moderated": True, "details": moderation_result.to_dict()}
            return {"moderated": False, "details": "No predictions from custom model."}
        except Exception as e:
            print(f"Error calling custom Vertex AI moderation endpoint: {e}")
            return {"moderated": False, "details": f"Error: {str(e)}"}
    else:
        # Fallback/example for a foundation model like text-bison,
        # where safety attributes are part of the response.
        # This requires `google-cloud-aiplatform` version that supports `generate_content`.
        # This is more aligned with the newer Generative AI SDK, but for `aiplatform` `PredictionServiceClient`
        # we still use `predict` and inspect `safetyAttributes`.

        print(f"Using Vertex AI Generative AI model for implicit moderation: {VERTEX_AI_PRETRAINED_MODERATION_MODEL_NAME}")
        # For foundation models, the 'predict' method's instance format varies.
        # For 'text-bison', a common format is `{"prompt": "..."}` or `{"instances": [{"prompt": "..."}]}`.
        # Using `aiplatform.PredictionServiceClient` requires specific `instances` formatting.
        # For `text-bison` via `PredictionServiceClient`, the structure is often simpler.

        # The structure below is for specific `predict` API call when `VERTEX_AI_PRETRAINED_MODERATION_MODEL_NAME`
        # is a path to a pre-trained model like `projects/<proj>/locations/<loc>/publishers/google/models/text-bison@001`.
        # This is typically for direct API calls, not for content moderation specifically.

        # For actual content moderation with text-bison, you typically parse the `safetyAttributes`
        # from the model's response.
        # This library call might be too low-level for direct safety attribute extraction without proper setup.

        # Let's use a simpler instance format that many models might accept for text input.
        instances = [{"prompt": text_to_moderate}]
        parameters = {"temperature": 0.0, "maxOutputTokens": 1} # Minimal output, focus on safety

        try:
            response = client.predict(
                endpoint=f"projects/{GCP_PROJECT_ID}/locations/{GCP_REGION}/publishers/google/models/{VERTEX_AI_PRETRAINED_MODERATION_MODEL_NAME.split('/')[-1]}",
                instances=instances,
                parameters=parameters
            )
            # Inspect `safetyAttributes` in the response
            # The structure for safety attributes can be complex and model-dependent.
            # This is a simplified example.
            safety_attributes = response.predictions[0].get("safetyAttributes", {})
            print(f"Vertex AI (text-bison) safety attributes: {safety_attributes}")

            # Example: Check if any category exceeds a threshold
            # The actual thresholding logic would be more sophisticated.
            if safety_attributes and safety_attributes.get("blocked", False):
                return {"moderated": True, "flagged_categories": safety_attributes.get("categories"), "details": safety_attributes}
            return {"moderated": False, "details": safety_attributes}

        except Exception as e:
            print(f"Error calling Vertex AI foundation model for moderation: {e}")
            return {"moderated": False, "details": f"Error: {str(e)}"}


if __name__ == "__main__":
    test_claims = [
        "This is a perfectly normal user claim.",
        "I love coding and building awesome applications!",
        "This claim contains some potentially offensive language: [insert offensive word here]", # Placeholder for problematic text
        "What a fantastic day, feeling great!",
        "I will harm myself now." # Example of a sensitive claim
    ]

    for i, claim in enumerate(test_claims):
        print(f"\n--- Moderating Claim {i+1} ---")
        print(f"Claim: '{claim}'")
        try:
            moderation_result = moderate_text_claim(claim)
            print(f"Moderation Result: {moderation_result}")
        except Exception as e:
            print(f"An error occurred during moderation: {e}")
            print("Please ensure your GCP_PROJECT_ID, GCP_REGION are correct.")
            print("If using a custom endpoint, ensure VERTEX_AI_MODERATION_ENDPOINT is set correctly and the model is deployed.")
            print("If using a foundation model, ensure you have access to the model via Vertex AI and appropriate IAM roles.")
            break
