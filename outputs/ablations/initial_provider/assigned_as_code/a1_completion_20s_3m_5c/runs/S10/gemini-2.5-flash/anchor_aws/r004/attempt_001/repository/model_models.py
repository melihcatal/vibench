from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class BedrockInputMessage(BaseModel):
    content: List[Dict[str, Any]]

class BedrockRequest(BaseModel):
    modelId: str
    messages: List[BedrockInputMessage]
    inferenceConfig: Optional[Dict[str, Any]] = None
    systemPrompts: Optional[List[Dict[str, Any]]] = None

class BedrockOutputContent(BaseModel):
    text: Optional[str] = None
    stopReason: Optional[str] = None

class BedrockOutputMessage(BaseModel):
    content: List[BedrockOutputContent]

class BedrockResponse(BaseModel):
    output: BedrockOutputMessage
    stopReason: Optional[str] = None
    usage: Optional[Dict[str, Any]] = None

class BedrockStreamCompletionResponse(BaseModel):
    chunk: Dict[str, Any] # This will hold the raw chunk data from the stream

class TextPayload(BaseModel):
    text: str

class JsonPayload(BaseModel):
    text: str
    json_schema: Dict[str, Any]

class QuestionContextPayload(BaseModel):
    question: str
    context: str

class EmbeddingsRequest(BaseModel):
    inputText: str

class EmbeddingsResponse(BaseModel):
    embedding: List[float]

class TranslateRequest(BaseModel):
    text: str
    source_language_code: str
    target_language_code: str

class TranslateResponse(BaseModel):
    translated_text: str

class SynthesizeSpeechRequest(BaseModel):
    text: str
    voice_id: str = "Joanna" # Default to Joanna
    output_format: str = "mp3"

class SynthesizeSpeechResponse(BaseMacommentdel):
    audio_stream: Any # Will be a botocore.response.StreamingBody
