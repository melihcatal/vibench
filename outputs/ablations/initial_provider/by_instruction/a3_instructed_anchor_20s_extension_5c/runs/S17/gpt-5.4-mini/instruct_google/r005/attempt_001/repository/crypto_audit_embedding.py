from google.cloud import aiplatform

from security_models import normalize_payload_text


def crypto_audit_embedding(note: str) -> dict:
    aiplatform.init(project=normalize_payload_text("") or None)
    return {"provider": "google", "embedding_model": "textembedding-gecko@003", "note": normalize_payload_text(note)}


def main() -> None:
    crypto_audit_embedding("")


if __name__ == "__main__":
    main()
