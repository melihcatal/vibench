import vertexai
from vertexai.preview.generative_models import GenerativeModel
from vision_client import initialize_vertexai
from vision_models import ImageAnalysisResult

def summarize_visual_analysis(analysis_result: ImageAnalysisResult, project_id: str, location: str) -> str:
    """Summarizes visual analysis results using Gemini Pro."""
    initialize_vertexai(project_id, location) # e.g., "your-gcp-project-id", "us-central1"
    model = GenerativeModel("gemini-pro")

    prompt = f"""Summarize the following image analysis results concisely:

Labels: {", ".join(analysis_result.labels)}
Description: {analysis_result.description}
Detected Text: {analysis_result.detected_text}
Safety Scores (Adult: {analysis_result.safety_scores.get('adult', 'UNKNOWN')}, Violence: {analysis_result.safety_scores.get('violence', 'UNKNOWN')}):

Provide a brief summary focusing on key findings."""

    response = model.generate_content([prompt])
    return response.text

if __name__ == '__main__':
    # Example usage
    example_result = ImageAnalysisResult(image_id="test_image_123")
    example_result.labels = ["cat", "pet", "animal"]
    example_result.description = "A fluffy cat sitting on a rug."
    example_result.detected_text = "MEOW"
    example_result.safety_scores = {"adult": "VERY_UNLIKELY", "violence": "VERY_UNLIKELY", "racy": "UNLIKELY"}

    # Replace with your actual GCP project ID and region
    project_id = "your-gcp-project-id" 
    location = "us-central1"

    summary = summarize_visual_analysis(example_result, project_id, location)
    print(f"Summary: {summary}")
