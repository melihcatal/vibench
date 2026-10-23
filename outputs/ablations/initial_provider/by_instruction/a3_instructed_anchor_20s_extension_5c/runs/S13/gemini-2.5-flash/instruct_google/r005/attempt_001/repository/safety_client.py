import os
import google.generativeai as genai
from typing import List, Dict, Any
from safety_models import ModerationRequest, ModerationResponse, SafetyRating, SafetyAttribute

class SafetyClient:
    def __init__(self):
        api_key = os.environ.get("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable not set.")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash') # Using a concrete model

    def moderate_text(self, request: ModerationRequest) -> ModerationResponse:
        return self.moderate_batch_text([request])[0]

    def moderate_batch_text(self, requests: List[ModerationRequest]) -> List[ModerationResponse]:
        texts = [req.text_content for req in requests]
        responses = []
        for text_content in texts:
            response = self.model.generate_content(
                text_content,
                safety_settings=[
                    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
                ]
            )

            safety_attributes = []
            blocked = False
            if response.prompt_feedback and response.prompt_feedback.safety_ratings:
                ratings = []
                for rating in response.prompt_feedback.safety_ratings:
                    ratings.append(SafetyRating(
                        category=rating.category.name,
                        probability=rating.probability.name,
                        probability_score=0.0 # Google's API doesn't directly provide a score here
                    ))
                    if rating.probability.name != "NEGLIGIBLE" and rating.probability.name != "UNLIKELY":
                        blocked = True
                safety_attributes.append(SafetyAttribute(
                    text_content=text_content,
                    categories=ratings,
                    blocked=blocked
                ))

            responses.append(ModerationResponse(
                id="", # The Google API doesn't provide an ID for the moderation request directly
                model='gemini-1.5-flash',
                results=safety_attributes
            ))        
        return responses

        response = self.model.generate_content(
            request.text_content,
            safety_settings=[
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
            ]
        )

        safety_attributes = []
        blocked = False
        if response.prompt_feedback and response.prompt_feedback.safety_ratings:
            ratings = []
            for rating in response.prompt_feedback.safety_ratings:
                ratings.append(SafetyRating(
                    category=rating.category.name,
                    probability=rating.probability.name,
                    probability_score=0.0 # Google's API doesn't directly provide a score here
                ))
                if rating.probability.name != "NEGLIGIBLE" and rating.probability.name != "UNLIKELY":
                    blocked = True
            safety_attributes.append(SafetyAttribute(
                text_content=request.text_content,
                categories=ratings,
                blocked=blocked
            ))

        return ModerationResponse(
            id="", # The Google API doesn't provide an ID for the moderation request directly
            model='gemini-1.5-flash',
            results=safety_attributes
        )
