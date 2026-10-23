from google.cloud import texttospeech
import os

class TextToSpeechClientHelper:
    """Provides a configured client for Google Cloud Text-to-Speech."""

    _client = None

    @classmethod
    def get_client(cls) -> texttospeech.TextToSpeechClient:
        """
        Returns a singleton instance of the Google Cloud Text-to-Speech client.
        Ensures GOOGLE_APPLICATION_CREDENTIALS environment variable is checked.
        
        Returns:
            A configured google.cloud.texttospeech.TextToSpeechClient instance.
        
        Raises:
            EnvironmentError: If GOOGLE_APPLICATION_CREDENTIALS is not set.
        """
        if cls._client is None:
            if "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ:
                print("WARNING: GOOGLE_APPLICATION_CREDENTIALS environment variable not set.")
                print("Attempting to initialize Google Cloud Text-to-Speech client without explicit credentials path.")
                print("This may rely on default application credentials or fail.")
            
            cls._client = texttospeech.TextToSpeechClient()
        return cls._client

if __name__ == '__main__':
    # Example usage:
    # Set your credentials path (e.g., in your shell or programmatically)
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/credentials.json"
    
    try:
        tts_client = TextToSpeechClientHelper.get_client()
        print("Google Cloud Text-to-Speech client initialized successfully.")
        # You can now use tts_client for operations
        # For example, to list voices:
        # voices = tts_client.list_voices().voices
        # print(f"Found {len(voices)} voices.")
    except Exception as e:
        print(f"Failed to initialize Text-to-Speech client: {e}")
