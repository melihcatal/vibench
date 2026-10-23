import os
import dashscope
import mistralai
import anthropic
import google.genai as genai
import boto3
import openai
import ibm_watsonx_ai

# Helper to choose provider based on environment variables
PROVIDER = os.getenv("LLM_PROVIDER", "dashscope")

if PROVIDER == "dashscope":
    DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")

    def get_chat_client():
        return dashscope.ChatCompletion(
            api_key=DASHSCOPE_API_KEY, model="qwen-72b-chat"
        )
else:
    raise NotImplementedError("Only DashScope provider implemented for model_client")
