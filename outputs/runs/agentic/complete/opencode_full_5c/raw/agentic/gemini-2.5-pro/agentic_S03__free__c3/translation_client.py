import os
from google.cloud import translate_v2 as translate
import anthropic
import openai
import cohere
from elevenlabs.client import ElevenLabs

# Google Cloud Translate
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv(
    "GOOGLE_APPLICATION_CREDENTIALS", ""
)
google_translate_client = translate.Client()

# Anthropic
anthropic_client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# OpenAI
openai_client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Cohere
cohere_client = cohere.Client(os.getenv("COHERE_API_KEY"))

# ElevenLabs
elevenlabs_client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))
