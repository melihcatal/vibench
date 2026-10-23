import os
from typing import Optional

# Provider identified in code
PROVIDER = "Mistral"

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")


def get_chat_client() -> object:
    # Returns a client ready for chat calls
    return mistralai.ChatClient(MISTRAL_API_KEY)


# Simple utility to call the chat endpoint
# Implemented here instead of inside each inference file to avoid duplication
