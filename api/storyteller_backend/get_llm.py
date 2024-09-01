from langchain_openai import ChatOpenAI

from dotenv import load_dotenv
import openai
import os

load_dotenv()
openai.api_key = os.environ["OPENAI_API_KEY"]


def get_llm():
    return ChatOpenAI(model='gpt-3.5-turbo', temperature=0)
