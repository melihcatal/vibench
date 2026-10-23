from typing import Optional, Dict, Any
import os
from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
from model_client import get_watsonx_client
from model_models import WatsonXRequest, WatsonXResponse


def summarize_text(
    text: str,
    model_id: str = "ibm/granite-13b-chat-v2",
    max_new_tokens: int = 200,
    **kwargs,
) -> str:
    """
    Summarize long text using IBM watsonx.ai Granite model.
    """
    client = get_watsonx_client()

    params = {
        GenParams.DECODING_METHOD: "greedy",
        GenParams.MAX_NEW_TOKENS: max_new_tokens,
        GenParams.MIN_NEW_TOKENS: 50,
        GenParams.TEMPERATURE: 0.1,
        GenParams.TOP_K: 50,
        GenParams.TOP_P: 1,
    }
    params.update(kwargs)

    request = WatsonXRequest(
        model_id=model_id,
        input=f"Summarize the following text:\n\n{text}",
        params=params,
    )

    response: WatsonXResponse = client.generate(request)
    return response.output
