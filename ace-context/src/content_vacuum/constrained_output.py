import outlines
import pydantic
import ollama

async_client = ollama.AsyncClient()

model = outlines.from_ollama(async_client,"qwen3-coder:30b")