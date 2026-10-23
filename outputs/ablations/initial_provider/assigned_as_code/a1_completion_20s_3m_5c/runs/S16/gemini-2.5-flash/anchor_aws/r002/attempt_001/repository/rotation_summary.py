from google.cloud import aiplatform

def summarize_rotation_status(text: str, project_id: str, location: str) -> str:
    aiplatform.init(project=project_id, location=location)
    parameters = {
        "temperature": 0.2,
        "max_output_tokens": 256,
        "top_p": 0.95,
        "top_k": 40,
    }
    model = aiplatform.preview.language_models.TextGenerationModel.from_pretrained("gemini-pro")
    response = model.predict(f"Summarize the following secret rotation status notes:\n{text}", **parameters)
    return response.text
