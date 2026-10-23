import json


class Model:
    """Dataclass‑like container for provider model specifications.

    Attributes reflect the fields understood by ManagedModelClient.invoke.
    """

    def __init__(self, model_id: str, provider: str, deployment: str | None = None):
        self.model_id = (
            model_id  # identifier used by the provider (e.g., deployment name)
        )
        self.provider = provider  # e.g. "Azure OpenAI Service"
        self.deployment = deployment  # optional explicit deployment mapping

    @classmethod
    def from_dict(cls, data: dict) -> "Model":
        """Create a Model instance from a dictionary of configuration values.

        Expected keys: model_id, provider, deployment (optional).
        """
        return cls(
            model_id=data["model_id"],
            provider=data["provider"],
            deployment=data.get("deployment"),
        )

    def __repr__(self) -> str:
        return f"Model({self.provider}, model_id={self.model_id!r}, deployment={self.deployment!r})"


class Deployment:
    """Represents an inference profile or scoped deployment on the platform.

    Contains a mapping from logical model name to concrete deployment ID.
    """

    def __init__(self, name: str, models: dict):
        self.name = name  # human‑readable name (e.g., "default")
        self.models = models  # dict[model_id] => deployment_id

    @classmethod
    def from_dict(cls, data: dict) -> "Deployment":
        """Deserialize from a dict of {model_id: deployment_id} pairs.

        Example input: {"gpt-35-turbo": "default"}
        """
        return cls(
            name=data["name"], models={k: v for k, v in data.get("models", {}).items()}
        )

    def resolve(self, logical_model: str) -> str | None:
        """Return the concrete deployment ID for a logical model name.

        Returns None if the logical model is not mapped.
        """
        return self.models.get(logical_model)


class ModelCatalog:
    """Simple in‑memory catalog of model resources for a project.

    In a real system this would load from a database or configuration service.
    """

    def __init__(self, project_id: str):
        # Example static data – replace with loader from environment / file if needed
        self.project_id = project_id
        self.deployments: dict[str, Deployment] = {
            "default": Deployment(
                name="default",
                models={
                    "gpt-35-turbo": "default-gpt35",
                    "gpt-4": "default-gpt4",
                },
            ),
            "experimental": Deployment(
                name="exp",
                models={"gpt-4o-mini": "exp-gpt4o-mini"},
            ),
        }

    def get_deployment(self, name: str) -> Deployment | None:
        return self.deployments.get(name)
