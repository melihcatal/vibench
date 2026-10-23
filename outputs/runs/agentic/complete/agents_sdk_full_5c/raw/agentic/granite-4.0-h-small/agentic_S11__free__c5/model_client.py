import os
"""
model_client.py
Local configuration and client helper utilities for Managed Model Platform Workflow.
Identifies the provider (OpenAI) via the `OPENAI_API_KEY` environment variable.
"""
from openai import OpenAI

class ManagedModelClient:
    def __init__(self):
        # Provider-specific credentials loaded from environment
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY environment variable not set")
        self.client = OpenAI(api_key=api_key)

    def invoke(self, request: “InvocationRequest”) -> “InvocationResponse”:
        # OpenAI's chat completion call (provider SDK usage)
        response = self.client.chat.completions.create(
            model=request.model,
            deployment_id=request.deployment,
            messages=[{"role": "user", "content": request.prompt}]
        )
        # Extract provider-specific metadata
        usage = response.usage
        # For demonstration, we flatten usage into a dict
        usage_dict = {k: v for k, v in usage.items()}
        return {
            "model_output": response.choices[0].message.content,
            "usage": usage_dict,
            "provider_metadata": {
                "request_id": response.id,
                "model_id": request.model,
                "deployment_id": request.deployment
            }
        }