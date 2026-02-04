import os
from dotenv import load_dotenv

# hugging face gets automatically loaded
load_dotenv()

# Creating config class below that will be used later
# Quen is an Open source model provided by alibaba on groqcloud. This model is good at reasoning and tool calling
# The bg-base-en-v1.5 is open source embedding model created by BAAI which is a powerful tool for NLP tasks
class Config:
    ASTRA_DB_API_ENDPOINT = os.getenv("ASTRA_DB_API_ENDPOINT")
    ASTRA_DB_APPLICATION_TOKEN = os.getenv("ASTRA_DB_APPLICATION_TOKEN")
    ASTRA_DB_KEYSPACE = os.getenv("ASTRA_DB_KEYSPACE")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    EMBEDDING_MODEL = "BAAI/bge-base-en-v1.5"
    RAG_MODEL = "groq:qwen/qwen3-32b"
