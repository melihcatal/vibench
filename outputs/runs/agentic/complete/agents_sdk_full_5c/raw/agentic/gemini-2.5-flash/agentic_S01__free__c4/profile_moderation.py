import os
from google.cloud import aiplatform

# Google Cloud Project ID and Location for Vertex AI
PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")
LOCATION = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1") # Default to us-central1

# Model ID for content moderation, typically a pre-trained model like text-moderation
# For demonstration, we'll use a generic text model if a specific moderation model ID is not available.
# In a real scenario, you'd use a dedicated content moderation model if available via Vertex AI.
# For simplicity and to satisfy the "concrete provider" requirement with a model ID, we'll
# simulate a call to a text model with moderation intent, acknowledging that a specific
# "content-moderation" model might have a different endpoint/SDK usage.
# If using a specific content moderation model, the `model_id` would be specific, e.g., "content-moderation".
# As Vertex AI offers `text-bison` for general text tasks, and specific moderation models often
# have specific names or approaches (like the Generative AI Safety Filter in newer APIs),
# we'll use `text-bison` and structure the prompt for moderation.
# A more direct moderation API might exist, but for Vertex AI SDK, `predict` is general.
# Let's use `gemini-pro` for text classification/moderation as it's more appropriate than text-bison for this.
MODEL_ID = "gemini-pro" # Or a dedicated content moderation model if available

def moderate_profile_text(profile_text: str) -> dict:
    """
    Moderates profile text using a Vertex AI generative model.
    This function will send the text to a generative model with instructions
    to identify if the content is inappropriate.
    """
    if not PROJECT_ID:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    aiplatform.init(project=PROJECT_ID, location=LOCATION)
    # Using `aiplatform.ImageGenerationModel` or `TextGenerationModel` depends on the actual model type.
    # For text moderation, we typically use TextGenerationModel.
    model = aiplatform.GenerativeModel(MODEL_ID)

    prompt = f"""Review the following user profile text for any inappropriate content, hate speech, or offensive language.
    Respond with "SAFE" if the content is appropriate, otherwise respond with "UNSAFE" and briefly explain why.
    
    Profile Text: """
    {profile_text}
    """
    """

    try:
        response = model.generate_content(prompt)
        # Assuming the model's response can be parsed to determine moderation status.
        # This is a simplification; actual moderation APIs provide scores or categories.
        # The first candidate's text is usually the most relevant.
        moderation_result = response.candidates[0].content.parts[0].text.strip()
        
        # A simple parsing, adjust based on actual model output
        is_safe = "SAFE" in moderation_result.upper()

        return {
            "is_safe": is_safe,
            "raw_moderation_output": moderation_result
        }
    except Exception as e:
        raise RuntimeError(f"Failed to moderate profile text using Vertex AI: {e}")
