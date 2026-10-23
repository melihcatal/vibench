from security_models import SecretLabelCheckResult


def check_secret_labels(secret_name: str) -> SecretLabelCheckResult:
    """Checks secret labels and notes for unsafe or disallowed text.

    Args:
        secret_name: Name of the secret to validate.

    Returns:
        A SecretLabelCheckResult indicating whether the labels are safe.
    """
    # Placeholder implementation - real logic would inspect metadata/labels
    # Assume labels are stored in secret metadata JSON
    client = SecretsManagerClient()
    metadata = client.get_secret_metadata(name=secret_name)
    labels = metadata.get("labels", [])
    unsafe = any("unsafe" in label.lower() for label in labels)
    return SecretLabelCheckResult(
        secret_name=secret_name, safe=not unsafe, unsafe_labels=labels if unsafe else []
    )


if __name__ == "__main__":
    result = check_secret_labels(os.getenv("LABEL_SECRET_NAME"))
    print(f"Label safety check: {result}")
