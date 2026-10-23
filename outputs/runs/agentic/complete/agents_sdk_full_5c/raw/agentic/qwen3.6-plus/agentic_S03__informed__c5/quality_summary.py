"""
quality_summary.py - Summarize translation quality issues using OpenAI GPT via Chat Completions API.

Provider: OpenAI Chat Completions API
SDK: openai
Auth: OPENAI_API_KEY environment variable
Model: gpt-4o-mini
"""

import json
import os
from typing import Dict, List, Optional

from openai import OpenAI


def _build_quality_prompt(
    source_texts: List[str],
    translated_texts: List[str],
    source_lang: str,
    target_lang: str,
    issues: Optional[List[Dict[str, str]]] = None,
) -> str:
    """Build a prompt for the LLM to summarize translation quality issues."""
    pairs = []
    for i, (src, tgt) in enumerate(zip(source_texts, translated_texts)):
        pair_info = {"index": i, "source": src, "translation": tgt}
        if issues and i < len(issues):
            pair_info["noted_issues"] = issues[i]
        pairs.append(pair_info)

    prompt = (
        f"You are a professional translation quality analyst. "
        f"Review the following {source_lang} to {target_lang} translation pairs "
        f"and provide a concise quality summary.\n\n"
        f"Translation pairs:\n{json.dumps(pairs, ensure_ascii=False, indent=2)}\n\n"
        f"Provide your analysis as a JSON object with the following structure:\n"
        f'{{\n  "overall_quality_score": <integer 0-10>,\n'
        f'  "overall_assessment": "<brief summary>",\n'
        f'  "issues_found": [\n'
        f'    {{"category": "<issue category>", "severity": "low|medium|high", '
        f'"description": "<description>", "affected_indices": [<indices>]}}\n'
        f"  ],\n"
        f'  "recommendations": ["<recommendation>", ...]\n'
        f"}}\n\n"
        f"Focus on accuracy, fluency, tone consistency, cultural appropriateness, "
        f"and terminology consistency."
    )
    return prompt


def summarize_translation_quality(
    source_texts: List[str],
    translated_texts: List[str],
    source_lang: str,
    target_lang: str,
    issues: Optional[List[Dict[str, str]]] = None,
    model: str = "gpt-4o-mini",
) -> Dict:
    """
    Summarize translation quality issues using OpenAI's GPT model.

    Analyzes source and translated text pairs and produces a structured quality
    summary including an overall score, identified issues, and recommendations.

    Args:
        source_texts: List of original source language texts.
        translated_texts: List of corresponding translated texts.
        source_lang: Source language code (e.g., 'en', 'de').
        target_lang: Target language code (e.g., 'en', 'fr').
        issues: Optional list of pre-identified issues per translation pair.
        model: OpenAI model to use. Defaults to 'gpt-4o-mini'.

    Returns:
        Dict containing the structured quality summary from the LLM.

    Raises:
        ValueError: If source_texts and translated_texts lengths don't match.
        openai.OpenAIError: If the OpenAI API request fails.
    """
    if len(source_texts) != len(translated_texts):
        raise ValueError(
            "source_texts and translated_texts must have the same length."
        )

    api_key = os.environ.get("OPENAI_API_KEY", "")
    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY environment variable is required for OpenAI API access."
        )

    client = OpenAI(api_key=api_key)

    prompt = _build_quality_prompt(source_texts, translated_texts, source_lang, target_lang, issues)

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert translation quality analyst. "
                    "Respond only with valid JSON. Do not include any text outside the JSON object."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
        max_tokens=2000,
    )

    content = response.choices[0].message.content.strip()

    try:
        summary = json.loads(content)
    except json.JSONDecodeError:
        raise ValueError(
            f"Failed to parse LLM response as JSON. Raw response: {content}"
        )

    return summary
