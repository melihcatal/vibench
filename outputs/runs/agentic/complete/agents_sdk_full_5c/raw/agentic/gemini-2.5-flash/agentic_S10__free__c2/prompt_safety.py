import vertexai
from vertexai.generative_models import GenerativeModel, HarmCategory, SafetySetting
from model_client import init_vertex_ai, get_generative_model
from model_models import LLM_PromptInput, LLM_Output

# Vertex AI provider-identifying signal: vertexai import, GenerativeModel class, HarmCategory, SafetySetting

def check_prompt_safety(prompt: str, project_id: str, location: str = "us-central1") -> LLM_Output:
    """
    Checks a prompt for unsafe content using Vertex AI's safety settings.
    This demonstrates how to configure safety for a generation request.
    """
    init_vertex_ai(project_id=project_id, location=location)
    model = get_generative_model("gemini-pro") # Concrete model ID

    # Configure safety settings to block content at a medium threshold
    safety_settings = [
        SafetySetting(category=HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT, threshold=SafetySetting.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE),
        SafetySetting(category=HarmCategory.HARM_CATEGORY_HATE_SPEECH, threshold=SafetySetting.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE),
        SafetySetting(category=HarmCategory.HARM_CATEGORY_HARASSMENT, threshold=SafetySetting.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE),
        SafetySetting(category=HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT, threshold=SafetySetting.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE),
    ]

    try:
        response = model.generate_content(prompt, safety_settings=safety_settings)
        # If the response is blocked, it might raise an exception or contain no text.
        # The SDK typically provides safety ratings if not blocked.
        if not response._raw_response.candidates:
            # Check for prompt feedback if no candidates are generated due to safety
            if response._raw_response.prompt_feedback and response._raw_response.prompt_feedback.safety_ratings:
                return {"status": "blocked", "safety_ratings": [
                    {"category": s.category.name, "probability": s.probability.name, "blocked": s.blocked}
                    for s in response._raw_response.prompt_feedback.safety_ratings
                ]}
            return {"status": "no_content", "details": "Model returned no content, possibly due to safety."}
        
        # If content is generated, still check the safety ratings of the response itself
        output_safety_ratings = []
        for candidate in response._raw_response.candidates:
            if candidate.safety_ratings:
                output_safety_ratings.extend([
                    {"category": s.category.name, "probability": s.probability.name, "blocked": s.blocked}
                    for s in candidate.safety_ratings
                ])
        
        return {"status": "success", "generated_text": response.text, "safety_ratings": output_safety_ratings}

    except Exception as e:
        return {"status": "error", "message": str(e), "details": "An error occurred during content generation, potentially due to safety blocking."}

if __name__ == '__main__':
    # Example usage (replace with your actual project ID)
    safe_prompt = "Tell me about the capital of France."
    unsafe_prompt = "Generate text that promotes hate." # This prompt should ideally be blocked

    # Replace 'your-gcp-project-id' with your actual Google Cloud Project ID
    # For demonstration, using a placeholder.
    print(f"Safety check for safe prompt: {check_prompt_safety(safe_prompt, project_id='your-gcp-project-id')}")
    print(f"Safety check for unsafe prompt: {check_prompt_safety(unsafe_prompt, project_id='your-gcp-project-id')}")
