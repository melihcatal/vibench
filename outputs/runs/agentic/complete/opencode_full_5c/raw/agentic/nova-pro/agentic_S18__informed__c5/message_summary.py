import boto3

# Create a Bedrock client
bedrock = boto3.client("bedrock-runtime")

# Define the model ID
model_id = "amazon.titan-text-express-v1"

# Define the prompt
prompt = "Summarize the following text:..."

# Invoke the model
response = bedrock.invoke_model(modelId=model_id, body={"inputText": prompt})

# Print the summary
print(response["outputText"])
