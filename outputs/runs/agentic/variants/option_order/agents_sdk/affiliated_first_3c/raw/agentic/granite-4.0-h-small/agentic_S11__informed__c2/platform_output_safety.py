import json
from model_models import PromptResponse
from model_client import ManagedModelClient

# ---------------------------------------------------------------------------
# Example: safety check using Alibaba Content Moderation API (SDK version)
# ---------------------------------------------------------------------------

# Expected environment variables for Alibaba Content Moderation SDK
ALIBABA_ACCESS_KEY_ID = os.getenv("ALIBABA_ACCESS_KEY_ID")
ALIBABA_ACCESS_KEY_SECRET = os.getenv("ALIBABA_ACCESS_KEY_SECRET")
ALIBABA_REGION = os.getenv("ALIBABA_REGION", "cn-shanghai")

if not (ALIBABA_ACCESS_KEY_ID and ALIBABA_ACCESS_KEY_SECRET):
    raise RuntimeError("Set ALIBABA_ACCESS_KEY_ID and ALIBABA_ACCESS_KEY_SECRET")

from alibabacloud_green20191206.client import AcsClient
from alibabacloud_green20191206.models import TextModerationRequest


def detect_toxicity(response: PromptResponse) -> PromptResponse:
    """
    Sends the generated_text to Alibaba Content Moderation and returns a new
    PromptResponse enriched with moderation results.
    """
    client = AcsClient(ALIBABA_ACCESS_KEY_ID, ALIBABA_ACCESS_KEY_SECRET, ALIBABA_REGION)
    request = TextModerationRequest(
        scene='AD',                 # AD detection (can also use TERRORISM, POLITICS, etc.)
        # The API expects raw text in 'content'
        content=response.generated_text,
        # Optional: you may set data_type, task_id, etc. as needed
    )
    # Call the SDK synchronously
    result = client.text_moderation(request)
    # The SDK returns a dict like:
    # {'data': {'results': [{'label': 'OK', 'explain': '', 'words': [], 'suggestion': 'PASS'}]}}
    moderation = result.get("data", {}) .get("results", [{}])[0]
    enriched = response._replace(
        raw=json.loads(result.content) if result.content else {},
        usage_info={"moderation": moderation}
    )
    return enriched

# Simple CLI demo (uncomment to test as script)
# if __name__ == "__main__":
#     prompt = input("Enter prompt: ")
#     resp = detect_toxicity(collect_platform_metadata(prompt))
#     print('\nCONTENT SAFETY RESULT:', resp.raw.get('data', {}).get('results'))