import os

from google.cloud import language_v1


def secret_label_safety(text: str):
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(
        content=text, type_=language_v1.Document.Type.PLAIN_TEXT
    )
    response = client.analyze_syntax(
        request={"document": document, "encoding_type": language_v1.EncodingType.UTF8}
    )
    unsafe = any(
        token.text.content.lower() in {"password", "token", "secret", "private"}
        for token in response.tokens
    )
    return {"unsafe": unsafe, "project": os.environ.get("GCP_PROJECT", "")}
