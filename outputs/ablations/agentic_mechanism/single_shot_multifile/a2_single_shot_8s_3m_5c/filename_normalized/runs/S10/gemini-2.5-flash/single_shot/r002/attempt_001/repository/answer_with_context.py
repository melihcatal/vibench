import os
import vertexai
from vertexai.generative_models import GenerativeModel
from model_client import get_gemini_model

def answer_with_context(question: str, context: str) -> str:
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")
    
    model = get_gemini_model(project_id, location, "gemini-pro")
    
    prompt = f"Using only the following context, answer the question. If the answer is not in the context, state that you cannot answer.

Context: {context}

Question: {question}

Answer:"
    
    response = model.generate_content(
        contents=prompt,
        generation_config={
            "max_output_tokens": 200,
            "temperature": 0.2,
            "top_p": 0.9,
        }
    )
    
    return response.text
