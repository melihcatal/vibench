from identity_models import ModeratedClaim

def moderate_claim(raw_claim: str) -> ModeratedClaim:
    """
    Simple moderation rule: flag any claim containing the word 'secret'.
    Returns a ModeratedClaim with the original text and a reason if flagged,
    otherwise with moderated text set to the original.
    """
    if "secret" in raw_claim.lower():
        return ModeratedClaim(
            original=raw_claim,
            moderated=None,
            reason="Contains prohibited keyword 'secret'"
        )
    return ModeratedClaim(
        original=raw_claim,
        moderated=raw_claim,
        reason=None
    )

if __name__ == "__main__":
    test = "This is a test with secret information."
    mc = moderate_claim(test)
    print("Moderated:", mc.dict())
