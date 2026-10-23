import os
from storage_models import SummarizeRequest, SummarizeResponse
from typing import Any

PROVIDER = "Gemini (Google Gemini API)"

# Placeholder LLM client using Google Gemini SDK
# In production you would import google-generativeai (google-genai) and instantiate generative_model
try:
    import google.generativeai as genai
except ImportError:
    genai = None

if genai:
    # Assumes GOOGLE_API_KEY is set elsewhere
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    llm = genai.GenerativeModel("gemini-1.5-flash")  # model family identifier
else:
    llm = None


def summarize_asset(request: SummarizeRequest) -> SummarizeResponse:
    """
    Generate a concise summary of extracted asset content using a hosted LLM.

    Args:
        request (SummarizeRequest): raw content and optional max length.
    Returns:
        SummarizeResponse: generated summary.
    """
    content = request.content
    if not content:
        raise ValueError("Empty content provided for summarization")
    if not llm:
        raise RuntimeError(
            f"[{PROVIDER}] LLM client not configured - missing credentials"
        )
    # Call the model; Gemini's generate_content returns a response with .text
    response = llm.generate_content(
        content, generation_config={"max_output_tokens": request.max_target_length}
    )
    summary = response.text.strip()
    print(
        f"[{PROVIDER}] Summarized content ({len(content)} chars) -> summary ({len(summary)} chars)"
    )
    return SummarizeResponse(summary=summary)


# Simple CLI entry point for testing
if __name__ == "__main__":
    import sys, json

    if len(sys.argv) < 2:
        print('Usage: stored_asset_summary.py "<content>" [max_target_length]')
        sys.exit(1)
    content = sys.argv[1]
    max_len = int(sys.argv[2]) if len(sys.argv) > 2 else 200
    resp = summarize_asset(SummarizeRequest(content=content, max_target_length=max_len))
    print(json.dumps({"summary": resp.summary}, ensure_ascii=False, indent=2))
