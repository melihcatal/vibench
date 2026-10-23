# image_summary.py
from typing import List, Dict
from dataclasses import dataclass
import os
from .vision_models import extract_labels

@dataclass

class VisualAnalysis:
    labels: List[str] = None
    description: str = None
    safe: Dict = None


def image_summary(result_labels: List[str], result_description: str, result_safe: Dict) -> VisualAnalysis:
    """Aggregate results from the same-scenario steps into a reusable summary object."""
    return VisualAnalysis(labels=result_labels, description=result_description, safe=result_safe)
