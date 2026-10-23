import os
from ibm_watsonx_ai import APIClient
from ibm_watsonx_ai.hai.llm import TextGenerationSession


def answer_with_context(question: str, context: str) -> str:
    """Answer a question using provided context with watsonx.ai hosted LLM.

    Provider: IBM watsonx.ai
    """
    api_key = os.getenv("WATSONX_API_KEY", "<INSERT_WATSONX_API_KEY>")
    project_id = os.getenv("WATSONX_PROJECT_ID", "<INSERT_WATSONX_PROJECT_ID>")
    client = APIClient(
        api_key=api_key,
        project_id=project_id,
        url="https://api.watsonx.ai",
    )
    session = TextGenerationSession(
        model_id="ibm/granite-20m-uncased",
        api_client=client,
    )
    system_prompt = "You are a helpful assistant. Answer the question based only on the provided context."
    prompt = f"{system_prompt}\n\nQuestion: {question}\nContext:\n{context}"
    response = session.generate(
        system_prompt=system_prompt, user_input=prompt, max_new_tokens=256
    )
    return response[0].get("text", "")
