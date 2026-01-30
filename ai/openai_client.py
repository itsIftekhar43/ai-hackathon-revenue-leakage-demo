import os
from dotenv import load_dotenv
import logging

load_dotenv()

USE_AI = os.getenv("USE_AI", "true").lower() == "true"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

logger = logging.getLogger(__name__)


def ai_available() -> bool:
    """Return True if AI calls can be attempted."""
    return USE_AI and bool(OPENAI_API_KEY)


def generate_audit_comment(issue: str) -> str:
    """Generate a human-friendly comment for an audit issue.

    Falls back to a helpful mock message if AI is disabled or unavailable.
    """
    if not USE_AI:
        return f"[Mock AI] Issue detected: {issue}"

    if not OPENAI_API_KEY:
        logger.warning("OPENAI_API_KEY is not set. Falling back to mock AI response.")
        return f"[AI unavailable - no API key] Issue: {issue}"

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

        # Fallback generic text
        return f"[AI returned no text] {issue}"

    except Exception as e:
        logger.exception("OpenAI request failed")
        return f"[AI unavailable] {issue}"
