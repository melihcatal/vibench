import vertexai
from vertexai.generative_models import GenerativeModel, Part, FinishReason
import vertexai.preview.generative_models as generative_models

def summarize_metric_trends(project_id: str, location: str, metric_data: str) -> str:
    """Summarize recent metric trends or anomalies using Google Cloud Vertex AI.

    Provider: Google Cloud Vertex AI
    """
    vertexai.init(project=project_id, location=location)
    # Provider-identifying signal: GenerativeModel("gemini-pro")
    model = GenerativeModel("gemini-pro")
    
    # Example prompt - in a real scenario, metric_data would be more structured
    prompt = f"Summarize the following metric data and highlight any trends or anomalies: {metric_data}"

    generation_config = {
        "max_output_tokens": 2048,
        "temperature": 0.4,
        "top_p": 1,
        "top_k": 32,
    }

    safety_settings = {
        generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    }

    responses = model.generate_content(
        [prompt],
        generation_config=generation_config,
        safety_settings=safety_settings,
        stream=False,
    )
    
    if responses.candidates and responses.candidates[0].content.parts:
        return responses.candidates[0].content.parts[0].text
    return "No summary could be generated."
