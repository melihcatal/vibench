import os

# Example model configuration for each supported provider
# (Only one provider block should be active at a time)

# AWS Amazon Translate
AMAZON_SOURCE_LANG = "en"
AMAZON_TARGET_LANG = "es"

# ALIBABA Alibaba Machine Translation
ALIBABA_SOURCE_LANG = "en"
ALIBABA_TARGET_LANG = "zh"

# DEEPL DeepL API
DEEPL_AUTH_KEY = "YOUR_DEEPL_KEY"
DEEPL_SOURCE_LANG = "en"
DEEPL_TARGET_LANG = "fr"

# GOOGLE Google Cloud Translation
GOOGLE_CREDENTIALS_PATH = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
GOOGLE_SOURCE_LANG = "en"
GOOGLE_TARGET_LANG = "ja"

# AZURE Azure AI Translator
AZURE_TRANSLATOR_KEY = os.getenv("AZURE_TRANSLATOR_KEY")
AZURE_TRANSLATOR_REGION = os.getenv("AZURE_TRANSLATOR_REGION")
AZURE_SOURCE_LANG = "en"
AZURE_TARGET_LANG = "de"
