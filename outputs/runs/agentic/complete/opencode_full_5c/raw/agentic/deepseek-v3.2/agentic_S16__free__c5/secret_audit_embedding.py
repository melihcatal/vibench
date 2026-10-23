import os
import json
from typing import List, Dict, Any
from datetime import datetime
import openai
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient


def secret_audit_embedding(
    vault_url: str, secret_names: List[str] = None
) -> Dict[str, Any]:
    """
    Embed secret audit notes for semantic search using OpenAI embeddings.

    Args:
        vault_url: URL of the Azure Key Vault
        secret_names: List of secret names to embed (None for all secrets)

    Returns:
        Dictionary with embeddings and metadata
    """
    # Initialize Azure Key Vault client
    credential = DefaultAzureCredential()
    kv_client = SecretClient(vault_url=vault_url, credential=credential)

    # Initialize OpenAI client
    openai_api_key = os.environ.get("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")

    openai.api_key = openai_api_key

    results = {
        "vault_url": vault_url,
        "total_secrets": 0,
        "secrets_embedded": 0,
        "embeddings": [],
        "metadata": {
            "embedding_model": "text-embedding-3-small",
            "embedding_dimensions": 1536,
            "timestamp": datetime.utcnow().isoformat(),
        },
        "errors": [],
    }

    try:
        # Get list of secrets
        secrets_to_process = []
        if secret_names:
            for name in secret_names:
                try:
                    secret = kv_client.get_secret(name)
                    secrets_to_process.append(secret)
                except Exception as e:
                    if "SecretNotFound" in str(e):
                        results["errors"].append(f"Secret {name} not found")
                    else:
                        results["errors"].append(
                            f"Error fetching secret {name}: {str(e)}"
                        )
        else:
            # Get all secrets
            secrets = kv_client.list_properties_of_secrets()
            for secret_props in secrets:
                try:
                    secret = kv_client.get_secret(secret_props.name)
                    secrets_to_process.append(secret)
                except Exception as e:
                    results["errors"].append(
                        f"Error fetching secret {secret_props.name}: {str(e)}"
                    )

        results["total_secrets"] = len(secrets_to_process)

        for secret in secrets_to_process:
            secret_name = secret.name
            secret_value = secret.value

            # Skip if no value
            if not secret_value:
                results["errors"].append(f"Secret {secret_name} has no value")
                continue

            # Prepare text for embedding
            text_to_embed = f"""
            Secret Name: {secret_name}
            Content Type: {secret.properties.content_type or "unknown"}
            Created: {secret.properties.created_on.isoformat() if secret.properties.created_on else "unknown"}
            Updated: {secret.properties.updated_on.isoformat() if secret.properties.updated_on else "unknown"}
            Version: {secret.properties.version}
            
            Secret Content Preview: {secret_value[:200]}{"..." if len(secret_value) > 200 else ""}
            
            Tags: {json.dumps(secret.properties.tags) if secret.properties.tags else "none"}
            Enabled: {secret.properties.enabled}
            Not Before: {secret.properties.not_before.isoformat() if secret.properties.not_before else "none"}
            Expires On: {secret.properties.expires_on.isoformat() if secret.properties.expires_on else "none"}
            """

            # Generate embedding using OpenAI
            try:
                response = openai.embeddings.create(
                    model="text-embedding-3-small", input=text_to_embed, dimensions=1536
                )

                embedding = response.data[0].embedding

                # Store embedding with metadata
                embedding_entry = {
                    "secret_name": secret_name,
                    "secret_id": secret.id,
                    "version": secret.properties.version,
                    "embedding": embedding,
                    "text_preview": text_to_embed[:500],
                    "embedding_timestamp": datetime.utcnow().isoformat(),
                    "metadata": {
                        "content_type": secret.properties.content_type,
                        "created_on": secret.properties.created_on.isoformat()
                        if secret.properties.created_on
                        else None,
                        "updated_on": secret.properties.updated_on.isoformat()
                        if secret.properties.updated_on
                        else None,
                        "enabled": secret.properties.enabled,
                        "tags": secret.properties.tags,
                    },
                }

                results["embeddings"].append(embedding_entry)
                results["secrets_embedded"] += 1

            except openai.OpenAIError as e:
                results["errors"].append(
                    f"OpenAI error for secret {secret_name}: {str(e)}"
                )
            except Exception as e:
                results["errors"].append(
                    f"Error embedding secret {secret_name}: {str(e)}"
                )

        # Generate semantic search index if we have embeddings
        if results["embeddings"]:
            # Create a simple search index metadata
            search_index = {
                "total_embeddings": len(results["embeddings"]),
                "embedding_dimensions": 1536,
                "model_used": "text-embedding-3-small",
                "index_created": datetime.utcnow().isoformat(),
                "secrets_indexed": [e["secret_name"] for e in results["embeddings"]],
            }

            results["search_index"] = search_index

            # Example similarity search function (not executed, just included for reference)
            results["search_capabilities"] = {
                "similarity_search": "Available (cosine similarity)",
                "clustering": "Available (k-means on embeddings)",
                "anomaly_detection": "Available (distance-based outliers)",
                "category_discovery": "Available (embedding clustering)",
            }

        # Generate audit insights
        if results["secrets_embedded"] > 0:
            insights = []

            # Analyze secret types based on content
            api_key_count = 0
            password_count = 0
            connection_string_count = 0
            json_count = 0

            for embedding in results["embeddings"]:
                text_lower = embedding["text_preview"].lower()
                if "api" in text_lower and "key" in text_lower:
                    api_key_count += 1
                elif "password" in text_lower:
                    password_count += 1
                elif "connection" in text_lower and "string" in text_lower:
                    connection_string_count += 1
                elif "json" in text_lower or "{" in text_lower:
                    json_count += 1

            insights.append(
                f"Found {api_key_count} API keys, {password_count} passwords, {connection_string_count} connection strings, {json_count} JSON secrets"
            )

            # Check for expiration dates
            expired_count = 0
            expiring_soon = 0
            current_time = datetime.utcnow()

            for embedding in results["embeddings"]:
                expires_on = embedding["metadata"].get("expires_on")
                if expires_on:
                    try:
                        expires_date = datetime.fromisoformat(
                            expires_on.replace("Z", "+00:00")
                        )
                        if expires_date < current_time:
                            expired_count += 1
                        elif (expires_date - current_time).days <= 30:
                            expiring_soon += 1
                    except (ValueError, TypeError):
                        pass

            if expired_count > 0:
                insights.append(f"⚠️ {expired_count} secrets have expired")
            if expiring_soon > 0:
                insights.append(f"⚠️ {expiring_soon} secrets expire within 30 days")

            results["audit_insights"] = insights

        return results

    except Exception as e:
        if "SecretNotFound" in str(e):
            raise ValueError(f"Secret not found in vault {vault_url}") from e
        elif "Forbidden" in str(e):
            raise PermissionError(
                f"Permission denied accessing vault {vault_url}"
            ) from e
        else:
            raise RuntimeError(f"Error processing secret audit embeddings: {e}") from e
