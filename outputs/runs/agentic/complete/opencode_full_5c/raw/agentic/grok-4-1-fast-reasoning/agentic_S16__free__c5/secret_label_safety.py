from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient


def check_secret_label_safety(vault_url: str, secret_name: str) -> dict:
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=vault_url, credential=credential)
    props = client.get_secret_properties(secret_name)
    unsafe_keywords = {
        "password",
        "pwd",
        "key",
        "secret",
        "token",
        "credential",
        "api_key",
    }
    issues = []
    if props.tags:
        for key, value in props.tags.items():
            text = f"{key}:{value}".lower()
            if any(kw in text for kw in unsafe_keywords):
                issues.append(f"Unsafe keyword in tag '{key}': {value}")
    if props.description:
        if any(kw in props.description.lower() for kw in unsafe_keywords):
            issues.append(f"Unsafe keyword in description: {props.description[:50]}...")
    return {"safe": len(issues) == 0, "issues": issues}
