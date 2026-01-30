import os
from dotenv import load_dotenv
import logging

load_dotenv()

# Feature toggle - keep AI feature ON by default for the project
USE_AI = os.getenv("USE_AI", "true").lower() == "true"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

logger = logging.getLogger(__name__)


def ai_available() -> bool:
    """Return True if the AI feature is enabled (real OpenAI or local mock will run)."""
    return USE_AI


def real_ai_available() -> bool:
    """Return True if real OpenAI is configured and can be used."""
    return bool(OPENAI_API_KEY)


def _explain_issue_locally(issue: str) -> str:
    """Return a deterministic, helpful explanation for a given audit issue.

    This is used as a local/mock AI so the feature can operate even without an
    OpenAI API key during development and demos.
    """
    # Simple rule-based explanations for common issues; keep them short and helpful.
    lower = issue.lower()
    if "negative tax" in lower:
        return (
            "The tax value is negative. Taxes should be non-negative, so this likely "
            "indicates a data entry or calculation error. Verify the tax source and "
            "ensure tax is being recorded as the correct positive amount."
        )
    if "commission exceeds fare" in lower:
        return (
            "The commission recorded is greater than the fare amount, which is unusual. "
            "Check for duplicated commission entries or incorrect commission calculation. "
            "Commissions are typically a percentage of the fare."
        )
    if "invalid fare" in lower:
        return (
            "The fare is zero or negative, which is invalid for completed trips. "
            "Confirm the fare calculation, pricing rules, and that the trip was billed correctly."
        )

    # Generic helpful fallback
    return f"Issue: {issue}. Please investigate the source data and business rules related to this field."


def generate_audit_comment(issue: str) -> str:
    """Generate a human-friendly comment for an audit issue.

    Behavior:
    - If real OpenAI is configured, call the API and return the model text.
    - Otherwise, return a useful local explanation (so AI appears always available in the app).
    """
    if not USE_AI:
        return f"[Mock AI] Issue detected: {issue}"

    # Prefer real OpenAI when available
    if real_ai_available():
        try:
            from openai import OpenAI
            client = OpenAI(api_key=OPENAI_API_KEY)

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a professional audit assistant."},
                    {"role": "user", "content": f"Explain this audit issue clearly:\n{issue}"}
                ],
                temperature=0.3
            )

            # Navigate response safely
            if getattr(response, "choices", None):
                choice = response.choices[0]
                if getattr(choice, "message", None) and getattr(choice.message, "content", None):
                    return choice.message.content
                if getattr(choice, "text", None):
                    return choice.text

            # Fallback generic text if API returns no usable text
            return f"[AI returned no text] {issue}"

        except Exception:
            logger.exception("OpenAI request failed; falling back to local explanation")
            # Fall through to local explanation

    # Local/mock explanation when real AI is not available or fails
    local = _explain_issue_locally(issue)
    return f"[Mock AI] {local}"
