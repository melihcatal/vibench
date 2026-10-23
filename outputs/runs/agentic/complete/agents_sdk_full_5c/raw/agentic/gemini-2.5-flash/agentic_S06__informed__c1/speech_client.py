from google.cloud import texttospeech

def get_text_to_speech_client() -> texttospeech.TextToSpeechClient:
    """Returns an initialized Google Cloud Text-to-Speech client."""
    # The client will automatically pick up credentials from the environment
    # (e.g., GOOGLE_APPLICATION_CREDENTIALS environment variable).
    return texttospeech.TextToSpeechClient()

if __name__ == "__main__":
    try:
        client = get_text_to_speech_client()
        print(f"Google Cloud Text-to-Speech client created: {client}")
        # You can optionally perform a small operation to verify connectivity
        # For example, listing voices requires authentication
        # voices = client.list_voices(language_code="en-US").voices
        # print(f"Successfully listed {len(voices)} voices for en-US.")
    except Exception as e:
        print(f"Error creating Text-to-Speech client: {e}")
        print("Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set.")
