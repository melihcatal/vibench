# metric_annotation_safety.py
# LATER-STEP implementation using Datadog Metrics API for annotation lookup and WatsonX Guardrails for safety checks

import os
from typing import List
from observability_client import ObservabilityClient
from observability_models import (
    AnnotationSafetyCheckRequest,
    AnnotationSafetyCheckResponse,
)
from ibm_watsonx_ai import WatsonXGuardrailsClient

# Provider identifier for this file (visible in code)
PROVIDER = "datadoc"


def check_annotation_safety(
    req: AnnotationSafetyCheckRequest,
) -> AnnotationSafetyCheckResponse:
    # Step 1: Retrieve recent annotations (as free text) for the given metric
    # This example assumes a simple key-value store where annotations are stored as tags on the metric.
    # In a real service, you would query the provider's annotation endpoint.
    client = ObservabilityClient()
    # Simulated fetch of annotation texts – replace with real provider call if available
    annotation_texts = client.query_recent(
        metric_name=req.free_text[0],  # reuse first element as placeholder metric name
        start="now-1d",
        end="now",
    )
    # Extract the text list (for demo we just use the request texts)
    texts = req.free_text
    # Step 2: Use WatsonX Guardrails to detect unsafe content
    guardrails = WatsonXGuardrailsClient()
    is_safe, unsafe_items = guardrails.detect_free_text_unsafe(texts)
    return AnnotationSafetyCheckResponse(safe=is_safe, unsafe_items=unsafe_items)


if __name__ == "__main__":
    # Example usage (remove or adapt when integrating into a real service)
    req = AnnotationSafetyCheckRequest(
        free_text=[
            "This metric indicates a potential security breach.",
            "System overload detected.",
        ]
    )
    result = check_annotation_safety(req)
    print(result)
