import requests
import os
import json
from typing import Dict, Any, List, Optional
import queue
import threading


class LiveCaptionSafetyChecker:
    def __init__(self):
        self.api_key = os.getenv("PERSPECTIVE_API_KEY")
        if not self.api_key:
            raise ValueError("PERSPECTIVE_API_KEY environment variable must be set")

        self.api_url = (
            "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
        )
        self.safety_queue = queue.Queue()
        self.result_queue = queue.Queue()
        self.is_checking = False

        self.attributes = {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {},
            "SEXUALLY_EXPLICIT": {},
            "FLIRTATION": {},
        }

    def analyze_text(self, text: str) -> Dict[str, Any]:
        if not text or not text.strip():
            return {"error": "Empty text"}

        request_data = {
            "comment": {"text": text},
            "languages": ["en"],
            "requestedAttributes": self.attributes,
            "doNotStore": True,
        }

        try:
            response = requests.post(
                f"{self.api_url}?key={self.api_key}",
                json=request_data,
                headers={"Content-Type": "application/json"},
            )
            response.raise_for_status()

            result = response.json()
            return self._process_analysis_result(result, text)
        except requests.exceptions.RequestException as e:
            return {"error": f"API request failed: {str(e)}", "text": text}
        except json.JSONDecodeError as e:
            return {"error": f"JSON decode failed: {str(e)}", "text": text}

    def _process_analysis_result(
        self, result: Dict[str, Any], original_text: str
    ) -> Dict[str, Any]:
        attribute_scores = {}
        summary_scores = {}

        if "attributeScores" in result:
            for attr_name, attr_data in result["attributeScores"].items():
                if "summaryScore" in attr_data:
                    score = attr_data["summaryScore"]["value"]
                    attribute_scores[attr_name] = score

                    if score > 0.7:
                        summary_scores[attr_name] = {"score": score, "level": "HIGH"}
                    elif score > 0.4:
                        summary_scores[attr_name] = {"score": score, "level": "MEDIUM"}
                    else:
                        summary_scores[attr_name] = {"score": score, "level": "LOW"}

        has_issues = any(score > 0.7 for score in attribute_scores.values())
        highest_risk = max(attribute_scores.values()) if attribute_scores else 0
        highest_risk_attribute = (
            max(attribute_scores, key=attribute_scores.get)
            if attribute_scores
            else None
        )

        return {
            "text": original_text,
            "attribute_scores": attribute_scores,
            "summary_scores": summary_scores,
            "has_safety_issues": has_issues,
            "highest_risk_score": highest_risk,
            "highest_risk_attribute": highest_risk_attribute,
            "should_flag": has_issues,
            "raw_result": result,
        }

    def check_caption_safety(self, caption: Dict[str, Any]) -> Dict[str, Any]:
        text = caption.get("text", "")
        is_final = caption.get("is_final", False)

        safety_result = self.analyze_text(text)

        return {
            "caption": caption,
            "safety_analysis": safety_result,
            "is_final": is_final,
            "timestamp": caption.get("timestamp"),
            "recommendation": "FLAG"
            if safety_result.get("should_flag", False)
            else "OK",
        }

    def start_safety_stream(self):
        self.is_checking = True

        def safety_worker():
            while self.is_checking:
                try:
                    caption = self.safety_queue.get(timeout=0.1)
                    safety_check = self.check_caption_safety(caption)
                    self.result_queue.put(safety_check)
                except queue.Empty:
                    continue
                except Exception as e:
                    self.result_queue.put({"error": str(e), "caption": caption})

        self.worker_thread = threading.Thread(target=safety_worker)
        self.worker_thread.daemon = True
        self.worker_thread.start()

    def stop_safety_stream(self):
        self.is_checking = False
        if self.worker_thread:
            self.worker_thread.join(timeout=1)

    def add_caption_for_safety_check(self, caption: Dict[str, Any]):
        self.safety_queue.put(caption)

    def get_safety_results(self):
        while True:
            try:
                yield self.result_queue.get(timeout=0.1)
            except queue.Empty:
                if not self.is_checking:
                    break
                continue

    def configure_attributes(self, attributes: List[str]):
        self.attributes = {
            attr: {}
            for attr in attributes
            if attr
            in [
                "TOXICITY",
                "SEVERE_TOXICITY",
                "IDENTITY_ATTACK",
                "INSULT",
                "PROFANITY",
                "THREAT",
                "SEXUALLY_EXPLICIT",
                "FLIRTATION",
            ]
        }

    def get_safety_summary(self, captions: List[Dict[str, Any]]) -> Dict[str, Any]:
        flagged_count = 0
        total_risk_score = 0
        risk_by_attribute = {}

        for caption in captions:
            safety_check = self.check_caption_safety(caption)
            if safety_check["recommendation"] == "FLAG":
                flagged_count += 1

            analysis = safety_check["safety_analysis"]
            if "attribute_scores" in analysis:
                for attr, score in analysis["attribute_scores"].items():
                    if attr not in risk_by_attribute:
                        risk_by_attribute[attr] = []
                    risk_by_attribute[attr].append(score)
                    total_risk_score += score

        avg_risk = total_risk_score / len(captions) if captions else 0

        return {
            "total_captions": len(captions),
            "flagged_captions": flagged_count,
            "flag_percentage": (flagged_count / len(captions)) * 100 if captions else 0,
            "average_risk_score": avg_risk,
            "risk_by_attribute": {
                attr: sum(scores) / len(scores)
                for attr, scores in risk_by_attribute.items()
            },
            "overall_safety": "SAFE"
            if avg_risk < 0.3
            else "MODERATE"
            if avg_risk < 0.6
            else "UNSAFE",
        }

    def filter_unsafe_captions(
        self, captions: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        safe_captions = []
        unsafe_captions = []

        for caption in captions:
            safety_check = self.check_caption_safety(caption)
            if safety_check["recommendation"] == "OK":
                safe_captions.append(caption)
            else:
                unsafe_captions.append(
                    {
                        "caption": caption,
                        "reason": safety_check["safety_analysis"].get(
                            "highest_risk_attribute"
                        ),
                        "risk_score": safety_check["safety_analysis"].get(
                            "highest_risk_score"
                        ),
                    }
                )

        return safe_captions, unsafe_captions
