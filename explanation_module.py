"""Concept explanation using Gemini."""
from gemini_client import generate

def explain_topic(topic: str) -> str:
    prompt = (
        f"Explain '{topic}' in very simple language for a beginner student. "
        "Use a short everyday example and keep it under 150 words."
    )
    return generate(prompt)
