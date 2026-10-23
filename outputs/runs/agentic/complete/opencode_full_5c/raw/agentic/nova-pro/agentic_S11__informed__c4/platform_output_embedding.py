import openai

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


def embed_platform_output(output: str) -> Dict[str, Any]:
    openai.api_key = OPENAI_API_KEY
    response = openai.Embedding.create(input=output, model="text-embedding-ada-002")
    return response
