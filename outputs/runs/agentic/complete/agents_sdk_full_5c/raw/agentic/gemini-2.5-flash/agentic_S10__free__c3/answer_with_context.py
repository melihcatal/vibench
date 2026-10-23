from vertexai.preview.language_models import TextGenerationModel

def answer_with_context(project_id: str, location: str, question: str, context: str) -> str:
    """Answers a question using provided context with a Google Cloud Vertex AI PaLM model."""
    model = TextGenerationModel.from_pretrained("text-bison@002")
    prompt = f"""Answer the following question based *only* on the provided context.

Context: """{context}"""

Question: """{question}"""

Answer:
"""
    response = model.predict(
        prompt=prompt,
        temperature=0.1,
        max_output_tokens=512,
    )
    return response.text

