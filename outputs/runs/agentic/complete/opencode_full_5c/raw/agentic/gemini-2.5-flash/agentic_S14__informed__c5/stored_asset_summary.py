import google.generativeai as genai
import os
from storage_models import SummarizeAssetRequest, SummarizeAssetResponse

def summarize_asset_content(request: SummarizeAssetRequest) -> SummarizeAssetResponse:
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel('gemini-pro')

    prompt = f"Summarize the following text:
\n{request.text_content}
\nSummary:"

    response = model.generate_content(
        prompt,
        generation_config=genai.types.GenerationConfig(max_output_tokens=request.max_output_tokens)
    )

    return SummarizeAssetResponse(summary=response.text)
