from vertexai.language_models import TextGenerationModel
from typing import Optional


def summarize_stored_asset_content(
    content: str, temperature: float = 0.2, max_output_tokens: int = 256
) -> str:
    """
    Summarize content extracted from a stored asset using Vertex AI Text Generation.
    Model: text-bison@002
    """
    model = TextGenerationModel.from_pretrained("text-bison@002")
    response = model.predict(
        f"Summarize the following content:\n\n{content}",
        temperature=temperature,
        max_output_tokens=max_output_tokens,
    )
    return response.text