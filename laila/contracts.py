from typing import Callable, Protocol


class ChatService(Protocol):
    def available_model(self) -> str:
        ...

    def ask(self, prompt: str, model: str, on_token: Callable[[str], None]) -> str:
        ...


class PromptInput(Protocol):
    def read(self) -> str:
        ...


class SpeechOutput(Protocol):
    def speak(self, text: str) -> None:
        ...


class TextOutput(Protocol):
    def write(self, text: str, end: str = "\n", flush: bool = False) -> None:
        ...