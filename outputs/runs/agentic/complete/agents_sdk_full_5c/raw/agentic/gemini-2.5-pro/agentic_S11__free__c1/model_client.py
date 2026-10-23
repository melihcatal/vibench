import os
from dotenv import load_dotenv

# Load environment variables from a .env file for local development
load_dotenv()

# Centralized API key management for various services
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")  # For Perspective API
DEEPL_API_KEY = os.getenv("DEEPL_API_KEY")
VOYAGE_API_KEY = os.getenv("VOYAGE_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID")
GCP_LOCATION = os.getenv("GCP_LOCATION", "us-central1")
