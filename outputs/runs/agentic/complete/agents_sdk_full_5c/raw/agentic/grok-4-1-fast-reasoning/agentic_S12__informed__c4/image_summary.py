import argparse
import json
import os
from anthropic import Anthropic
from vision_models import AnalysisArtifacts

def image_summary(analysis_data: dict) -> str:
    client = Anthropic(api_key=os.environ['ANTHROPIC_API_KEY'])
    prompt = f"""Summarize the following image analysis results concisely:

Labels: {', '.join(analysis_data.get('labels', []))}
Description: {analysis_data.get('description', '')}
Texts: {', '.join(analysis_data.get('texts', [])[:10])}
Safety: {analysis_data.get('safety', {})}"""
    message = client.messages.create(
        model='claude-3-5-sonnet-20240620',
        max_tokens=200,
        temperature=0.3,
        messages=[{'role': 'user', 'content': prompt}]
    )
    return message.content[0].text

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Summarize image analysis using Anthropic Claude')
    parser.add_argument('analysis_json', help='Path to JSON file with analysis results')
    args = parser.parse_args()
    with open(args.analysis_json, 'r') as f:
        data = json.load(f)
    summary = image_summary(data)
    print(summary)