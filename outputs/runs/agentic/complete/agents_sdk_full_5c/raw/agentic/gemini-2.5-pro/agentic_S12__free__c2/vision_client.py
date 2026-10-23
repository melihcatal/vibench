import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- Provider-specific Configuration ---

# OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# AWS Rekognition
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")

# Azure Vision
AZURE_VISION_ENDPOINT = os.getenv("AZURE_VISION_ENDPOINT")
AZURE_VISION_KEY = os.getenv("AZURE_VISION_KEY")

# Google Cloud Vision (uses Application Default Credentials)
# No explicit client config needed if gcloud CLI is set up

# Anthropic
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# DeepL
DEEPL_AUTH_KEY = os.getenv("DEEPL_AUTH_KEY")

# Perspective API
PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY")

# Backblaze B2
B2_ENDPOINT_URL = os.getenv("B2_ENDPOINT_URL")
B2_ACCESS_KEY_ID = os.getenv("B2_ACCESS_KEY_ID")
B2_SECRET_ACCESS_KEY = os.getenv("B2_SECRET_ACCESS_KEY")
