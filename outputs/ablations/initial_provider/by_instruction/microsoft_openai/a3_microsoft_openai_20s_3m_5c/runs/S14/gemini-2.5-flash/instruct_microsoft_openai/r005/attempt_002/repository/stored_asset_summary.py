import os
from openai import AzureOpenAI
from storage_models import StoredAssetSummaryRequest, StoredAssetSummaryResponse

def stored_asset_summary(request: StoredAssetSummaryRequest) -> StoredAssetSummaryResponse:
    try:
        azure_openai_endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
        azure_openai_key = os.environ.get("AZURE_OPENAI_KEY")
        azure_openai_deployment_name = os.environ.get("AZURE_OPENAI_DEPLOYMENT_NAME", "text-davinci-003") # Example deployment name

        if not azure_openai_endpoint or not azure_openai_key:
            return StoredAssetSummaryResponse(success=False, error="AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_KEY environment variables must be set.")

        client = AzureOpenAI(
            azure_endpoint=azure_openai_endpoint,
            api_key=azure_openai_key,
            api_version="2023-05-15"
        )

        prompt = f"Summarize the following text, aiming for a {request.summary_length} summary: {request.text}"

        response = client.completions.create(
            model=azure_openai_deployment_name,
            prompt=prompt,
            max_tokens=150 if request.summary_length == "short" else (300 if request.summary_length == "medium" else 500),
            temperature=0.7
        )

        summary = response.choices[0].text.strip()
        return StoredAssetSummaryResponse(success=True, summary=summary)
    except Exception as e:
        return StoredAssetSummaryResponse(success=False, error=str(e))
