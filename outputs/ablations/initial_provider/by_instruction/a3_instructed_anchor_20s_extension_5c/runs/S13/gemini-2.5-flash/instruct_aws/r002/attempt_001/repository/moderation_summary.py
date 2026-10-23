import os
from google.cloud import aiplatform

def moderation_summary(moderation_decisions: list[dict]) -> str:
    """
    Summarize moderation decisions using Google's Generative AI (Vertex AI).
    """
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    region = os.environ.get("GOOGLE_CLOUD_REGION", "us-central1")

    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable not set.")

    aiplatform.init(project=project_id, location=region)

    # Using a text-bison model for summarization. Adjust model as needed.
    # Ensure the model is deployed in your Vertex AI project.
    model_name = "text-bison"
    try:
        parameters = {
            "temperature": 0.2,
            "max_output_tokens": 256,
            "top_p": 0.95,
            "top_k": 40
        }
        model = aiplatform.get_model_registry().get_model(model_name)
        # For gemini, you might use: model = aiplatform.preview.language_models.ChatModel.from_pretrained("chat-bison")

        prompt_text = "Summarize the following moderation decisions: "
        for decision in moderation_decisions:
            prompt_text += f"Text: {decision.get('text', 'N/A')}, Unsafe: {decision.get('is_unsafe', 'N/A')}, Details: {decision.get('decision_details', 'N/A')}. "
        
        # For text-bison, direct prediction
        response = model.predict(prompt=prompt_text, **parameters)
        summary = response.predictions[0].content

        return summary
    except Exception as e:
        return f"Error generating summary with Google Vertex AI: {e}"
