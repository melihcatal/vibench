from storage_client import get_comprehend_client
from storage_models import AssetMetadataEmbeddingRequest, AssetMetadataEmbeddingResponse
from botocore.exceptions import ClientError


def embed_asset_metadata_and_text(
    request: AssetMetadataEmbeddingRequest,
) -> AssetMetadataEmbeddingResponse:
    comprehend_client = get_comprehend_client()
    try:
        # AWS Comprehend does not offer direct text embedding models in the same way
        # that services like Amazon Bedrock or dedicated LLM APIs do.
        # For the purpose of providing a list of floats as an "embedding" within Comprehend,
        # we can use sentiment analysis results as a numerical representation.
        # The sentiment scores (Positive, Negative, Neutral, Mixed) can form a basic embedding.
        response = comprehend_client.detect_sentiment(
            Text=request.text_to_embed,
            LanguageCode="en",  # Assuming English for sentiment analysis for simplicity
        )

        sentiment_scores = response["SentimentScore"]
        embedding = [
            sentiment_scores["Positive"],
            sentiment_scores["Negative"],
            sentiment_scores["Neutral"],
            sentiment_scores["Mixed"],
        ]

        return AssetMetadataEmbeddingResponse(
            success=True,
            message="Text sentiment detected and used as a proxy for embedding",
            embedding=embedding,
            raw_response=response,
        )
    except ClientError as e:
        return AssetMetadataEmbeddingResponse(
            success=False, message=f"AWS Comprehend ClientError: {e}"
        )
    except Exception as e:
        return AssetMetadataEmbeddingResponse(
            success=False, message=f"An unexpected error occurred: {e}"
        )
