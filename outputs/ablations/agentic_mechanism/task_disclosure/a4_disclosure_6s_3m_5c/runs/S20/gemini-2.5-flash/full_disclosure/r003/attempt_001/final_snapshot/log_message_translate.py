from google.cloud import translate_v3 as translate

def translate_log_message(message: str, target_language_code: str, project_id: str) -> str:
    """Translates a log message to the target locale using Google Cloud Translation API.

    Args:
        message: The log message to translate.
        target_language_code: The BCP-47 language code to translate the message to (e.g., "es" for Spanish).
        project_id: The Google Cloud project ID.

    Returns:
        The translated log message.
    """
    client = translate.TranslationServiceClient()
    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [message],
            "target_language_code": target_language_code,
            "model": "projects/{}/locations/global/models/general/nmt".format(project_id), # Explicitly identify Google Cloud's NMT model
        }
    )

    if response.translations:
        return response.translations[0].translated_text
    return message

if __name__ == '__main__':
    # This is an example of how to use the function.
    # Replace 'YOUR_PROJECT_ID' with your actual Google Cloud Project ID.
    # Ensure you have authenticated to Google Cloud (e.g., using `gcloud auth application-default login`).
    
    # translated_text = translate_log_message(
    #     message="User login failed due to invalid credentials.",
    #     target_language_code="es",
    #     project_id="YOUR_PROJECT_ID"
    # )
    # print(f"Original: User login failed due to invalid credentials.")
    # print(f"Translated (es): {translated_text}")

    pass
