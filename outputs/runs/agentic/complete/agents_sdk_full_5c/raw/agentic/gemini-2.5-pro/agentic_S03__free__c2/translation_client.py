import os

# --- Provider-specific configuration ---

# Google Cloud Project ID for Translation and Perspective APIs
GOOGLE_PROJECT_ID = os.getenv("GOOGLE_PROJECT_ID")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY") # For Perspective API

# DeepL API configuration
DEEPL_API_KEY = os.getenv("DEEPL_API_KEY")
DEEPL_API_URL = "https://api-free.deepl.com/v2/translate"

# Azure Cognitive Services configuration
AZURE_TRANSLATOR_KEY = os.getenv("AZURE_TRANSLATOR_KEY")
AZURE_TRANSLATOR_REGION = os.getenv("AZURE_TRANSLATOR_REGION")
AZURE_TRANSLATOR_ENDPOINT = os.getenv("AZURE_TRANSLATOR_ENDPOINT")

# Yandex.Cloud configuration
YANDEX_FOLDER_ID = os.getenv("YANDEX_FOLDER_ID")
YANDEX_API_KEY = os.getenv("YANDEX_API_KEY") # Or IAM Token
YANDEX_TRANSLATE_URL = "https://translate.api.cloud.yandex.net/translate/v2/translate"

# Anthropic API Key
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# Cohere API Key
COHERE_API_KEY = os.getenv("COHERE_API_KEY")

# OpenAI API Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
