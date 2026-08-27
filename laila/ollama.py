import json
from typing import Callable
from urllib.request import Request, urlopen

from .config import Settings


class OllamaChatService:
    def __init__(self, settings: Settings):
        self._settings = settings

    def available_model(self) -> str:
        request = Request(f"{self._settings.ollama_url}/api/tags")
        with urlopen(request, timeout=self._settings.model_timeout) as response:
            models = json.load(response).get("models", [])
        names = [model.get("name") for model in models if model.get("name")]
        if self._settings.default_model in names:
            return self._settings.default_model
        if names:
            return names[0]
        raise RuntimeError("Ollama is running, but no models are installed.")

    def ask(self, prompt: str, model: str, on_token: Callable[[str], None]) -> str:
        payload = {
            "model": model,
            "stream": True,
            "options": {"num_predict": 128, "temperature": 0.2, "top_p": 0.9},
            "messages": [
                {"role": "system", "content": self._settings.system_prompt},
                {"role": "user", "content": prompt},
            ],
        }
        request = Request(
            f"{self._settings.ollama_url}/api/chat",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
        )
        parts = []
        with urlopen(request, timeout=self._settings.chat_timeout) as response:
            for line in response:
                if not line.strip():
                    continue
                result = json.loads(line)
                part = result.get("message", {}).get("content", "")
                if part:
                    on_token(part)
                    parts.append(part)
                if result.get("done"):
                    break
        return "".join(parts).strip()