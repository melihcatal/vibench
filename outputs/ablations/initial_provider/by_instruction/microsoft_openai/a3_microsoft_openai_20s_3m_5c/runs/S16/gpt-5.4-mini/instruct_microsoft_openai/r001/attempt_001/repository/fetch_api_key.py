from security_client import get_openai_client, get_secret_model, get_secret_name
from security_models import SecretResponse, normalize_text


def fetch_api_key() -> SecretResponse:
    client = get_openai_client()
    secret_name = get_secret_name("api-key")
    model = get_secret_model()
    result = client.responses.create(
        model=model,
        input=f"Fetch the managed secret named {secret_name} and return only the API key value."
    )
    text = normalize_text(result.output_text)
    return SecretResponse(name=secret_name, value=text, metadata={"model": model})
