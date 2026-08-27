# Laila

Laila is a lightweight local AI assistant for macOS. It sends prompts to a
locally running [Ollama](https://ollama.com/) model, prints the response in the
terminal, and reads the response aloud with the macOS `say` command.

Laila supports two input modes:

- **Voice mode**: listens through the microphone, transcribes speech, and
	speaks the answer. This is the default.
- **Text mode**: reads prompts from the terminal. This is useful for setup,
	testing, and environments where microphone access is unavailable.

## How It Works

1. Laila checks Ollama for an available model through `GET /api/tags`.
2. It records a voice prompt or reads a line from the terminal.
3. It sends the prompt to Ollama through `POST /api/chat`.
4. The streamed response is printed to the terminal and spoken aloud.
5. The assistant repeats until you enter `quit`, `exit`, or `q` in text mode,
	 or press `Ctrl+C` in voice mode.

The assistant uses a short-response system prompt by default: answers are
normally limited to one to three short sentences, with a concise clarification
question when needed.

## Prerequisites

- macOS, for the built-in `say` speech output and microphone support
- Python 3
- [Ollama](https://ollama.com/download) installed and running
- An Ollama model, such as `gemma3:1b`
- Internet access when using voice mode, because speech transcription uses
	Google Speech Recognition

Text mode only needs the local Ollama service and does not require microphone
or speech-recognition access.

## Setup

From the project directory:

```bash
cd /Users/Utkarsh/AI/LailaAI

python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Start Ollama if it is not already running. The Ollama application normally
starts the local service automatically. It can also be started from a terminal:

```bash
ollama serve
```

Download the default model:

```bash
ollama pull gemma3:1b
```

Confirm that Ollama can see the model:

```bash
ollama list
```

On the first voice run, macOS may ask for microphone permission. Allow your
terminal application under **System Settings > Privacy & Security >
Microphone**.

## Runbook

### Run with text input

Text mode is the fastest way to verify the Python environment and Ollama
connection:

```bash
source .venv/bin/activate
python start_Laila.py --text
```

You should see a message similar to:

```text
laila online (gemma3:1b). Type 'quit' to exit.
```

Type a prompt at `You:` and press Enter. Enter `quit` to stop the assistant.

### Run with voice input

```bash
source .venv/bin/activate
python start_Laila.py
```

Laila listens for up to eight seconds for each prompt. After speech starts, it
stops recording after about 0.7 seconds of silence, transcribes the recording,
and sends the text to Ollama. Press `Ctrl+C` to exit.

The explicit voice flag is also available:

```bash
python start_Laila.py --voice
```

### Check the command options

```bash
python start_Laila.py --help
```

## Configuration

Configuration is controlled with environment variables:

| Variable | Default | Purpose |
| --- | --- | --- |
| `OLLAMA_URL` | `http://localhost:11434` | Base URL of the Ollama server |
| `OLLAMA_MODEL` | `gemma3:1b` | Preferred model name |

For example, to use another model already installed in Ollama:

```bash
OLLAMA_MODEL llama3.2:3b python start_Laila.py --text
```

If the preferred model is not installed, Laila uses the first model returned by
Ollama. If no models are installed, startup stops with an error.

To use Ollama on another machine, point Laila at that machine's API endpoint:

```bash
OLLAMA_URL=http://192.168.1.20:11434 python start_Laila.py --text
```

Only set this when the Ollama service is reachable from the current machine.

## Troubleshooting

### `urlopen error` or connection refused

Ollama is not reachable. Start it and verify the API directly:

```bash
curl http://localhost:11434/api/tags
```

If Ollama uses a different host or port, set `OLLAMA_URL` accordingly.

### `Ollama is running, but no models are installed.`

Install a model and try again:

```bash
ollama pull gemma3:1b
ollama list
```

### Voice input reports missing packages

Activate the virtual environment and install the project dependencies:

```bash
source .venv/bin/activate
python -m pip install -r requirements.txt
```

### Microphone input does not work

Check that the terminal application has microphone permission in macOS System
Settings. Also confirm that the intended microphone is selected as the macOS
input device.

### `I could not understand that`

This means speech was recorded but could not be transcribed. Speak closer to
the microphone, reduce background noise, or use text mode. Voice transcription
also requires an internet connection.

### No audio response

Laila uses the macOS `say` command. Verify it is available:

```bash
which say
say "Laila audio test"
```

The text response is still printed even when `say` is unavailable.

### The response takes too long

The model request timeout is 120 seconds. Smaller local models usually respond
faster. You can also select another installed model with `OLLAMA_MODEL`.

## Project Structure

```text
start_Laila.py       Command-line entry point and mode selection
laila/
	application.py     Main assistant loop
	audio.py           Microphone capture and speech transcription
	config.py          Environment-backed settings and system prompt
	contracts.py       Interfaces for input, output, and chat services
	io.py              Terminal I/O and macOS speech output
	ollama.py          Ollama model discovery and streaming chat requests
requirements.txt     Python dependencies for voice input
```

The input, output, and chat interfaces are kept separate from the application
loop. This makes text mode useful for local verification and keeps the Ollama
integration replaceable.

## Development Checks

Compile the Python files to catch syntax errors:

```bash
python -m compileall start_Laila.py laila
```

Inspect the available CLI options without connecting to Ollama:

```bash
python start_Laila.py --help
```

There are currently no automated tests in the repository.
