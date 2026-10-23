from google.cloud import secretmanager

def check_secret_label_safety(project_id: str, secret_id: str, unsafe_keywords: list[str]) -> dict:
    """
    Checks secret labels for unsafe text based on a list of keywords.
    """
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}"
    secret = client.get_secret(request={"name": name})

    unsafe_findings = []
    for key, value in secret.labels.items():
        for keyword in unsafe_keywords:
            if keyword.lower() in key.lower() or keyword.lower() in value.lower():
                unsafe_findings.append({"label_key": key, "label_value": value, "found_keyword": keyword})
                
    return {"secret_id": secret_id, "unsafe_label_findings": unsafe_findings}
