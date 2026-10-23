from security_client import get_openai_client, get_secret_model, get_secret_name, get_secret_stage, get_secret_version
from security_models import SecretResponse, normalize_text


def rotate_secret_version() -> SecretResponse:
    client = get_openai_client()
    secret_name = get_secret_name("rotating-secret")
    version = get_secret_version()
    stage = get_secret_stage()
    model = get_secret_model()
    result = client.responses.create(
        model=model,
        input=f"Read the secret {secret_name} at version {version} or stage {stage} and return the active value."
    )
    return SecretResponse(name=secret_name, value=normalize_text(result.output_text), metadata={"model": model, "version": version, "stage": stage})
