import os
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

def embed_platform_output(text: str) -> list[float]:
    """
    Embeds platform output using Google's Generative AI embedding model.

    Args:
        text: The text content to embed.

    Returns:
        A list of floats representing the embedding vector.
    """
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel("embedding-001")
    response = model.embed_content(
        content=text,
        task_type="retrieval_document",
        safety_settings={
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        }
    )
    return response["embedding"]
