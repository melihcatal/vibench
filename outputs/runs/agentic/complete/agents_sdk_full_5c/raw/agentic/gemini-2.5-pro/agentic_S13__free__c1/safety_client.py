import os
from dotenv import load_dotenv

load_dotenv()

# Centralized configuration for various safety service clients
class SafetyClients:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    COHERE_API_KEY = os.getenv("COHERE_API_KEY")
    PERSPECTIVE_API_KEY = os.getenv("GOOGLE_API_KEY") # Perspective API uses Google API Key
    AZURE_CONTENT_SAFETY_KEY = os.getenv("AZURE_CONTENT_SAFETY_KEY")
    AZURE_CONTENT_SAFETY_ENDPOINT = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    # Google Translate uses service account credentials, often set via GOOGLE_APPLICATION_CREDENTIALS
    ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
    # AWS credentials are typically handled via environment variables like AWS_ACCESS_KEY_ID or IAM roles.
    # No explicit key is needed here if the environment is configured.

# Instantiate for easy import
safety_clients_config = SafetyClients()
