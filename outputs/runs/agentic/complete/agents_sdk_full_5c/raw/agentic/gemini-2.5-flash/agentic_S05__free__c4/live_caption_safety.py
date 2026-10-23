from google.cloud import aiplatform
import os

def check_text_safety_vertex_ai(
    text: str,
    project_id: str,
    location: str = "us-central1",
    model_id: str = "projects/cloud-aiplatform/locations/us-central1/models/text-bison-001", # Using a generative model with safety attributes
) -> dict:
    """
    Checks text for unsafe content using Google Cloud Vertex AI generative models.
    The safety attributes are usually returned as part of the model's response.

    Args:
        text: The text content to check.
        project_id: The Google Cloud project ID.
        location: The Vertex AI endpoint location.
        model_id: The full resource name of the generative model to use.
                  e.g., "projects/cloud-aiplatform/locations/us-central1/models/text-bison-001"

    Returns:
        A dictionary containing safety attributes, or an empty dict if not found.
    """
    aiplatform.init(project=project_id, location=location)
    # The TextGenerationModel is a higher-level SDK for generative models
    # For direct API calls or more control over prediction endpoint, 
    # one might use aiplatform.GapicPredictionServiceClient.
    # However, for safety attributes with text-bison, the SDK is convenient.
    from vertexai.preview.language_models import TextGenerationModel

    model = TextGenerationModel.from_pretrained(model_id.split('/')[-1]) # Extracting model name from path

    # When making a prediction with generative models, safety attributes are part of the response.
    # We're not asking it to generate, but just passing the text to get a response that includes safety.
    response = model.predict(prompt=text, safety_settings={})
    
    # The safety attributes are usually within the `_prediction_response` object 
    # of the model's prediction response.
    # The exact structure can vary, and direct access might require inspecting the object.
    # For `text-bison`, safety attributes are typically associated with each candidate.
    safety_attributes = {}
    if response.candidates and hasattr(response.candidates[0], 'safety_attributes'):
        safety_attributes = response.candidates[0].safety_attributes.to_dict() # Assuming it can be converted to dict
    elif hasattr(response, 'safety_attributes'):
        safety_attributes = response.safety_attributes.to_dict()
    
    return safety_attributes

async def check_live_caption_safety(caption_stream_gen, project_id: str):
    """
    Checks live captions for unsafe content using Google Cloud Vertex AI.

    Args:
        caption_stream_gen: An async generator yielding (transcript, is_final) tuples.
        project_id: Your Google Cloud project ID.

    Yields:
        Tuples of (transcript, is_final, safety_attributes) for each caption.
    """
    async for transcript, is_final in caption_stream_gen:
        if transcript.strip() and is_final: # Only check final, non-empty captions for safety
            safety_attrs = check_text_safety_vertex_ai(
                text=transcript,
                project_id=project_id,
            )
            yield transcript, is_final, safety_attrs
        else:
            yield transcript, is_final, {}

if __name__ == '__main__':
    # Example usage:
    # import asyncio
    #
    # GOOGLE_CLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT", "your-gcp-project-id")
    #
    # async def dummy_caption_source():
    #     yield "This is a normal sentence.", False
    #     await asyncio.sleep(0.5)
    #     yield "I hate this, it's terrible!", True # Example of potentially unsafe content
    #     await asyncio.sleep(0.5)
    #     yield "Let's discuss the project tasks.", True
    #
    # async def main():
    #     print(f"Checking caption safety for project {GOOGLE_CLOUD_PROJECT}...")
    #     async for transcript, is_final, safety_attrs in check_live_caption_safety(
    #         dummy_caption_source(), GOOGLE_CLOUD_PROJECT
    #     ):
    #         if is_final:
    #             print(f"Final Caption: \"{transcript}\" - Safety: {safety_attrs}")
    #         else:
    #             print(f"Partial Caption: \"{transcript}\"")
    #
    # if GOOGLE_CLOUD_PROJECT == "your-gcp-project-id":
    #     print("Please set the GOOGLE_CLOUD_PROJECT environment variable or replace 'your-gcp-project-id'.")
    # else:
    #     asyncio.run(main())
    pass
