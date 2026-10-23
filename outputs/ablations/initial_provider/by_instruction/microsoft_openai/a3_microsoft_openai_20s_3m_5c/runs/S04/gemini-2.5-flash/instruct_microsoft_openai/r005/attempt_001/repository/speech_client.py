import os
import requests

class SpeechClient:
    """
    Provides client utilities for interacting with the Azure Speech-to-Text API.
    """
    def __init__(self, speech_key: str = None, service_region: str = None):
        self.speech_key = speech_key or os.environ.get("SPEECH_KEY")
        self.service_region = service_region or os.environ.get("SPEECH_REGION")

        if not self.speech_key or not self.service_region:
            raise ValueError("SPEECH_KEY and SPEECH_REGION environment variables or explicit arguments must be set.")

        self.base_url = f"https://{self.service_region}.api.cognitive.microsoft.com/speechtotext/v3.0"

    def get_headers(self, content_type: str = "application/json") -> dict:
        """
        Returns standard headers required for Azure Speech-to-Text API requests.
        """
        return {
            "Ocp-Apim-Subscription-Key": self.speech_key,
            "Content-Type": content_type
        }

    def get_base_url(self) -> str:
        """
        Returns the base URL for the Azure Speech-to-Text API.
        """
        return self.base_url

    def create_session(self) -> requests.Session:
        """
        Creates and returns a requests.Session object configured with base headers.
        """
        session = requests.Session()
        session.headers.update({"Ocp-Apim-Subscription-Key": self.speech_key})
        return session

# Example usage (for demonstration, not executed directly)
if __name__ == "__main__":
    # os.environ["SPEECH_KEY"] = "YOUR_AZURE_SPEECH_SERVICE_KEY"
    # os.environ["SPEECH_REGION"] = "YOUR_AZURE_SPEECH_SERVICE_REGION"

    try:
        client = SpeechClient()
        print(f"SpeechClient initialized. Base URL: {client.get_base_url()}")
        headers = client.get_headers()
        # print(f"Headers: {headers}") # Don't print key to console
        print("Headers generated successfully (key omitted for security).")
        
        # Example of using a session
        with client.create_session() as session:
            print("Requests session created.")
            # response = session.get(f"{client.get_base_url()}/transcriptions")
            # print(f"Session get response status: {response.status_code}")

    except ValueError as e:
        print(f"Error initializing SpeechClient: {e}")
    print("To run this example, set SPEECH_KEY, SPEECH_REGION environment variables.")
