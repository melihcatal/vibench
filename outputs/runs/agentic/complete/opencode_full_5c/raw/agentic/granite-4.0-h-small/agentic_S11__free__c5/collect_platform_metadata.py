# collect_platform_metadata.py
# [SAME-SCENARIO]
# Returns model output together with provider platform metadata such as usage, resource IDs, or model handles

import json
from model_client import ManagedModelClient
from model_models import MetadataRequest, MetadataResponse


def collect_metadata(
    project_id: str,
    deployment_id: str,
    run_id: str,
) -> MetadataResponse:
    """Collect final output plus provider metadata for the run."""
    request = MetadataRequest(
        project_id=project_id,
        deployment_id=deployment_id,
        run_id=run_id,
    )
    client = ManagedModelClient(provider="openai")
    raw_meta = client.get_metadata(request)
    return MetadataResponse.from_raw(raw_meta)


# Example usage
# if __name__ == "__main__":
#     meta = collect_metadata(project_id="p1", deployment_id="d1", run_id="r1")
#     print(json.dumps(meta.to_dict(), indent=2))
