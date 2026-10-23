from google.cloud import aiplatform
import os

def summarize_transcription_results(project_id: str, region: str, transcript_text: str, model_name: str = "text-bison@002"):
    """
    Summarizes transcription results using a Google Cloud Vertex AI generative model.

    Args:
        project_id: Your Google Cloud project ID.
        region: The Google Cloud region where your Vertex AI model is deployed (e.g., "us-central1").
        transcript_text: The full text of the transcript to summarize.
        model_name: The name of the generative model to use (e.g., "text-bison@002").

    Returns:
        The summarized text.
    """
    aiplatform.init(project=project_id, location=region)
    # Using a predefined model for text generation
    model = aiplatform.language_models.TextGenerationModel.from_pretrained(model_name)

    prompt = f"Summarize the following meeting transcript:

{transcript_text}\n\nSummary:"

    # Adjust parameters for summarization as needed
    response = model.predict(
        prompt,
        temperature=0.2,
        max_output_tokens=256,
        top_p=0.8,
        top_k=40,
    )

    summary = response.text
    print(f"Transcript summarized using Vertex AI model: {model_name}.")
    return summary
