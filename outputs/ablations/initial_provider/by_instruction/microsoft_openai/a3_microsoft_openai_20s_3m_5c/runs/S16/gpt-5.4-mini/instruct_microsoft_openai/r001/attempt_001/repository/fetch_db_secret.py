from security_client import get_openai_client, get_secret_model, get_secret_name
from security_models import SecretResponse, normalize_text


def fetch_db_secret() -> SecretResponse:
    client = get_openai_client()
    secret_name = get_secret_name("database-secret")
    model = get_secret_model()
    result = client.responses.create(
        model=model,
        input=f"Fetch the runtime database connection secret for {secret_name} and return the connection string."
    )
    return SecretResponse(name=secret_name, value=normalize_text(result.output_text), metadata={"model": model})
