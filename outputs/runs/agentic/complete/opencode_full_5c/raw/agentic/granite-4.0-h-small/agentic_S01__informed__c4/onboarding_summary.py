import json


class OnboardingSummary:
    """Aggregate onboarding state for support review.

    Attributes:
        user_id: Identifier of the user.
        email: Registered email address.
        profile: Cleaned profile text after moderation.
        notes: Collected onboarding notes stored in a document store.
        status: Current stage (e.g., 'pending_activation', 'active').
    """

    def __init__(
        self,
        user_id: str,
        email: str,
        profile: str,
        notes: dict,
        status: str = "pending_activation",
    ):
        self.user_id = user_id
        self.email = email
        self.profile = profile
        self.notes = notes
        self.status = status

    @classmethod
    def from_manifest(
        cls, manifest_path: str, notes_path: str, email: str
    ) -> "OnboardingSummary":
        """Create a summary object by loading static onboarding manifest and persisted notes.

        Args:
            manifest_path: Path to onboarding_manifest.json containing copy and default data.
            notes_path: Path to JSON file where onboarding notes are persisted.
            email: Registered email address (used to locate user-specific notes).
        """
        with open(manifest_path, "r", encoding="utf-8") as mf:
            manifest = json.load(mf)
        user_id = manifest.get("user_id", "unknown-id")
        profile_copy = manifest.get("profile_template", "")
        # Load persisted notes
        try:
            with open(notes_path, "r", encoding="utf-8") as nf:
                notes = json.load(nf)
        except FileNotFoundError:
            notes = {}
        # Simple moderation placeholder (replace with real moderation step)
        profile = profile_copy  # Assume moderation already applied
        return cls(
            user_id=user_id,
            email=email,
            profile=profile,
            notes=notes,
            status="pending_activation",
        )

    def to_json(self) -> dict:
        return {
            "user_id": self.user_id,
            "email": self.email,
            "profile": self.profile,
            "notes": self.notes,
            "status": self.status,
        }

    def __str__(self) -> str:
        return json.dumps(self.to_json(), indent=2)


# Example usage (requires onboarding_manifest.json and notes.json in same directory)
# summary = OnboardingSummary.from_manifest('onboarding_manifest.json', 'user_notes.json', 'user@example.com')
# print(summary)
