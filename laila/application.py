from .contracts import ChatService, PromptInput, SpeechOutput, TextOutput


class AssistantApplication:
    def __init__(
        self,
        chat_service: ChatService,
        prompt_input: PromptInput,
        speech_output: SpeechOutput,
        text_output: TextOutput,
        voice_mode: bool,
    ):
        self._chat_service = chat_service
        self._prompt_input = prompt_input
        self._speech_output = speech_output
        self._text_output = text_output
        self._voice_mode = voice_mode

    def run(self) -> int:
        model = self._chat_service.available_model()
        if self._voice_mode:
            self._text_output.write(
                f"laila online ({model}). Listening continuously. Press Ctrl+C to exit."
            )
        else:
            self._text_output.write(f"laila online ({model}). Type 'quit' to exit.")

        while True:
            try:
                prompt = self._prompt_input.read()
            except (EOFError, KeyboardInterrupt):
                self._text_output.write("")
                break
            if prompt.lower() in {"quit", "exit", "q"}:
                break
            if not prompt:
                continue
            self._text_output.write("laila is thinking...", flush=True)
            answer = self._chat_service.ask(
                prompt,
                model,
                on_token=lambda token: self._text_output.write(token, end="", flush=True),
            )
            self._text_output.write("")
            self._text_output.write(f"laila: {answer}")
            self._speech_output.speak(answer)
        return 0