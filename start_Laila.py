import argparse
import sys
from urllib.error import HTTPError, URLError
from laila.application import AssistantApplication
from laila.audio import MicrophoneInput
from laila.config import Settings
from laila.io import ConsoleInput, ConsoleOutput, MacSpeechOutput
from laila.ollama import OllamaChatService


def main():
    parser = argparse.ArgumentParser(description="Local voice assistant powered by Ollama")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--voice",
        dest="voice",
        action="store_true",
        default=True,
        help="listen through the microphone (default)",
    )
    mode.add_argument(
        "--text",
        dest="voice",
        action="store_false",
        help="type prompts instead of using the microphone",
    )
    args = parser.parse_args()

    try:
        app = AssistantApplication(
            chat_service=OllamaChatService(Settings.from_environment()),
            prompt_input=MicrophoneInput() if args.voice else ConsoleInput(),
            speech_output=MacSpeechOutput(),
            text_output=ConsoleOutput(),
            voice_mode=args.voice,
        )
        return app.run()
    except (HTTPError, URLError, TimeoutError, RuntimeError) as error:
        print(f"laila could not start: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())