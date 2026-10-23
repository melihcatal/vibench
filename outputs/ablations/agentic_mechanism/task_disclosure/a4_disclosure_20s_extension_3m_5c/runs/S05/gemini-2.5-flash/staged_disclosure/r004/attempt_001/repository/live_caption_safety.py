from google.cloud import aiplatform_v1 as aiplatform
from google.protobuf import json_format
from google.oauth2 import service_account
import os

def check_safety(transcript_text: str) -> dict:
    """
    Checks live transcript text for unsafe content using Google Cloud's Generative AI safety attributes.

    Args:
        transcript_text: The text from the live transcript to be checked.

    Returns:
        A dictionary containing the safety analysis results.
    """
    
    # Initialize the AI Platform client
    # It is recommended to set GOOGLE_APPLICATION_CREDENTIALS environment variable
    # to the path of your service account key file for authentication.
    client_options = {"api_endpoint": "us-central1-aiplatform.googleapis.com"}
    client = aiplatform.PredictionServiceClient(client_options=client_options)

    # The model name for text-bison (a generative AI model with safety features)
    # This example uses a hypothetical model name and requires a deployed model
    # with safety attribute capabilities.
    # In a real-world scenario, you would use a deployed model endpoint.
    # For content moderation specifically, you might use a dedicated content safety API if available,
    # or a generative model with safety attributes.
    endpoint = client.endpoint_path(
        project=os.getenv("GOOGLE_CLOUD_PROJECT"), 
        location="us-central1", 
        endpoint="YOUR_GENERATIVE_MODEL_ENDPOINT_ID" # Replace with your actual endpoint ID
    )

    instance = aiplatform.Value(string_value=transcript_text)
    instances = [instance]
    
    # The parameters for the prediction. This might vary based on your model deployment.
    # For safety attributes, you would typically configure the model to return them.
    parameters = aiplatform.Value(json_format.ParseDict({}, aiplatform.Value()._pb))

    try:
        response = client.predict(endpoint=endpoint, instances=instances, parameters=parameters)
        # Assuming the response contains safety attributes in its predictions.
        # The exact structure depends on the model output.
        # This is a placeholder for how you might extract safety information.
        
        safety_results = []
        for prediction in response.predictions:
            # Example: Extracting safety scores or categories
            # This part needs to be adapted based on the actual model output structure.
            # print(f"Prediction: {prediction}") # For debugging
            # If your model returns a structured output for safety, parse it here.
            safety_results.append(json_format.MessageToDict(prediction))
        
        return {"status": "success", "safety_analysis": safety_results}

    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    # Example Usage:
    # Set the GOOGLE_CLOUD_PROJECT environment variable
    # export GOOGLE_CLOUD_PROJECT="your-gcp-project-id"
    # Set the GOOGLE_APPLICATION_CREDENTIALS environment variable
    # export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/service-account-key.json"
    
    # You also need to deploy a Generative AI model with safety attribute capabilities
    # and replace "YOUR_GENERATIVE_MODEL_ENDPOINT_ID" with your actual endpoint ID.

    test_text_safe = "Hello, this is a safe and positive message."
    test_text_unsafe = "I will harm you." # Example of potentially unsafe content

    print(f"Checking text: '{test_text_safe}'")
    result_safe = check_safety(test_text_safe)
    print(f"Safety analysis for safe text: {result_safe}")

    print(f"
Checking text: '{test_text_unsafe}'")
    result_unsafe = check_safety(test_text_unsafe)
    print(f"Safety analysis for unsafe text: {result_unsafe}")
