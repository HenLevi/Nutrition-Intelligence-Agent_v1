import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.1"


def ollama_call(prompt: str, timeout: int = 120) -> str:
    r = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False,
        },
        timeout=timeout,
    )
    r.raise_for_status()
    return r.json()["response"].strip()


def detect_language(text: str) -> str:
    prompt = (
        "Detect the language of the following text. "
        "Answer with one word only: Hebrew or English.\n\n"
        f"{text}"
    )
    return ollama_call(prompt).lower()


def translate(text: str, target_language: str) -> str:
    prompt = f"Translate the following text to {target_language}:\n\n{text}"
    return ollama_call(prompt)
