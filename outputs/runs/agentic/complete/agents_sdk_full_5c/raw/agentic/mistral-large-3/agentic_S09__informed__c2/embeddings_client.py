import os
from typing import Optional

import dashscope
from dashscope import TextEmbedding


def get_dashscope_client() -> Optional[TextEmbedding]:
    api_key = os.getenv("DASHSCOPE_API_KEY")
    if not api_key:
        raise ValueError("DASHSCOPE_API_KEY environment variable not set")
    dashscope.api_key = api_key
    return TextEmbedding