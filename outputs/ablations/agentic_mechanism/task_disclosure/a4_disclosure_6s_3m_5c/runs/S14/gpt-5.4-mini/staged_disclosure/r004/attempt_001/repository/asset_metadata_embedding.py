import json
import os
from typing import Any, Dict, Iterable, List, Optional

from openai import OpenAI


OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


def _normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, (int, float, bool)):
        return str(value)
    if isinstance(value, dict):
        parts = []
        for key in sorted(value.keys()):
            normalized = _normalize_text(value[key])
            if normalized:
                parts.append(f"{key}: {normalized}")
        return "\n".join(parts)
    if isinstance(value, (list, tuple, set)):
        parts = [_normalize_text(item) for item in value]
        return "\n".join(part for part in parts if part)
    return str(value).strip()


def build_embedding_text(metadata: Dict[str, Any], extracted_text: str) -> str:
    metadata_text = _normalize_text(metadata)
    extracted_text = (extracted_text or "").strip()
    combined_parts = []
    if metadata_text:
        combined_parts.append(f"metadata\n{metadata_text}")
    if extracted_text:
        combined_parts.append(f"extracted_text\n{extracted_text}")
    return "\n\n".join(combined_parts)


def embed_asset_metadata_and_text(
    metadata: Dict[str, Any],
    extracted_text: str,
    *,
    client: Optional[OpenAI] = None,
    model: Optional[str] = None,
) -> List[float]:
    text = build_embedding_text(metadata, extracted_text)
    if not text:
        return []
    openai_client = client or OpenAI()
    response = openai_client.embeddings.create(
        model=model or OPENAI_EMBEDDING_MODEL,
        input=text,
    )
    return list(response.data[0].embedding)


def embed_asset_record(asset: Dict[str, Any], *, client: Optional[OpenAI] = None, model: Optional[str] = None) -> Dict[str, Any]:
    metadata = asset.get("metadata", {}) if isinstance(asset, dict) else {}
    extracted_text = asset.get("extracted_text", "") if isinstance(asset, dict) else ""
    embedding = embed_asset_metadata_and_text(metadata, extracted_text, client=client, model=model)
    result = dict(asset) if isinstance(asset, dict) else {"asset": asset}
    result["search_embedding"] = embedding
    result["embedding_model"] = model or OPENAI_EMBEDDING_MODEL
    result["embedding_input"] = build_embedding_text(metadata, extracted_text)
    return result


def embed_assets(assets: Iterable[Dict[str, Any]], *, client: Optional[OpenAI] = None, model: Optional[str] = None) -> List[Dict[str, Any]]:
    return [embed_asset_record(asset, client=client, model=model) for asset in assets]


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Embed asset metadata and extracted text using OpenAI embeddings.")
    parser.add_argument("input", help="Path to a JSON file containing either one asset object or a list of asset objects.")
    parser.add_argument("--output", help="Optional path to write enriched JSON output.")
    parser.add_argument("--model", default=None, help="Override the embedding model.")
    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8") as f:
        payload = json.load(f)

    if isinstance(payload, list):
        output = embed_assets(payload, model=args.model)
    elif isinstance(payload, dict):
        output = embed_asset_record(payload, model=args.model)
    else:
        raise ValueError("Input JSON must be an object or an array of objects.")

    rendered = json.dumps(output, ensure_ascii=False, indent=2)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(rendered)
    else:
        print(rendered)


if __name__ == "__main__":
    main()
