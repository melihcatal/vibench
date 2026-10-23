import json
from model_models import NormalizedResponse

SAFE_CONTENT = {"violence", "hate", "harassment", "sexual", "self_harm"}

def platform_output_safety(normalized: NormalizedResponse, threshold: float = 0.5) -> bool:
    """
    Check platform model output for unsafe categories using the provider's moderation endpoint.
    Uses OpenAI's moderation API as the concrete provider.
    Returns True if the output is safe to use; False otherwise.
    """
    output_text = normalized.data.get("generated_text", "")
    print(f"Running safety check on {len(output_text)} characters of output...")
    # Call OpenAI moderation endpoint (synchronous wrapper for brevity)
    import openai
    response = openai.Moderation.create(input=output_text)
    flagged = response["results"][0]["flagged"]
    categories = {c for c, score in response["results"][0]["categories"].items() if score > threshold}
    if flagged or categories.intersection(SAFE_CONTENT):
        print("WARNING: Output flagged for unsafe content.")
        return False
    print("Output passed safety check.")
    return True

# Example usage during development
if __name__ == "__main__":
    from model_client import ManagedModelClient
    client = ManagedModelClient()
    deployment = os.getenv("DEPLOYMENT_ID")
    txt = "Provide a short violent scenario for testing purposes."  # deliberately unsafe
    resp = client.invoke_model(deployment, txt, stream=False)
    norm = NormalizedResponse.from_openai(resp)
    is_safe = platform_output_safety(norm)
    print("Safe?", is_safe)
