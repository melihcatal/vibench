import os
import json
from typing import List, Dict, Any, Optional
from messaging_models import MessageProcessingResult
import openai


def summarize_processing_results(results: List[MessageProcessingResult]) -> str:
    openai.api_key = os.getenv("OPENAI_API_KEY")
    if not openai.api_key:
        raise ValueError("OPENAI_API_KEY environment variable must be set")

    summary_data = []
    for result in results:
        summary_data.append(
            {
                "message_id": result.message_id,
                "success": result.success,
                "processing_time_ms": result.processing_time_ms,
                "summary": result.summary,
            }
        )

    prompt = f"""
    Analyze these message processing results and provide a concise summary:
    
    {json.dumps(summary_data, indent=2)}
    
    Please provide:
    1. Overall success rate
    2. Average processing time
    3. Key patterns or issues observed
    4. Recommendations for improvement
    
    Keep the summary under 200 words.
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that summarizes message processing results.",
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=300,
            temperature=0.3,
        )

        summary = response.choices[0].message.content.strip()
        return summary

    except Exception as e:
        raise Exception(f"Failed to generate summary with OpenAI: {e}")


def summarize_message_batch(messages: List[Dict[str, Any]]) -> str:
    openai.api_key = os.getenv("OPENAI_API_KEY")
    if not openai.api_key:
        raise ValueError("OPENAI_API_KEY environment variable must be set")

    message_contents = []
    for msg in messages:
        if isinstance(msg, dict) and "data" in msg:
            content = json.dumps(msg["data"], ensure_ascii=False)
            message_contents.append(content[:500])

    prompt = f"""
    Summarize the key themes and patterns in these messages:
    
    {json.dumps(message_contents, indent=2)}
    
    Provide a concise summary (under 150 words) of what these messages are about.
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that summarizes message content.",
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=200,
            temperature=0.2,
        )

        summary = response.choices[0].message.content.strip()
        return summary

    except Exception as e:
        raise Exception(f"Failed to summarize messages with OpenAI GPT-4: {e}")


def generate_processing_insights(
    results: List[MessageProcessingResult],
) -> Dict[str, Any]:
    openai.api_key = os.getenv("OPENAI_API_KEY")
    if not openai.api_key:
        raise ValueError("OPENAI_API_KEY environment variable must be set")

    success_count = sum(1 for r in results if r.success)
    failure_count = len(results) - success_count
    avg_time = (
        sum(r.processing_time_ms for r in results) / len(results) if results else 0
    )

    prompt = f"""
    Based on these processing results, generate insights:
    
    Total messages: {len(results)}
    Successful: {success_count}
    Failed: {failure_count}
    Average processing time: {avg_time:.2f}ms
    
    Individual results:
    {json.dumps([r.to_dict() for r in results], indent=2)}
    
    Provide insights in JSON format with these keys:
    - "success_rate_percentage"
    - "performance_rating" (good/average/poor)
    - "common_issues" (list)
    - "recommendations" (list)
    - "estimated_improvement_potential"
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a data analyst that provides JSON-formatted insights.",
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=400,
            temperature=0.1,
        )

        insights_text = response.choices[0].message.content.strip()

        try:
            insights = json.loads(insights_text)
        except json.JSONDecodeError:
            insights = {"raw_insights": insights_text}

        return insights

    except Exception as e:
        raise Exception(f"Failed to generate insights with OpenAI: {e}")


if __name__ == "__main__":
    sample_results = [
        MessageProcessingResult(
            message_id="msg_001",
            success=True,
            processing_time_ms=125.5,
            summary="User registration processed successfully",
        ),
        MessageProcessingResult(
            message_id="msg_002",
            success=False,
            processing_time_ms=45.2,
            summary="Invalid email format",
        ),
        MessageProcessingResult(
            message_id="msg_003",
            success=True,
            processing_time_ms=89.7,
            summary="Purchase order validated",
        ),
    ]

    try:
        summary = summarize_processing_results(sample_results)
        print("Summary:")
        print(summary)

        insights = generate_processing_insights(sample_results)
        print("\nInsights:")
        print(json.dumps(insights, indent=2))

    except Exception as e:
        print(f"Error: {e}")
