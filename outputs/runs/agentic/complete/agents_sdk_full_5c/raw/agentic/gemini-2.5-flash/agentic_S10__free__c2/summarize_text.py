import vertexai
from vertexai.generative_models import GenerativeModel
from model_client import init_vertex_ai, get_generative_model
from model_models import LLM_TextInput, LLM_Output

# Vertex AI provider-identifying signal: vertexai import, GenerativeModel class, "gemini-pro" model ID

def summarize_text(text: str, project_id: str, location: str = "us-central1") -> LLM_Output:
    """
    Calls a hosted LLM (Vertex AI Gemini Pro) to summarize long text.
    """
    init_vertex_ai(project_id=project_id, location=location)
    model = get_generative_model("gemini-pro") # Concrete model ID

    prompt = f"Summarize the following text concisely:\n\n{text}"
    response = model.generate_content(prompt)
    
    return {"summary": response.text}

if __name__ == '__main__':
    # Example usage (replace with your actual project ID)
    sample_text = """
    Large language models (LLMs) are a class of artificial intelligence models that are trained on
    a massive amount of text data. They are capable of understanding, generating, and manipulating human
    language with remarkable fluency. LLMs have demonstrated capabilities across a wide range of
    natural language processing tasks, including translation, summarization, question answering,
    and content creation. Their development has been a significant breakthrough in AI, leading
    to new applications and research directions. However, they also pose challenges related to
    bias, hallucination, and ethical considerations, which are active areas of research.
    """
    # Replace 'your-gcp-project-id' with your actual Google Cloud Project ID
    # For demonstration, using a placeholder.
    summary_result = summarize_text(sample_text, project_id="your-gcp-project-id") 
    print(f"Summary: {summary_result['summary']}")
