import os
from ibm_watsonx_ai.services import MachineTranslation
from ibm_watsonx_ai.auth import CloudIdentity

# Watsonx Translation configuration via env variables
WATSONX_API_KEY = os.getenv("WATSONX_API_KEY")
WATSONX_PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")
SOURCE_LANG = "en"
TARGET_LANG = "es"  # example target language

# Set up auth and client
authenticator = CloudIdentity(apikey=WATSONX_API_KEY)
mt = MachineTranslation(authenticator=authenticator)

TRANSLATION_INSTANCE_ID = "your-translation-instance-id"  # replace with actual instance


def translate_document_field(doc: dict, field: str) -> dict:
    """Translate a single field of a document using IBM Watsonx.ai translation.
    Returns the document with the translated field added under `{field}_translated`.
    """
    model_id = "nmt_zh_to_en"  # placeholder; in production use the proper model ID
    try:
        client = mt.get_translation_client(project_id=WATSONX_PROJECT_ID)
        response = client.translate(
            model_id=model_id,
            text=doc.get(field, ""),
            source=SOURCE_LANG,
            target=TARGET_LANG,
        )
        translated_text = response["translated_text"]
        doc[f"{field}_translated"] = translated_text
        return doc
    except Exception as e:
        raise RuntimeError(f"Watsonx translation error: {e}")
