import os
from typing import List, Dict, Any
from ibm_watsonx_ai import APIClient
from ibm_watsonx_ai.foundation_models import Embeddings


def embed_moderation_reason(reasons: List[str]) -> List[List[float]]:
    """
    Embeds moderation rationales for case retrieval using IBM Watsonx.ai Slate Embeddings.
    """
    api_key = os.getenv("WATSONX_API_KEY")
    project_id = os.getenv("WATSONX_PROJECT_ID")

    if not api_key or not project_id:
        raise ValueError(
            "Watsonx.ai credentials not found. "
            "Set WATSONX_API_KEY and WATSONX_PROJECT_ID."
        )

    client = APIClient(api_key=api_key, project_id=project_id)
    embeddings_model = Embeddings(
        model_id="ibm/slate-125m-english-rtrvr", params={"truncate_input_tokens": 512}
    )

    try:
        responses = []
        for reason in reasons:
            response = client.foundation_models.embeddings.create(
                model=embeddings_model, inputs=[reason]
            )
            responses.append(response.results[0].embedding)
        return responses
    except Exception as e:
        raise Exception(f"Watsonx.ai embeddings failed: {str(e)}")
