import os
from google.cloud import aiplatform

def summarize_asset_content(text_content: str) -> str:
    aiplatform.init(project=os.environ.get("GOOGLE_CLOUD_PROJECT"))
    parameters = {
        "max_output_tokens": 200,
        "temperature": 0.2,
        "top_p": 0.8,
        "top_k": 40
    }
    model = aiplatform.gapic.PredictionServiceClient.get_endpoint(
        name=aiplatform.gapic.PredictionServiceClient.endpoint_path(
            project=os.environ.get("GOOGLE_CLOUD_PROJECT"),
            location="us-central1",
            publisher="google",
            model="text-bison@001",
        )
    )
    response = model.predict(
        endpoint=model.name,
        instances=[{"prompt": f"Summarize the following text:\n\n{text_content}"}],
        parameters=parameters,
    )
    return response.predictions[0]["content"]
