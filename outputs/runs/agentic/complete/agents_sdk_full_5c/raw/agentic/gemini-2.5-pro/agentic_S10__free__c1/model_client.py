import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Keys for various services
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY") # Used for Gemini and Perspective
DEEPL_API_KEY = os.getenv("DEEPL_API_KEY")
VOYAGE_API_KEY = os.getenv("VOYAGE_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

# You can add client initialization logic here if desired,
# but for this project, we will initialize clients in their respective modules
# to make dependencies explicit.
