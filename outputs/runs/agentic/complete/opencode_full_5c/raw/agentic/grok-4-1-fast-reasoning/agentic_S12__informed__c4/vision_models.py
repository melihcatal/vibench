"""
Standard data shapes for vision tasks.

Labels: {"labels": [{"name": str, "confidence": float}, ...]}

Description: {"description": str, "confidence": float}

Texts: {"texts": [str, ...]}

Safety: {"is_safe": bool, "risks": {str: float}, "moderation_labels": [...]}

VisionAnalysis: dict with keys 'labels', 'description', 'texts', 'safety'
"""
