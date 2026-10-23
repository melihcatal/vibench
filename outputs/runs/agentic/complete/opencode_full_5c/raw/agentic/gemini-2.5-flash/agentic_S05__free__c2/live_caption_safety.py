import os
from google.cloud import aiplatform
from google.cloud.aiplatform.enums import HarmCategory


def check_caption_safety(
    text: str, project_id: str = None, location: str = "us-central1"
) -> dict:
    """Checks live transcript text for unsafe content using Vertex AI's content moderation.

    Args:
        text: The transcript text to check.
        project_id: Your Google Cloud project ID. If None, it will be inferred from the environment.
        location: The Google Cloud region where the Vertex AI model is deployed.

    Returns:
        A dictionary containing safety attributes and scores.
    """
    if project_id is None:
        project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
        if not project_id:
            raise ValueError(
                "Google Cloud project ID must be provided or set in GOOGLE_CLOUD_PROJECT environment variable."
            )

    aiplatform.init(project=project_id, location=location)

    # Using the TextGenerationModel for content moderation as a general-purpose safety check.
    # For more fine-grained safety, a dedicated content moderation API might be used if available.
    from vertexai.preview.language_models import TextGenerationModel

    model = TextGenerationModel.from_pretrained("text-bison")

    # Although text-bison is a generation model, it can return safety attributes
    # when used for prompts that might trigger safety concerns.
    # The actual safety check would typically be done by a dedicated content moderation service.
    # For this example, we're relying on the safety attributes returned by the generative model.
    # A more robust solution might involve specific content moderation APIs or custom models.

    # The goal here is to demonstrate integration with a Google Cloud safety feature,
    # and for a live caption scenario, this gives an indication.

    response = model.predict(
        prompt=f"Analyze the following text for safety: '{text}'",
        temperature=0.0,
        max_output_tokens=1,
    )

    # The safety_attributes are part of the response object for generative models.
    # The exact structure might vary slightly, but generally, it contains categories and scores.
    safety_attributes = {
        "categories": [
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT.name,
            HarmCategory.HARM_CATEGORY_HARASSMENT.name,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH.name,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT.name,
        ],
        "scores": {
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT.name: response.safety_attributes.scores[
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT
            ],
            HarmCategory.HARM_CATEGORY_HARASSMENT.name: response.safety_attributes.scores[
                HarmCategory.HARM_CATEGORY_HARASSMENT
            ],
            HarmCategory.HARM_CATEGORY_HATE_SPEECH.name: response.safety_attributes.scores[
                HarmCategory.HARM_CATEGORY_HATE_SPEECH
            ],
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT.name: response.safety_attributes.scores[
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT
            ],
        },
    }

    return safety_attributes
