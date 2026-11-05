import os
from dotenv import load_dotenv
from openai import AsyncOpenAI
from agents import OpenAIChatCompletionsModel, set_tracing_disabled

load_dotenv(override=True)
set_tracing_disabled(True)   # tracing OpenAI key maangta hai

MODEL_NAME = os.getenv("DEFAULT_MODEL_NAME", "gemini-3.5-flash-lite")

gemini_client = AsyncOpenAI(
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    api_key=os.getenv("GOOGLE_API_KEY"),
)
gemini_model = OpenAIChatCompletionsModel(model=MODEL_NAME, openai_client=gemini_client)