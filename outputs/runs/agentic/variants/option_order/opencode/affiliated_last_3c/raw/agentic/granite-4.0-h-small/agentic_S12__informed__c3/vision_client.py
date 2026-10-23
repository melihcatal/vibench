import base64

class VisionClient:
    """Local configuration and client helper utilities for Static Image and Visual Understanding.\n    \n    This helper centralizes provider configuration (credentials, endpoint, model) and provides\n    a unified interface for loading the appropriate provider SDK client.\n    """

    PROVIDERS = {
        "google_vision": {
            "module": "google.cloud.vision",
            "client_cls": "ImageAnnotatorClient",
            "env_var": "GOOGLE_APPLICATION_CREDENTIALS",
        },
        "clarifai": {
            "module": "clarifai.rest",
            "client_cls": "ClarifaiApp",
            "env_var": "CLARIFAI_PAT",
        },
        "aws_rekognition": {
            "module": "boto3",
            "client_cls": "client",
            "client_fn": "rekognition",
            "env_vars": ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY"],
        },
        "alibaba_vl": {
            "module": "dashscope",
            "client_cls": "vision",
            "env_var": "DASHSCOPE_API_KEY",
        },
        "azure_vision": {
            "module": "azure.ai.vision.imageanalysis",
            "client_cls": "ImageAnalysisClient",
            "env_vars": ["AZURE_VISION_ENDPOINT", "AZURE_VISION_KEY"],
        },
    }

    def __init__(self, provider: str, **config):
        """Instantiate the underlying SDK client for the chosen provider.\n        \n        Args:\n            provider (str): One of the keys in `PROVIDERS` (e.g., "google_vision").\n            **config: Additional configuration such as region, endpoint, etc.\n        """
        spec = self.PROVIDERS.get(provider)
        if not spec:
            raise ValueError(f"Unknown provider '{provider}'. Choose from {list(self.PROVIDERS)}")

        # Load credentials from environment\n        cred_env = spec.get("env_var")
        if cred_env:
            import os
            if not os.getenv(cred_env):
                raise RuntimeError(\n                    f"Environment variable '{cred_env}' not set for provider {provider}")
        cred_envs = spec.get("env_vars")
        if cred_envs:
            missing = [env for env in cred_envs if not os.getenv(env)]
            if missing:
                raise RuntimeError(\n                    f"Environment variables {missing} not set for provider {provider}")

        # Import provider module (lazy import to keep dependencies optional)\n        mod = __import__(spec["module"], fromlist=[spec.get("client_cls") or spec.get("client_fn")])
        if "client_fn" in spec:\n            # e.g., boto3.client('rekognition')\n            self.client = getattr(mod, spec["client_fn"])(**config)
        else:\n            # SDK classes are instantiated directly\n            cls = getattr(mod, spec["client_cls"])
            self.client = cls(**config)

    def __getattr__(self, attr):
        """Delegate attribute access to the wrapped client."""
        return getattr(self.client, attr)
