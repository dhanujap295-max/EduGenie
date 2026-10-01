"""Gemini API client for EduGenie."""
import os
import re
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent / ".env")

MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-2.5-flash").strip() or "gemini-2.5-flash"
_client = None

class GeminiError(Exception):
    pass

def _get_client():
    global _client
    if _client is not None:
        return _client
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key or api_key.lower() in {"your_gemini_api_key_here", "paste_your_api_key_here"}:
        raise GeminiError("Gemini API key is missing. Open .env and set GEMINI_API_KEY, then restart the server.")
    try:
        from google import genai
        _client = genai.Client(api_key=api_key)
        return _client
    except Exception as exc:
        raise GeminiError(f"Could not initialize Gemini client: {exc}") from exc

def generate(prompt: str, json_mode: bool = False) -> str:
    client = _get_client()
    kwargs = {"model": MODEL_NAME, "contents": prompt}
    if json_mode:
        try:
            from google.genai import types
            kwargs["config"] = types.GenerateContentConfig(response_mime_type="application/json")
        except Exception:
            pass
    try:
        response = client.models.generate_content(**kwargs)
    except Exception as exc:
        raise GeminiError(f"Gemini API error: {exc}") from exc
    text = getattr(response, "text", None)
    if not text or not text.strip():
        raise GeminiError("Gemini returned an empty response. Try again.")
    return text.strip()

def clean_json_block(text: str) -> str:
    return re.sub(r"```(?:json)?\s*\n?(.*?)```", r"\1", text, flags=re.DOTALL).strip()
