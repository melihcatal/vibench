import vertexai
from vertexai.preview.language_models import TextGenerationModel
import os

def answer_with_context(question: str, context: str) -> str:
    """Answers a question using provided context with a hosted LLM."""
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")
    
    vertexai.init(project=project_id, location=location)
    model = TextGenerationModel.from_pretrained("text-bison@001")
    
    prompt = f"""Given the following context, answer the question.
If the answer is not in the context, say "I don't know."

Context:
{context}

Question: {question}

Answer:
"""
    
    response = model.predict(
        prompt,
        max_output_tokens=256,
        temperature=0.1,
        top_p=0.8,
        top_k=40
    )
    return response.text
