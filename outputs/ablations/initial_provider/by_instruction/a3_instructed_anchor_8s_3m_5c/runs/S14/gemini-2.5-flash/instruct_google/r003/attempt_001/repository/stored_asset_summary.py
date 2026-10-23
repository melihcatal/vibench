from vertexai.preview.language_models import TextGenerationModel
import dataclasses

@dataclasses.dataclass
class StoredAssetSummaryRequest:
    text_content: str
    max_output_tokens: int = 256
    temperature: float = 0.2

@dataclasses.dataclass
class StoredAssetSummaryResponse:
    summary_text: str

def summarize_stored_asset(
    request: StoredAssetSummaryRequest
) -> StoredAssetSummaryResponse:
    """Summarizes content extracted from a stored asset using Google Cloud Vertex AI (PaLM 2)."""
    model = TextGenerationModel.from_pretrained("text-bison@001")

    prompt = f"Summarize the following text:\n\n{request.text_content}"

    response = model.predict(
        prompt,
        max_output_tokens=request.max_output_tokens,
        temperature=request.temperature,
    )

    return StoredAssetSummaryResponse(
        summary_text=response.text
    )
