import os
import google.generativeai as genai
from typing import Optional

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def get_vision_model(model_name: str = "gemini-1.5-flash") -> genai.GenerativeModel:
    return genai.GenerativeModel(
        model_name,
        generation_config={"response_mime_type": "application/json"},
        safety_settings=[
            genai.types.HarmCategoryBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        ]
        * 4,
    )
