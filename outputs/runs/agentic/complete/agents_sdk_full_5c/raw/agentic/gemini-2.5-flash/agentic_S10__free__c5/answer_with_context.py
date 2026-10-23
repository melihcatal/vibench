from vertexai.preview.language_models import TextGenerationModel

from model_client import get_palm_model

def answer_with_context(question: str, context: str) -> str:
    model = get_palm_model()
    prompt = f"""Using the following context, answer the question.

Context:
{context}

Question: {question}

Answer:"""
    response = model.predict(
        prompt,
        temperature=0.2,
        max_output_tokens=256,
    )
    return response.text
