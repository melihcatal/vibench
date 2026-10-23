import vertexai
from vertexai.generative_models import GenerativeModel
import json
from model_client import init_vertex_ai, get_generative_model
from model_models import LLM_TextInput, LLM_Output

# Vertex AI provider-identifying signal: vertexai import, GenerativeModel class, "gemini-pro" model ID

def extract_json_from_text(text: str, project_id: str, location: str = "us-central1") -> LLM_Output:
    """
    Calls a hosted LLM (Vertex AI Gemini Pro) to extract structured JSON from text.
    """
    init_vertex_ai(project_id=project_id, location=location)
    model = get_generative_model("gemini-pro") # Concrete model ID

    prompt = f"""
    Extract key information from the following text into a JSON object.
    The JSON should contain 'title', 'author', and 'keywords' (as a list of strings).
    If a field is not found, use null.

    Text:
    """
    {text}
    """

    JSON:
    """
    response = model.generate_content(prompt)
    
    try:
        # Assuming the model reliably outputs valid JSON
        extracted_data = json.loads(response.text)
        return {"extracted_json": extracted_data}
    except json.JSONDecodeError:
        return {"error": "Failed to decode JSON from model output", "raw_output": response.text}

if __name__ == '__main__':
    # Example usage (replace with your actual project ID)
    sample_text = """
    The groundbreaking article "The Future of AI" was published last month by Dr. Anya Sharma.
    It discusses advancements in machine learning, neural networks, and ethical AI development.
    Keywords include artificial intelligence, machine learning, ethics, future tech.
    """
    # Replace 'your-gcp-project-id' with your actual Google Cloud Project ID
    # For demonstration, using a placeholder.
    json_result = extract_json_from_text(sample_text, project_id="your-gcp-project-id")
    print(f"Extracted JSON: {json_result}")
