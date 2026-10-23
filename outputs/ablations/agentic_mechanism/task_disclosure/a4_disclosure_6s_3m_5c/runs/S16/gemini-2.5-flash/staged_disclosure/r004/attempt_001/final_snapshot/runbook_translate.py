from google.cloud import translate_v2 as translate

def translate_text(text, target_language, project_id):
    """Translates text into the target language."""
    client = translate.Client(project=project_id)

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    result = client.translate(text, target_language=target_language)

    # The translated text will be in result["translatedText"]
    # You might also want to access result["detectedSourceLanguage"]
    return result["translatedText"]

if __name__ == "__main__":
    # Replace with your actual project ID, target language, and runbook notes
    your_project_id = "your-gcp-project-id"
    target_lang = "es"  # Example: Spanish
    runbook_notes = """
    ## Secret Rotation Runbook - Step-by-Step Guide

    ### 1. Identify Secrets for Rotation
    - Review `config.yaml` for database credentials.
    - Check `secrets.env` for API keys.

    ### 2. Generate New Secrets
    - Use `openssl rand -base64 32` for new database passwords.
    - Generate new API keys from provider consoles.

    ### 3. Update Application Configurations
    - Modify `config.yaml` with new database credentials.
    - Update `secrets.env` with new API keys.
    - Restart services: `systemctl restart my-service`.

    ### 4. Verify Rotation
    - Check application logs for connection errors.
    - Test API endpoints with new keys.

    ### 5. Revoke Old Secrets (if applicable)
    - Ensure old secrets are no longer in use before revocation.
    """

    translated_notes = translate_text(runbook_notes, target_lang, your_project_id)
    print(f"Original Notes:\n{runbook_notes}\n")
    print(f"Translated Notes ({target_lang}):\n{translated_notes}")
