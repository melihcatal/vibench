from google.cloud import aiplatform
from google.protobuf import struct_pb2

from storage_client import get_aiplatform_text_model_client
from storage_models import StoredAssetSummaryRequest, StoredAssetSummaryResponse

def summarize_stored_asset_content(
    request: StoredAssetSummaryRequest
) -> StoredAssetSummaryResponse:
    """Summarizes content extracted from a stored asset using Google Cloud AI Platform (Vertex AI)."""
    # aiplatform.init ensures project and location are set for Vertex AI operations.
    # These should ideally come from environment variables or a configuration file.
    aiplatform.init(project=request.project_id, location=request.location)

    # Initialize the TextGenerationModel with the specified model_name
    # For models like gemini-pro, direct initialization with model_name is common.
    # If the model is deployed on an endpoint, you would use Endpoint.predict instead.
    model = aiplatform.preview.generative_models.GenerativeModel(request.model_name)

    # Define the prompt for summarization
    prompt = f"Summarize the following text:

{request.text_content}

Summary:"

    # Generate content with the model
    response = model.generate_content(
        prompt,
        generation_config={
            "max_output_tokens": request.max_output_tokens,
            "temperature": request.temperature,
            "top_p": 1
        },
        safety_settings=[]
    )
    
    # Extract the summary from the response
    summary = response.candidates[0].content.parts[0].text

    return StoredAssetSummaryResponse(
        summary=summary,
    )
