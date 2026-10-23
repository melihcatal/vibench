from typing import Iterator
from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
from model_client import get_watsonx_client
from model_models import WatsonXRequest


def stream_completion(
    prompt: str,
    model_id: str = "ibm/granite-13b-chat-v2",
    max_new_tokens: int = 200,
    **kwargs,
) -> Iterator[str]:
    """
    Stream partial output tokens from IBM watsonx.ai Granite model.
    """
    client = get_watsonx_client()

    params = {
        GenParams.DECODING_METHOD: "greedy",
        GenParams.MAX_NEW_TOKENS: max_new_tokens,
        GenParams.MIN_NEW_TOKENS: 1,
        GenParams.TEMPERATURE: 0.7,
        GenParams.TOP_K: 50,
        GenParams.TOP_P: 1,
        GenParams.STREAM: True,
    }
    params.update(kwargs)

    request = WatsonXRequest(model_id=model_id, input=prompt, params=params)

    for chunk in client.generate_stream(request):
        yield chunk
