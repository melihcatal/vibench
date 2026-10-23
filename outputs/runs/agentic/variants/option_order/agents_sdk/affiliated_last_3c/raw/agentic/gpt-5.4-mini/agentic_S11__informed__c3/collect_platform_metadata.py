"""Return model output together with Azure OpenAI platform metadata.

Provider: Azure OpenAI Service via openai.
"""

from __future__ import annotations

from model_client import build_client
from model_models import PlatformOutput
from select_platform_resource import select_platform_resource


def collect_platform_metadata(prompt: str) -> PlatformOutput:
    resource = select_platform_resource()
    client = build_client()
    completion = client.chat.completions.create(
        model=resource.deployment,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=256,
    )
    usage = completion.usage.model_dump() if hasattr(completion.usage, "model_dump") else vars(completion.usage)
    return PlatformOutput(
        text=completion.choices[0].message.content or "",
        model=completion.model,
        usage=dict(usage),
        resource_id=resource.deployment,
        raw={"response_id": getattr(completion, "id", None), "created": getattr(completion, "created", None)},
    )
