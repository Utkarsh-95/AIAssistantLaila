import os
from dataclasses import dataclass


SYSTEM_PROMPT = (
    "You are Laila, a fast and capable voice assistant. "
    "Understand the user's intent before answering. Give the direct answer first, "
    "keep replies to 1-3 short sentences, and ask one concise clarification question "
    "when the request is genuinely ambiguous. Do not repeat the user's request."
)


@dataclass(frozen=True)
class Settings:
    ollama_url: str = "http://localhost:11434"
    default_model: str = "gemma3:1b"
    system_prompt: str = SYSTEM_PROMPT
    model_timeout: int = 5
    chat_timeout: int = 120

    @classmethod
    def from_environment(cls):
        return cls(
            ollama_url=os.getenv("OLLAMA_URL", cls.ollama_url).rstrip("/"),
            default_model=os.getenv("OLLAMA_MODEL", cls.default_model),
        )