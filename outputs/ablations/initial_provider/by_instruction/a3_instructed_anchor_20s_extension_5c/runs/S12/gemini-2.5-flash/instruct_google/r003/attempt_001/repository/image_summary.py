from google.cloud import aiplatform
import os

def summarize_image_analysis(labels: list, description: str, text_detection_results: dict, safety_scores: dict) -> str:
    # Initialize Vertex AI
    project_id = os.environ.get("GCP_PROJECT_ID")
    location = os.environ.get("GCP_LOCATION", "us-central1")

    if not project_id:
        return "Error: GCP_PROJECT_ID environment variable not set."

    aiplatform.init(project=project_id, location=location)

    # Use a pre-trained generative model
    model = aiplatform.GenerativeModel("gemini-pro") # Using gemini-pro for text summarization

    # Construct the prompt
    prompt_parts = [
        "Summarize the following image analysis results in a concise paragraph:",
        "Labels: " + ", ".join([label['description'] for label in labels]),
        "Description: " + description,
        "Detected Text: " + text_detection_results.get('full_text', 'No text detected.'),
        "Safety Scores: " + ", ".join([f"{k}: {v}" for k, v in safety_scores.items()])
    ]
    prompt = "\n".join(prompt_parts)

    # Generate content
    response = model.generate_content(prompt)

    return response.text
