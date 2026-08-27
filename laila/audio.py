import time


class MicrophoneInput:
    def __init__(
        self,
        sample_rate: int = 16000,
        chunk_seconds: float = 0.1,
        max_seconds: int = 8,
        silence_seconds: float = 0.7,
        threshold: int = 550,
    ):
        self._sample_rate = sample_rate
        self._chunk_seconds = chunk_seconds
        self._max_seconds = max_seconds
        self._silence_seconds = silence_seconds
        self._threshold = threshold

    def read(self) -> str:
        try:
            import speech_recognition as sr
            import sounddevice as sd
            import numpy as np
        except ImportError as error:
            raise RuntimeError(
                "Voice input needs SpeechRecognition, sounddevice, and NumPy. "
                "Run: python -m pip install -r requirements.txt"
            ) from error

        chunks = []
        started = False
        silent_for = 0
        print("Listening... speak when ready.", flush=True)
        with sd.InputStream(
            samplerate=self._sample_rate,
            channels=1,
            dtype="int16",
            blocksize=int(self._chunk_seconds * self._sample_rate),
        ) as stream:
            deadline = time.monotonic() + self._max_seconds
            while time.monotonic() < deadline:
                chunk, _ = stream.read(int(self._chunk_seconds * self._sample_rate))
                chunks.append(chunk.copy())
                volume = np.abs(chunk.astype(np.int32)).mean()
                if volume > self._threshold:
                    started = True
                    silent_for = 0
                elif started:
                    silent_for += self._chunk_seconds
                    if silent_for >= self._silence_seconds:
                        break

        if not started:
            return ""
        recording = np.concatenate(chunks)
        audio = sr.AudioData(recording.tobytes(), self._sample_rate, 2)
        try:
            return sr.Recognizer().recognize_google(audio)
        except sr.UnknownValueError:
            print("I could not understand that. Listening again.", flush=True)
            return ""
        except sr.RequestError as error:
            raise RuntimeError("Speech recognition needs an internet connection.") from error