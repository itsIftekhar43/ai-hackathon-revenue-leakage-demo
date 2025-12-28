import os
from dotenv import load_dotenv

load_dotenv()

USE_AI = os.getenv("USE_AI", "true").lower() == "true"

def generate_audit_comment(issue: str) -> str:
    if not USE_AI:
        return f"[Mock AI] Issue detected: {issue}"

    try:
        from openai import OpenAI
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a professional audit assistant."},
                {"role": "user", "content": f"Explain this audit issue clearly:\n{issue}"}
            ],
            temperature=0.3
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"[AI unavailable] {issue}"
