"""Tiny client for any OpenAI-compatible endpoint (Ollama, llama.cpp, vLLM, LM Studio)."""
import json
import urllib.error
import urllib.request


class LLMError(RuntimeError):
    pass


def chat(base_url, model, messages, api_key="local", timeout=120, temperature=0.2):
    url = base_url.rstrip("/") + "/chat/completions"
    body = json.dumps(
        {"model": model, "messages": messages, "temperature": temperature, "stream": False}
    ).encode()
    req = urllib.request.Request(
        url,
        data=body,
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"},
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.load(resp)
        return data["choices"][0]["message"]["content"]
    except urllib.error.URLError as e:
        raise LLMError(
            f"Could not reach {url} ({e}). Is your local model server running? "
            "Try: ollama serve && ollama pull qwen2.5-coder:7b"
        ) from e
    except (KeyError, IndexError, ValueError) as e:
        raise LLMError(f"Unexpected response from model server: {e}") from e
