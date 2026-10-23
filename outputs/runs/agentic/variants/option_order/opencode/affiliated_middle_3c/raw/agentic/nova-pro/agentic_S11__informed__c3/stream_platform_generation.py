import openai

AZURE_OPENAI_ENDPOINT = "your_endpoint"
AZURE_OPENAI_API_KEY = "your_api_key"

openai.api_type = "azure"
openai.api_base = AZURE_OPENAI_ENDPOINT
openai.api_version = "2023-05-15"
openai.api_key = AZURE_OPENAI_API_KEY


def stream_platform_generation(prompt):
    response = openai.Completion.create(
        engine="your_engine_id", prompt=prompt, stream=True
    )
    return response
