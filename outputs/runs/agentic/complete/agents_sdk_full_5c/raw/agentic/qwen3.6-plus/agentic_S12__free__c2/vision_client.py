"""
vision_client.py - Provide local configuration and client helper utilities
for Static Image and Visual Understanding tasks.

Provider: Google Cloud Vision API (vision.googleapis.com)
Provider SDK: google-cloud-vision
Provider Identifying Signals: google.cloud.vision_v1.ImageAnnotatorClient,
                              GCLOUD_VISION_ env vars, vision.googleapis.com
"""

import os
from typing import Optional, Dict, Any
from google.cloud import vision_v1
from google.api_core import client_options

from vision_models import (
    VisionImageRequest,
    ImageLabelsResponse,
    ImageDescriptionResponse,
    ImageTextResponse,
    ImageSafetyResponse,
    ImageLabel,
    DetectedText,
    SafetyRating,
)


class GoogleVisionClient:
    """
    Client wrapper for Google Cloud Vision API.
    
    Provider: Google Cloud Vision API
    API Endpoint: vision.googleapis.com
    SDK: google.cloud.vision_v1
    """

    DEFAULT_ENDPOINT = "vision.googleapis.com"
    DEFAULT_MODEL = "builtin/stable"

    def __init__(
        self,
        credentials_path: Optional[str] = None,
        project_id: Optional[str] = None,
        api_endpoint: Optional[str] = None,
    ):
        self.project_id = project_id or os.environ.get(
            "GCLOUD_VISION_PROJECT_ID", ""
        )
        self.api_endpoint = api_endpoint or os.environ.get(
            "GCLOUD_VISION_API_ENDPOINT", self.DEFAULT_ENDPOINT
        )

        client_opts = client_options.ClientOptions(
            api_endpoint=self.api_endpoint
        )

        if credentials_path:
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path
        elif creds_env := os.environ.get("GCLOUD_VISION_CREDENTIALS_PATH"):
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = creds_env

        self.client = vision_v1.ImageAnnotatorClient(
            client_options=client_opts
        )

    def _make_google_image(self, request: VisionImageRequest) -> vision_v1.Image:
        """Create a Google Cloud Vision Image from our normalized request."""
        if request.image_bytes:
            return vision_v1.Image(content=request.image_bytes)
        elif request.image_uri:
            source = vision_v1.GcsImageSource(image_uri=request.image_uri)
            return vision_v1.Image(source=source)
        raise ValueError("No image data available in request")

    def detect_labels(
        self,
        request: VisionImageRequest,
        max_results: int = 10,
    ) -> ImageLabelsResponse:
        """
        Detect labels/objects in an image using Google Cloud Vision API.
        
        Uses vision_v1.Feature.Type.LABEL_DETECTION
        Model: builtin/stable
        """
        try:
            image = self._make_google_image(request)
            feature = vision_v1.Feature(
                type_=vision_v1.Feature.Type.LABEL_DETECTION,
                max_results=max_results,
            )
            response = self.client.annotate_image(
                request={"image": image, "features": [feature]}
            )

            labels = [
                ImageLabel.from_google_label(label)
                for label in response.label_annotations
            ]

            return ImageLabelsResponse(
                labels=labels,
                raw_response={"label_count": len(labels)},
            )
        except Exception as e:
            return ImageLabelsResponse(error=str(e))

    def describe_image(
        self,
        request: VisionImageRequest,
        max_results: int = 10,
    ) -> ImageDescriptionResponse:
        """
        Generate a visual description for an image using Google Cloud Vision API.
        
        Uses vision_v1.Feature.Type.IMAGE_PROPERTIES for dominant colors/topics
        combined with label detection for description generation.
        """
        try:
            image = self._make_google_image(request)

            features = [
                vision_v1.Feature(
                    type_=vision_v1.Feature.Type.LABEL_DETECTION,
                    max_results=max_results,
                ),
                vision_v1.Feature(
                    type_=vision_v1.Feature.Type.WEB_DETECTION,
                    max_results=max_results,
                ),
                vision_v1.Feature(
                    type_=vision_v1.Feature.Type.IMAGE_PROPERTIES,
                ),
            ]

            response = self.client.annotate_image(
                request={"image": image, "features": features}
            )

            labels = response.label_annotations
            web_entities = response.web_detection.web_entities

            topics = []
            if labels:
                topics = [l.description for l in labels if l.score > 0.5]
            if web_entities:
                topics.extend(
                    [e.description for e in web_entities[:5] if e.description]
                )

            description_parts = []
            if labels:
                top_labels = sorted(labels, key=lambda x: x.score, reverse=True)
                desc = top_labels[0].description if top_labels else "image"
                description_parts.append(
                    f"An image showing {desc}"
                    + (f" with {', '.join(topics[1:4])}" if len(topics) > 1 else "")
                    + "."
                )
            if web_entities:
                best_guess = response.web_detection.best_guess_labels
                if best_guess:
                    description_parts.append(
                        f"Context: {best_guess[0].label}"
                    )

            full_description = " ".join(description_parts) if description_parts else "No description generated."

            confidence = labels[0].score if labels else 0.0

            return ImageDescriptionResponse(
                description=full_description,
                confidence=confidence,
                topics=topics,
                raw_response={
                    "label_count": len(labels),
                    "web_entity_count": len(web_entities),
                },
            )
        except Exception as e:
            return ImageDescriptionResponse(
                description="", confidence=0.0, error=str(e)
            )

    def detect_text(
        self,
        request: VisionImageRequest,
        language_hints: Optional[list] = None,
    ) -> ImageTextResponse:
        """
        Detect text in an image using Google Cloud Vision API (OCR).
        
        Uses vision_v1.Feature.Type.TEXT_DETECTION
        Supports language hints for improved accuracy.
        """
        try:
            image = self._make_google_image(request)

            image_context = None
            if language_hints:
                image_context = vision_v1.ImageContext(
                    language_hints=language_hints
                )

            feature = vision_v1.Feature(
                type_=vision_v1.Feature.Type.TEXT_DETECTION,
                max_results=50,
            )

            req_kwargs = {"image": image, "features": [feature]}
            if image_context:
                req_kwargs["image_context"] = image_context

            response = self.client.annotate_image(request=req_kwargs)

            texts = [
                DetectedText.from_google_text(ann)
                for ann in response.text_annotations
            ]

            full_text = texts[0].text if texts else ""

            return ImageTextResponse(
                texts=texts[1:] if len(texts) > 1 else [],
                full_text=full_text,
                raw_response={"text_block_count": len(texts) - 1 if texts else 0},
            )
        except Exception as e:
            return ImageTextResponse(error=str(e))

    def detect_document_text(
        self,
        request: VisionImageRequest,
        language_hints: Optional[list] = None,
    ) -> ImageTextResponse:
        """
        Detect dense document text using Google Cloud Vision DOCUMENT_TEXT_DETECTION.
        """
        try:
            image = self._make_google_image(request)

            image_context = None
            if language_hints:
                image_context = vision_v1.ImageContext(
                    language_hints=language_hints
                )

            feature = vision_v1.Feature(
                type_=vision_v1.Feature.Type.DOCUMENT_TEXT_DETECTION,
            )

            req_kwargs = {"image": image, "features": [feature]}
            if image_context:
                req_kwargs["image_context"] = image_context

            response = self.client.annotate_image(request=req_kwargs)

            texts = [
                DetectedText.from_google_text(ann)
                for ann in response.text_annotations
            ]

            full_text = texts[0].text if texts else ""

            return ImageTextResponse(
                texts=texts[1:] if len(texts) > 1 else [],
                full_text=full_text,
                raw_response={"text_block_count": len(texts) - 1 if texts else 0},
            )
        except Exception as e:
            return ImageTextResponse(error=str(e))

    def score_image_safety(
        self,
        request: VisionImageRequest,
    ) -> ImageSafetyResponse:
        """
        Check image safety using Google Cloud Vision SafeSearch Detection.
        
        Uses vision_v1.Feature.Type.SAFE_SEARCH_DETECTION
        Categories: adult, spoof, medical, violence, racy
        """
        try:
            image = self._make_google_image(request)

            feature = vision_v1.Feature(
                type_=vision_v1.Feature.Type.SAFE_SEARCH_DETECTION,
            )

            response = self.client.annotate_image(
                request={"image": image, "features": [feature]}
            )

            safe_search = response.safe_search_annotation

            category_map = {
                "adult": safe_search.adult,
                "spoof": safe_search.spoof,
                "medical": safe_search.medical,
                "violence": safe_search.violence,
                "racy": safe_search.racy,
            }

            likelihood_name = {
                0: "UNKNOWN",
                1: "VERY_UNLIKELY",
                2: "UNLIKELY",
                3: "POSSIBLE",
                4: "LIKELY",
                5: "VERY_LIKELY",
            }

            ratings = []
            flagged = []
            for category, likelihood_val in category_map.items():
                lik_name = likelihood_name.get(likelihood_val, "UNKNOWN")
                rating = SafetyRating.from_google_safe_search(category, lik_name)
                ratings.append(rating)
                if rating.likelihood_score >= 0.5:
                    flagged.append(category)

            return ImageSafetyResponse(
                ratings=ratings,
                is_safe=len(flagged) == 0,
                flagged_categories=flagged,
                raw_response={"categories_checked": len(category_map)},
            )
        except Exception as e:
            return ImageSafetyResponse(error=str(e))


def create_vision_client(
    credentials_path: Optional[str] = None,
    project_id: Optional[str] = None,
    api_endpoint: Optional[str] = None,
) -> GoogleVisionClient:
    """Factory function to create a configured Google Vision client."""
    return GoogleVisionClient(
        credentials_path=credentials_path,
        project_id=project_id,
        api_endpoint=api_endpoint,
    )
