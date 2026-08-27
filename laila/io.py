import shutil
import subprocess


class ConsoleInput:
    def read(self) -> str:
        return input("You: ").strip()


class ConsoleOutput:
    def write(self, text: str, end: str = "\n", flush: bool = False) -> None:
        print(text, end=end, flush=flush)


class MacSpeechOutput:
    def speak(self, text: str) -> None:
        if shutil.which("say"):
            subprocess.run(
                ["say", text],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=False,
            )