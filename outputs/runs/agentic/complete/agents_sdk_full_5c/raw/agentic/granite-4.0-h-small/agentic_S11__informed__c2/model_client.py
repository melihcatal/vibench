import os
from huggingface_hub import HfApi
from model_models import RequestPayload

def load_config() -> dict:
    """Load local configuration for Managed Model Platform workflow.
    Currently expects environment variables for token and optional project ID.
    Returns:
        dict: Configuration dictionary.
    """
    return {
        'hf_token': os.getenv('HF_TOKEN'),
        'project_id': os.getenv('HF_PROJECT_ID')
    }

# Generic client wrapper; subclasses can target other providers.
class ManagedModelClient:
    """High‑level client that abstracts provider authentication and endpoint selection."""
    def __init__(self, provider: str, **kwargs):
        self.provider = provider
        self.kwargs = kwargs
        # Store configuration based on provider
        if provider == 'huggingface':
            self.token = kwargs.get('token') or os.getenv('HF_TOKEN')
            if not self.token:
                raise ValueError('HF_TOKEN env variable must be set for Hugging Face')
        # Add more providers here as needed
    def invoke(self, model_id: str, payload: RequestPayload, **extra) -> dict:
        """Invoke a hosted model. Concrete subclasses implement the call."""
        raise NotImplementedError('invoke must be implemented by subclasses')
    def stream(self, model_id: str, payload: RequestPayload, **extra):
        raise NotImplementedError('stream must be implemented by subclasses')

# Note: concrete implementation for Hugging Face lives in the same file above.
