from google.cloud.aiplatform_v1.types import PredictResponse
from model_models import ModelOutput


def check_vertex_ai_safety(model_output: ModelOutput) -> dict:
    # Vertex AI's text generation models often include safety attributes directly in the response.
    # This example assumes the safety attributes are available in the metadata of ModelOutput.
    # In a real scenario, you would parse the actual structure of the safety attributes
    # from the Vertex AI model response.

    safety_attributes = model_output.metadata.get("safety_attributes", {})

    # Example structure of safety_attributes (this might vary based on model and API version)
    # {
    #     "categories": ["HARM_CATEGORY_DANGEROUS_CONTENT", "HARM_CATEGORY_TOXICITY"],
    #     "scores": [0.9, 0.7],
    #     "blocked": False
    # }

    # For demonstration, we'll just return the raw safety attributes if they exist.
    # In a production system, you'd apply thresholds and specific logic to determine
    # if the content is "unsafe".

    return safety_attributes
