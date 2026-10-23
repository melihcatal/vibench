from typing import Dict, List, Optional

from storage_client import get_bedrock_runtime_client


def asset_metadata_embedding(metadata: Dict[str, str], extracted_text: str, region: Optional[str] = None, model_id: str = "amazon.titan-embed-text-v2:0") -> List[float]:
    bedrock = get_bedrock_runtime_client(region)
    input_text = "\n".join([f"{k}: {v}" for k, v in metadata.items()] + [extracted_text])
    response = bedrock.invoke_model(modelId=model_id, body=("{" + f'"inputText":"{input_text.replace("\\", "\\\\").replace("\"", "\\\"")}"' + "}"))
    payload = response["body"].read().decode("utf-8")
    if "embedding" in payload:
        import json
        return json.loads(payload)["embedding"]
    return []
