import os
from ibm_watsonx_ai import APIClient
from ibm_watsonx_ai.hai.llm import StreamingTextGenerationSession


def stream_completion(prompt: str, max_tokens: int = 256) -> str:
    """Stream partial output tokens from watsonx.ai hosted LLM.

    Provider: IBM watsonx.ai
    """
    api_key = os.getenv("WATSONX_API_KEY", "<INSERT_WATSONX_API_KEY>")
    project_id = os.getenv("WATSONX_PROJECT_ID", "<INSERT_WATSONX_PROJECT_ID>")
    client = APIClient(
        api_key=api_key,
        project_id=project_id,
        url="https://api.watsonx.ai",
    )
    session = StreamingTextGenerationSession(
        model_id="ibm/granite-20m-uncased",
        api_client=client,
    )
    # Iterate over streamed tokens and accumulate.
    output = []
    for token in session.stream_generate(
        system_prompt="You will complete the given prompt.",
        user_input=prompt,
        max_new_tokens=max_tokens,
    ):
        output.append(token.text)
    return "".join(output)
