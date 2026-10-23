import vertexai
from vertexai.generative_models import GenerativeModel, Part, Content
from model_client import init_vertex_ai, get_generative_model
from model_models import LLM_ContextInput, LLM_TextInput, LLM_Output

# Vertex AI provider-identifying signal: vertexai import, GenerativeModel class, "gemini-pro" model ID

def answer_question_with_context(question: str, context: str, project_id: str, location: str = "us-central1") -> LLM_Output:
    """
    Calls a hosted LLM (Vertex AI Gemini Pro) to answer a question using provided context.
    """
    init_vertex_ai(project_id=project_id, location=location)
    model = get_generative_model("gemini-pro") # Concrete model ID

    # Using multi-turn or structured prompt for context
    prompt_parts = [
        Part.from_text(f"Context: {context}\n\nQuestion: {question}\n\nAnswer:"),
    ]

    response = model.generate_content(prompt_parts)
    
    return {"answer": response.text}

if __name__ == '__main__':
    # Example usage (replace with your actual project ID)
    sample_context = """
    The Golden Gate Bridge is a suspension bridge spanning the Golden Gate, the one-mile-wide
    (1.6 km) strait connecting San Francisco Bay to the Pacific Ocean. The bridge is one of the
    most internationally recognized symbols of San Francisco, California, and the United States.
    It was declared one of the modern Wonders of the World by the American Society of Civil Engineers.
    Construction began on January 5, 1933, and it was completed in 1937. The chief engineer was Joseph Strauss.
    """
    sample_question = "Who was the chief engineer of the Golden Gate Bridge?"
    
    # Replace 'your-gcp-project-id' with your actual Google Cloud Project ID
    # For demonstration, using a placeholder.
    answer_result = answer_question_with_context(sample_question, sample_context, project_id="your-gcp-project-id")
    print(f"Answer: {answer_result['answer']}")
