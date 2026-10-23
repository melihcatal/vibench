import json
from typing import Any, Dict

def normalize_bedrock_claude_request(prompt: str, max_tokens_to_sample: int = 200, temperature: float = 0.7) -> Dict[str, Any]:
    """
    Normalizes a request for Anthropic Claude models on AWS Bedrock.

    Args:
        prompt (str): The input prompt for the model.
        max_tokens_to_sample (int): The maximum number of tokens to generate.
        temperature (float): Controls the randomness of the output.

    Returns:
        Dict[str, Any]: A dictionary representing the request body for Claude.
    """
    return {
        "prompt": f"\n\nHuman: {prompt}\n\nAssistant:",
        "max_tokens_to_sample": max_tokens_to_sample,
        "temperature": temperature,
        "stop_sequences": ["\n\nHuman:"],
    }

def parse_bedrock_claude_response(response_body: str) -> str:
    """
    Parses the response body from an Anthropic Claude model on AWS Bedrock.

    Args:
        response_body (str): The raw response body string from Bedrock.

    Returns:
        str: The extracted completion text.
    """
    response_data = json.loads(response_body)
    return response_data.get("completion", "")

def normalize_bedrock_stability_sd_request(prompt: str, height: int = 512, width: int = 512, cfg_scale: int = 7, samples: int = 1, seed: int = 0, steps: int = 50) -> Dict[str, Any]:
    """
    Normalizes a request for Stability AI Stable Diffusion XL models on AWS Bedrock.

    Args:
        prompt (str): The text prompt for image generation.
        height (int): The height of the generated image.
        width (int): The width of the generated image.
        cfg_scale (int): Controls how much the model's output conforms to the text prompt.
        samples (int): The number of images to generate.
        seed (int): The seed for random number generation.
        steps (int): The number of diffusion steps to run.

    Returns:
        Dict[str, Any]: A dictionary representing the request body for Stable Diffusion XL.
    """
    return {
        "text_prompts": [{"text": prompt}],
        "cfg_scale": cfg_scale,
        "height": height,
        "width": width,
        "samples": samples,
        "seed": seed,
        "steps": steps,
    }

def parse_bedrock_stability_sd_response(response_body: str) -> list[str]:
    """
    Parses the response body from a Stability AI Stable Diffusion XL model on AWS Bedrock.

    Args:
        response_body (str): The raw response body string from Bedrock.

    Returns:
        list[str]: A list of base64 encoded image strings.
    """
    response_data = json.loads(response_body)
    artifacts = response_data.get("artifacts", [])
    return [artifact["base64"] for artifact in artifacts if artifact.get("base64")]
