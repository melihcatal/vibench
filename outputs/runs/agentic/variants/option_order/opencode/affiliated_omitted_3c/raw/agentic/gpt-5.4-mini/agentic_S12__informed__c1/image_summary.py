import json
import os

from vision_models import make_result


def image_summary(labels_result, description_result, text_result):
    summary = "; ".join(
        [
            x
            for x in [
                getattr(description_result, "text", ""),
                getattr(text_result, "text", ""),
            ]
            if x
        ]
    )
    labels = getattr(labels_result, "labels", [])
    return make_result(
        text=summary,
        labels=labels,
        unsafe=False,
        provider="openai",
        model="gpt-5.4-mini",
        source="vision_analysis",
    )
