import google.cloud.aiplatform as aiplatform

def get_model_output_with_metadata(project_id: str, location: str, prompt: str):
    """
    Returns model output together with provider platform metadata such as usage, resource IDs, or model handles.
    """
    aiplatform.init(project=project_id, location=location)

    # Use a concrete model ID for identification
    model = aiplatform.TextGenerationModel.from_pretrained("gemini-pro")

    # Predict with the model
    response = model.predict(prompt)

    # Extract output and metadata
    model_output = response.text
    metadata = {
        "model_name": "gemini-pro",
        "project_id": project_id,
        "location": location,
        # 'usage_metadata' might be available depending on the response structure
        # and API version. For demonstration, we'll assume it's directly accessible
        # or can be constructed from the response object if available.
        # As per the current `google-cloud-aiplatform` SDK structure for predict,
        # usage metadata like token counts are typically within response.usage_metadata.
        # If not directly present in the `response` object for `predict` in this manner,
        # it might require parsing the raw API response or checking other attributes.
        # For this example, we'll simulate its inclusion.
        "usage_metadata": getattr(response, 'usage_metadata', "Not directly available in this simplified response attribute for gemini-pro predict."),
        "candidates_count": len(response.candidates),
        "safety_attributes": response.candidates[0].safety_attributes if response.candidates else "No candidates",
    }
    
    # A more robust way to get usage metadata, if available, would involve
    # inspecting the full response object or specific SDK features for it.
    # For many models, token count metadata is typically found in response.metadata
    # or a similar attribute if the model's prediction API returns it.
    # Example for token count (conceptual, exact path may vary by SDK version):
    # if hasattr(response, 'metadata') and 'token_count' in response.metadata:
    #     metadata['token_count'] = response.metadata['token_count']

    return model_output, metadata

