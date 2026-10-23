import os
from dashscope import Generation


def collect_platform_metadata(prompt: str, model_name: str = "qwen-turbo"):
    response = Generation.call(
        model=model_name,
        prompt=prompt,
        api_key=os.environ.get("DASHSCOPE_API_KEY"),
    )

    # DashScope response typically includes 'output' and 'usage'
    output_content = (
        response.output.text if response.output and response.output.text else ""
    )
    usage_info = response.usage.to_dict() if response.usage else {}

    metadata = {
        "model_name": model_name,
        "request_id": response.request_id,  # Provider-specific metadata
        "usage": usage_info,
        # Add other relevant metadata from the response object if available
    }
    return {"output": output_content, "metadata": metadata}
