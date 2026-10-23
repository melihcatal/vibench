import os
from dashscope import Generation


def get_dashscope_client():
    # DashScope SDK typically initializes client implicitly via API key in os.environ
    # or passed directly to call methods. This function can ensure API key is set.
    api_key = os.environ.get("DASHSCOPE_API_KEY")
    if not api_key:
        raise ValueError("DASHSCOPE_API_KEY environment variable not set.")
    print("DashScope client configured.")
    # For DashScope, the 'client' is often the module itself for generation tasks
    return Generation
