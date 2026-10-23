from __future__ import annotations

import base64
import os
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from openai import OpenAI
from google.cloud import vision
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.core.credentials import AzureKeyCredential
import boto3

from vision_models import (
    ImageAnalysisRequest,
    ImageDescriptionRequest,
    ImageSafetyRequest,
    ImageTextRequest,
)


OPENAI_VISION_MODEL = os.getenv("OPENAI_VISION_MODEL", "gpt-4o")
AZURE_VISION_ENDPOINT = os.getenv("AZURE_VISION_ENDPOINT", "")
AZURE_VISION_KEY = os.getenv("AZURE_VISION_KEY", "")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")


@dataclass
class OpenAIVisionClient:
    client: OpenAI
    model: str = OPENAI_VISION_MODEL

    def describe_image(self, request: ImageDescriptionRequest) -> Dict[str, Any]:
        payload = request.as_openai_content()
        response = self.client.responses.create(
            model=self.model,
            input=[
                {
                    "role": "user",
                    "content": payload,
                }
            ],
            max_output_tokens=request.max_tokens,
        )
        return {"text": response.output_text, "model": self.model}


@dataclass
class AzureVisionAnalyzer:
    client: ImageAnalysisClient

    def analyze_image(self, request: ImageAnalysisRequest) -> Dict[str, Any]:
        image_bytes = request.load_bytes()
        result = self.client.analyze(
            image_data=image_bytes,
            visual_features=["objects", "tags"],
        )
        labels: List[Dict[str, Any]] = []
        for obj in getattr(result, "objects_result", {}).get("values", []) if isinstance(getattr(result, "objects_result", None), dict) else getattr(getattr(result, "objects_result", None), "values", []):
            labels.append({"name": getattr(obj, "tags", [{}])[0].get("name", getattr(obj, "name", "")), "confidence": getattr(obj, "confidence", 0.0)})
        for tag in getattr(getattr(result, "tags_result", None), "values", []) or []:
            labels.append({"name": getattr(tag, "name", ""), "confidence": getattr(tag, "confidence", 0.0)})
        return {"labels": labels, "provider": "azure-ai-vision"}


@dataclass
class GoogleVisionClient:
    client: vision.ImageAnnotatorClient

    def detect_text(self, request: ImageTextRequest) -> Dict[str, Any]:
        image = vision.Image(content=request.load_bytes())
        response = self.client.text_detection(image=image)
        texts = [t.description for t in response.text_annotations if getattr(t, "description", None)]
        return {"texts": texts, "provider": "google-cloud-vision"}


@dataclass
class AwsRekognitionClient:
    client: Any

    def score_image(self, request: ImageSafetyRequest) -> Dict[str, Any]:
        image_bytes = request.load_bytes()
        response = self.client.detect_moderation_labels(Image={"Bytes": image_bytes}, MinConfidence=50)
        labels = response.get("ModerationLabels", [])
        return {"labels": labels, "provider": "aws-rekognition"}


def get_openai_vision_client() -> OpenAIVisionClient:
    return OpenAIVisionClient(client=OpenAI())


def get_azure_vision_analyzer() -> AzureVisionAnalyzer:
    if not AZURE_VISION_ENDPOINT or not AZURE_VISION_KEY:
        raise RuntimeError("AZURE_VISION_ENDPOINT and AZURE_VISION_KEY are required for Azure AI Vision")
    return AzureVisionAnalyzer(
        client=ImageAnalysisClient(endpoint=AZURE_VISION_ENDPOINT, credential=AzureKeyCredential(AZURE_VISION_KEY))
    )


def get_google_vision_client() -> GoogleVisionClient:
    return GoogleVisionClient(client=vision.ImageAnnotatorClient())


def get_aws_rekognition_client() -> AwsRekognitionClient:
    return AwsRekognitionClient(client=boto3.client("rekognition", region_name=AWS_REGION))
