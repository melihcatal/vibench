import os
from openai import OpenAI

from storage_models import StoredAssetSummaryRequest, StoredAssetSummaryResponse

def stored_asset_summary(request: StoredAssetSummaryRequest) -> StoredAssetSummaryResponse:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    client = OpenAI(api_key=api_key)

    prompt = f"Summarize the following text in about {request.summary_length} words: {request.text}"
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # Concrete model identifier
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes text."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=request.summary_length * 2, # Allow more tokens for output safety
        temperature=0.7,
    )

    summary = response.choices[0].message.content.strip()
    return StoredAssetSummaryResponse(summary=summary)
