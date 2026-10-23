import vertexai
from vertexai.preview.language_models import TextGenerationModel

def answer_question_with_context(question: str, context: str) -> str:
    vertexai.init(project="YOUR_PROJECT_ID", location="us-central1")
    model = TextGenerationModel.from_pretrained("text-bison@001")

    prompt = f"""
    Context: {context}

    Question: {question}

    Answer:
    """

    response = model.predict(prompt=prompt, temperature=0.2, max_output_tokens=1024)
    return response.text
