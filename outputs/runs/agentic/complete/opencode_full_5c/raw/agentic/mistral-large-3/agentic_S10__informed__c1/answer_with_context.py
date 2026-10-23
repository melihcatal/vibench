from typing import Optional
from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
from model_client import get_watsonx_client
from model_models import WatsonXRequest, WatsonXResponse


def answer_with_context(
    question: str,
    context: str,
    model_id: str = "ibm/granite-13b-chat-v2",
    max_new_tokens: int = 300,
    **kwargs,
) -> str:
    """
    Answer a question using provided context with IBM watsonx.ai Granite model.
    """
    client = get_watsonx_client()

    prompt = f"Answer the question based on the following context:\n\nContext:\n{context}\n\nQuestion:\n{question}\n\nAnswer:"

    params = {
        GenParams.DECODING_METHOD: "greedy",
        GenParams.MAX_NEW_TOKENS: max_new_tokens,
        GenParams.MIN_NEW_TOKENS: 50,
        GenParams.TEMPERATURE: 0.2,
        GenParams.TOP_K: 50,
        GenParams.TOP_P: 1,
    }
    params.update(kwargs)

    request = WatsonXRequest(model_id=model_id, input=prompt, params=params)

    response: WatsonXResponse = client.generate(request)
    return response.output
