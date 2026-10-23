import boto3
import os
import json
from model_models import BedrockRequest, BedrockResponse, BedrockStreamCompletionResponse, EmbeddingsRequest, EmbeddingsResponse, TranslateRequest, TranslateResponse, SynthesizeSpeechRequest

class BedrockModelClient:
    def __init__(self, region_name=None, model_id="amazon.titan-text-express-v1"):
        self.region_name = region_name or os.environ.get("AWS_REGION", "us-east-1")
        self.bedrock_runtime_client = boto3.client("bedrock-runtime", region_name=self.region_name)
        self.translate_client = boto3.client("translate", region_name=self.region_name)
        self.comprehend_client = boto3.client("comprehend", region_name=self.region_name)
        self.polly_client = boto3.client("polly", region_name=self.region_name)
        self.model_id = model_id

    def _invoke_model(self, request_body: dict, model_id: str, content_type="application/json", accept="application/json"):
        response = self.bedrock_runtime_client.invoke_model(
            body=json.dumps(request_body),
            modelId=model_id,
            contentType=content_type,
            accept=accept
        )
        response_body = json.loads(response['body'].read())
        return response_body

    def _invoke_model_with_response_stream(self, request_body: dict, model_id: str, content_type="application/json", accept="application/json"):
        response = self.bedrock_runtime_client.invoke_model_with_response_stream(
            body=json.dumps(request_body),
            modelId=model_id,
            contentType=content_type,
            accept=accept
        )
        return response['body']

    def invoke_llm(self, messages: list, system_prompts: list = None, inference_config: dict = None, model_id: str = None) -> BedrockResponse:
        model_to_use = model_id if model_id else self.model_id
        request = {
            "modelId": model_to_use,
            "messages": messages,
            "inferenceConfig": inference_config if inference_config else {"maxTokens": 2048, "temperature": 0.7, "topP": 0.9},
        }
        if system_prompts:
            request["systemPrompts"] = system_prompts

        response_body = self._invoke_model(request_body=request, model_id=model_to_use)

        # Parse the response based on the model. This is a simplified example for Titan Text Express
        # Actual parsing might need to be more robust depending on the specific model's output structure
        output_text = ""
        for message_content in response_body.get("output", {}).get("message", {}).get("content", []):
            if "text" in message_content:
                output_text += message_content["text"]

        return BedrockResponse(output={"message": {"content": [{"text": output_text}]}})

    def invoke_llm_stream(self, messages: list, system_prompts: list = None, inference_config: dict = None, model_id: str = None):
        model_to_use = model_id if model_id else self.model_id
        request = {
            "modelId": model_to_use,
            "messages": messages,
            "inferenceConfig": inference_config if inference_config else {"maxTokens": 2048, "temperature": 0.7, "topP": 0.9},
        }
        if system_prompts:
            request["systemPrompts"] = system_prompts

        response_stream = self._invoke_model_with_response_stream(request_body=request, model_id=model_to_use)
        for event in response_stream:
            if 'chunk' in event:
                yield BedrockStreamCompletionResponse(chunk=event['chunk'])

    def get_embeddings(self, request: EmbeddingsRequest, model_id: str = "amazon.titan-embed-text-v1") -> EmbeddingsResponse:
        body = json.dumps({"inputText": request.inputText})
        response = self.bedrock_runtime_client.invoke_model(
            body=body,
            modelId=model_id,
            contentType="application/json",
            accept="application/json"
        )
        response_body = json.loads(response['body'].read())
        return EmbeddingsResponse(embedding=response_body["embedding"])

    def translate_text(self, request: TranslateRequest) -> TranslateResponse:
        response = self.translate_client.translate_text(
            Text=request.text,
            SourceLanguageCode=request.source_language_code,
            TargetLanguageCode=request.target_language_code
        )
        return TranslateResponse(translated_text=response['TranslatedText'])
    
    def detect_pii(self, text: str, language_code: str = "en"):
        response = self.comprehend_client.detect_pii_entities(
            Text=text,
            LanguageCode=language_code
        )
        return response['Entities']

    def synthesize_speech(self, request: SynthesizeSpeechRequest):
        response = self.polly_client.synthesize_speech(
            Text=request.text,
            OutputFormat=request.output_format,
            VoiceId=request.voice_id
        )
        return response['AudioStream']
