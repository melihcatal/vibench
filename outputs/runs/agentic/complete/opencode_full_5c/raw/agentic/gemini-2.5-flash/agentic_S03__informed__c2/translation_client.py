from google.cloud import translate_v2 as translate
import os


class TranslationClient:
    """Helper class for Google Cloud Translation API."""

    def __init__(self):
        # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
        if not os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"):
            print(
                "Warning: GOOGLE_APPLICATION_CREDENTIALS environment variable not set."
            )
            print("Please set it to the path of your Google service account key file.")
        self._client = translate.Client()

    def get_client(self) -> translate.Client:
        return self._client


if __name__ == "__main__":
    # Example usage
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path/to/your/google_credentials.json"
    client_helper = TranslationClient()
    client = client_helper.get_client()
    # You can now use the client to translate, e.g., client.translate("text", target_language="es")
    print("Google Cloud Translation client initialized.")
