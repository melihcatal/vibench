import os
import openai
from storage_models import SummarizeTextRequest, SummarizeTextResponse

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def summarize_stored_asset_content(request: SummarizeTextRequest) -> SummarizeTextResponse:
    if not OPENAI_API_KEY:
        return SummarizeTextResponse(success=False, error_message="OPENAI_API_KEY environment variable not set")

    client = openai.OpenAI(api_key=OPENAI_API_KEY)
    
    try:
        # Using gpt-3.5-turbo for summarization
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes text concisely."},
                {"role": "user", "content": f"Summarize the following text:\n\n{request.text}"}
            ],
            max_tokens=request.max_tokens,
            temperature=0.7,
        )
        summary = response.choices[0].message.content.strip()
        return SummarizeTextResponse(success=True, summary=summary)
    except Exception as e:
        return SummarizeTextResponse(success=False, error_message=str(e))
