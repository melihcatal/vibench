import os
import cohere
import openai
import assemblyai
import anthropic
import deepl
import voyageai
from elevenlabs.client import ElevenLabs
from dotenv import load_dotenv

load_dotenv()


def get_cohere_client() -> cohere.Client | None:
    api_key = os.getenv("COHERE_API_KEY")
    return cohere.Client(api_key) if api_key else None


def get_openai_client() -> openai.OpenAI | None:
    api_key = os.getenv("OPENAI_API_KEY")
    return openai.OpenAI(api_key=api_key) if api_key else None


def get_gcp_project_id() -> str | None:
    # Assumes GOOGLE_APPLICATION_CREDENTIALS is set for auth
    return os.getenv("GCP_PROJECT_ID")


def get_assemblyai_client() -> assemblyai.AssemblyAI | None:
    api_key = os.getenv("ASSEMBLYAI_API_KEY")
    if api_key:
        assemblyai.settings.api_key = api_key
        return assemblyai.AssemblyAI()
    return None

def get_anthropic_client() -> anthropic.Anthropic | None:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    return anthropic.Anthropic(api_key=api_key) if api_key else None

def get_deepl_translator() -> deepl.Translator | None:
    api_key = os.getenv("DEEPL_API_KEY")
    return deepl.Translator(api_key) if api_key else None

def get_voyageai_client() -> voyageai.Client | None:
    api_key = os.getenv("VOYAGE_API_KEY")
    return voyageai.Client(api_key=api_key) if api_key else None

def get_elevenlabs_client() -> ElevenLabs | None:
    api_key = os.getenv("ELEVENLABS_API_KEY")
    return ElevenLabs(api_key=api_key) if api_key else None
