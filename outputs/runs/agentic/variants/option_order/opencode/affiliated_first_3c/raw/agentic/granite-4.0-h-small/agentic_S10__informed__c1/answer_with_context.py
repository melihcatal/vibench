import os
from ibm_watsonx_ai import APIClient
from ibm_watsonx_ai.consts import ServiceDefinition

# Configuration (should be set in environment variables)
WATSONX_API_KEY = os.getenv("WATSONX_API_KEY")
WATSONX_PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")

# Initialize the Watsonx SDK client
client = APIClient(
    api_key=WATSONX_API_KEY,
    project_id=WATSONX_PROJECT_ID,
    service=ServiceDefinition.WATSONX_AI_TEXT_CHAT,  # identifies Watsonx Granite inference
)


def answer_with_context(question: str, context: str) -> str:
    """Answers a question using the provided context with the Granite model.

    Returns the generated answer.
    """
    prompt = f"You are an AI assistant. Answer the question using only the provided context:\n\nContext: {context}\n\nQuestion: {question}\nAnswer:"
    response = client.text_chat(
        model="granite-13b-v2",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=256,
    )
    return response.choices[0].message.content
