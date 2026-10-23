# [LATER-STEP] stored_asset_summary.py

# Uses Alibaba Cloud Qwen (DashScope) LLM for summarizing stored asset content.
# Provider: Alibaba Cloud Qwen via DashScope
# SDK: dashscope
# Auth: DASHSCOPE_API_KEY

import os
import json
from dashscope import AssetSummaryTool
from .storage_client import get_bucket_name
from .storage_client import _download_object


# Public entry point
async def summarize_asset(
    object_key: str, bucket_name: str = None, model_name: str = "qwen_vl_max"
) -> dict:
    """Generates a concise summary of arbitrary stored asset text.

    Args:
        object_key: S3 key pointing to a text-based asset (CSV, JSON, Markdown, etc.).
        bucket_name: Optional bucket name; pulls from env var otherwise.
        model_name: DashScope model to use for summarization.

    Returns:
        dict containing `summary`, `originalTextLength`, `model` used, etc.
    """
    if bucket_name is None:
        bucket_name = get_bucket_name()

    raw_content = _download_object(bucket_name, object_key).decode("utf-8")
    tool = AssetSummaryTool(model=model_name)
    result = tool.summarize(raw_content)
    return {
        "summary": result.summary,
        "originalLength": len(raw_content),
        "model": model_name,
    }


# Example usage:
# if __name__ == '__main__':
#     print(summarize_asset('document.txt'))
