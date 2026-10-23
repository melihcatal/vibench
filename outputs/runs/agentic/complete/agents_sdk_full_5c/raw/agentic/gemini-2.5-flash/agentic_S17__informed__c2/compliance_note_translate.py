import os
from google.cloud import translate_v3

from security_models import TranslationRequest, TranslationResult

def translate_compliance_note(request: TranslationRequest) -> TranslationResult:
    """Translates encryption or compliance notes for reviewers using Google Cloud Translation."""
    client = translate_v3.TranslationServiceClient()

    # A translation request can have a parent, typically a project ID.
    # For this example, we assume the project ID is available in environment variables.
    project_id = os.environ["GCP_PROJECT_ID"]
    parent = f"projects/{project_id}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [request.text],
            "target_language_code": request.target_language,
            "source_language_code": request.source_language, # Optional, if not provided, it will be detected
            # You can also specify model="nmt" for Neural Machine Translation
        }
    )

    translated_text = response.translations[0].translated_text
    detected_source_language = response.translations[0].detected_language_code

    return TranslationResult(
        translated_text=translated_text,
        detected_source_language=detected_source_language
    )

if __name__ == "__main__":
    # Example usage (requires GOOGLE_APPLICATION_CREDENTIALS, GCP_PROJECT_ID env vars)
    # from dotenv import load_dotenv
    # load_dotenv()
    # 
    # note_req = TranslationRequest(
    #     text="Dieser Bericht muss ins Englische übersetzt werden.",
    #     target_language="en",
    #     source_language="de"
    # )
    # translated_result = translate_compliance_note(note_req)
    # print(f"Original: {note_req.text}")
    # print(f"Translated: {translated_result.translated_text}")
    # print(f"Detected Source Language: {translated_result.detected_source_language}")
    # 
    # note_req_auto_detect = TranslationRequest(
    #     text="El cifrado es esencial para la seguridad de los datos.",
    #     target_language="en"
    # )
    # translated_result_auto = translate_compliance_note(note_req_auto_detect)
    # print(f"\nOriginal: {note_req_auto_detect.text}")
    # print(f"Translated: {translated_result_auto.translated_text}")
    # print(f"Detected Source Language: {translated_result_auto.detected_source_language}")
    pass
