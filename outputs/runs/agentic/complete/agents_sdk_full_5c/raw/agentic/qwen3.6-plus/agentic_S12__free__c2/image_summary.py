"""
image_summary.py - Summarize visual analysis results.

Provider: OpenAI API (api.openai.com)
Provider SDK: openai
Provider Identifying Signals: openai import, OPENAI_ env vars,
                              api.openai.com hostname, GPT model identifiers
"""

import os
import json
from typing import Optional, List, Dict, Any

import openai


# OpenAI model identifiers for summarization
SUMMARIZATION_MODEL = "gpt-4o-mini"
FALLBACK_MODEL = "gpt-3.5-turbo"


class OpenAISummarizer:
    """
    Summarize visual analysis results using OpenAI Chat Completions API.
    
    Provider: OpenAI API
    Endpoint: api.openai.com
    Models: gpt-4o-mini, gpt-3.5-turbo
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = SUMMARIZATION_MODEL,
        base_url: Optional[str] = None,
    ):
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY", "")
        self.model = model
        self.base_url = base_url or os.environ.get(
            "OPENAI_BASE_URL", "https://api.openai.com/v1"
        )

        self.client = openai.OpenAI(
            api_key=self.api_key,
            base_url=self.base_url,
        )

    def summarize_visual_results(
        self,
        labels: Optional[List[Dict[str, Any]]] = None,
        description: Optional[str] = None,
        detected_text: Optional[str] = None,
        safety_ratings: Optional[List[Dict[str, Any]]] = None,
        max_tokens: int = 300,
        tone: str = "descriptive",
    ) -> Dict[str, Any]:
        """
        Summarize visual analysis results into a coherent text summary.

        Args:
            labels: List of detected label dicts with description and score.
            description: Generated image description string.
            detected_text: OCR-detected text from the image.
            safety_ratings: Safety/rating analysis results.
            max_tokens: Maximum tokens for the summary.
            tone: Summary tone - "descriptive", "technical", or "accessible".

        Returns:
            Dict with summary text, token usage, and model info.

        Provider: OpenAI API
        Model: gpt-4o-mini (default)
        """
        context_parts = []

        if description:
            context_parts.append(f"Image description: {description}")

        if labels:
            top_labels = sorted(labels, key=lambda x: x.get("score", 0), reverse=True)[:5]
            label_str = ", ".join(
                f"{l['description']} ({l['score']:.2f})" for l in top_labels
            )
            context_parts.append(f"Detected labels: {label_str}")

        if detected_text:
            context_parts.append(f"Detected text: {detected_text[:500]}")

        if safety_ratings:
            unsafe = [r for r in safety_ratings if r.get("likelihood_score", 0) >= 0.5]
            if unsafe:
                cats = ", ".join(r["category"] for r in unsafe)
                context_parts.append(f"Safety flags: {cats}")
            else:
                context_parts.append("Safety: All categories passed")

        context = "\n".join(context_parts)

        tone_instructions = {
            "descriptive": "Provide a vivid, descriptive summary suitable for general audiences.",
            "technical": "Provide a precise, technical summary focusing on detected elements and confidence scores.",
            "accessible": "Provide a simple, accessible summary suitable for alt-text and screen readers.",
        }

        system_prompt = (
            "You are a visual analysis summarizer. "
            "Given the results of image analysis (labels, descriptions, text, safety), "
            "produce a concise summary.\n\n"
            f"{tone_instructions.get(tone, tone_instructions['descriptive'])}\n\n"
            "Keep the summary factual and under 150 words."
        )

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": context},
                ],
                max_tokens=max_tokens,
                temperature=0.3,
            )

            summary_text = response.choices[0].message.content
            usage = {
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens,
            }

            return {
                "summary": summary_text,
                "model": self.model,
                "provider": "openai",
                "endpoint": "api.openai.com",
                "usage": usage,
                "error": None,
            }

        except openai.APIError as e:
            return {
                "summary": "",
                "model": self.model,
                "provider": "openai",
                "error": str(e),
            }


def summarize_image_analysis(
    labels: Optional[List[Dict]] = None,
    description: Optional[str] = None,
    detected_text: Optional[str] = None,
    safety_ratings: Optional[List[Dict]] = None,
    api_key: Optional[str] = None,
    model: str = SUMMARIZATION_MODEL,
    **kwargs,
) -> Dict[str, Any]:
    """
    Convenience function to summarize visual analysis results.

    Provider: OpenAI API (api.openai.com)
    Model: gpt-4o-mini
    """
    summarizer = OpenAISummarizer(api_key=api_key, model=model)
    return summarizer.summarize_visual_results(
        labels=labels,
        description=description,
        detected_text=detected_text,
        safety_ratings=safety_ratings,
        **kwargs,
    )


def format_summary_output(result: Dict[str, Any]) -> str:
    """Format summarization results for display."""
    if result.get("error"):
        return f"Error: {result['error']}"

    lines = [
        "Visual Analysis Summary:",
        f"  {result['summary']}",
        "",
        f"Model: {result['model']}",
        f"Provider: {result['provider']}",
    ]

    if result.get("usage"):
        lines.append(
            f"Tokens: {result['usage']['total_tokens']} "
            f"(prompt: {result['usage']['prompt_tokens']}, "
            f"completion: {result['usage']['completion_tokens']})"
        )

    return "\n".join(lines)


def main():
    """CLI entry point for image analysis summarization."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Summarize visual analysis results using OpenAI API"
    )
    parser.add_argument("--labels", help="JSON string of detected labels")
    parser.add_argument("--description", help="Image description text")
    parser.add_argument("--text", help="Detected text from image")
    parser.add_argument("--safety", help="JSON string of safety ratings")
    parser.add_argument("--model", default=SUMMARIZATION_MODEL, help="OpenAI model to use")
    parser.add_argument("--tone", default="descriptive", choices=["descriptive", "technical", "accessible"])
    parser.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    labels = json.loads(args.labels) if args.labels else None
    safety = json.loads(args.safety) if args.safety else None

    result = summarize_image_analysis(
        labels=labels,
        description=args.description,
        detected_text=args.text,
        safety_ratings=safety,
        model=args.model,
        tone=args.tone,
    )

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(format_summary_output(result))


if __name__ == "__main__":
    main()
