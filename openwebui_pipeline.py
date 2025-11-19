"""
title: Llama Index Ollama Pipeline
author: open-webui
date: 2024-05-30
version: 1.0
license: MIT
description: A pipeline for retrieving relevant information from a knowledge base using the Llama Index library with Ollama embeddings.
requirements: llama-index, llama-index-llms-ollama, llama-index-embeddings-ollama
"""

from typing import List, Union, Generator, Iterator
from schemas import OpenAIChatMessage
import os
import requests
from pydantic import BaseModel


class Pipeline:

    class Valves(BaseModel):
        BACKEND_URL: str="http://host.docker.internal:8000"
        PROVIDER: str = "ollama"
        MODEL_NAME: str = "gemma3:4b"
        TEMPERATURE: float = 0.1
        RESPONSE_FORMAT: str = "text"

    def __init__(self):
        # self.documents = None
        # self.index = None
        self.valves = self.Valves(
            **{
                "BACKEND_URL": os.getenv("BACKEND_URL", "http://host.docker.internal:8000"),
                "PROVIDER": os.getenv("PROVIDER", "ollama"),
                "MODEL_NAME": os.getenv("MODEL_NAME", "gemma3:4b"),
                "TEMPERATURE": float(os.getenv("TEMPERATURE", 0.1)),
                "RESPONSE_FORMAT": os.getenv("RESPONSE_FORMAT", "text")
            }
        )

    async def on_startup(self):
        # from llama_index.embeddings.ollama import OllamaEmbedding
        # from llama_index.llms.ollama import Ollama
        # from llama_index.core import Settings, VectorStoreIndex, SimpleDirectoryReader

        # Settings.embed_model = OllamaEmbedding(
        #     model_name=self.valves.LLAMAINDEX_EMBEDDING_MODEL_NAME,
        #     base_url=self.valves.LLAMAINDEX_OLLAMA_BASE_URL,
        # )
        # Settings.llm = Ollama(
        #     model=self.valves.LLAMAINDEX_MODEL_NAME,
        #     base_url=self.valves.LLAMAINDEX_OLLAMA_BASE_URL,
        # )

        # # This function is called when the server is started.
        # global documents, index

        # self.documents = SimpleDirectoryReader("/app/backend/data").load_data()
        # self.index = VectorStoreIndex.from_documents(self.documents)
        pass

    async def on_shutdown(self):
        # This function is called when the server is stopped.
        pass

    # def pipe(
    #     self, user_message: str, model_id: str, messages: List[dict], body: dict
    # ) -> Union[str, Generator, Iterator]:
    #     # This is where you can add your custom RAG pipeline.
    #     # Typically, you would retrieve relevant information from your knowledge base and synthesize it to generate a response.

    #     print(messages)
    #     print(user_message)

    #     query_engine = self.index.as_query_engine(streaming=True)
    #     response = query_engine.query(user_message)

    #     return response.response_gen
    
    def pipe(self,user_message: str) -> Union[str, Generator, Iterator]:
        url = f"{self.valves.BACKEND_URL}/kb/generate"
        
        data = {
            "provider": self.valves.PROVIDER,
            "model_name": self.valves.MODEL_NAME,
            "temperature": self.valves.TEMPERATURE,
            "response_format": self.valves.RESPONSE_FORMAT,
            "query": user_message
        }
        
        try:
            print(f"Sending request to {url}...")
            response = requests.post(url, data=data)
            
            print(f"Response status: {response.status_code}")
            print(f"Response headers: {dict(response.headers)}")
            
            if response.status_code == 200:
                if self.valves.RESPONSE_FORMAT == "json":
                    result = response.json()
                    print("\nJSON Response:")
                    print(result)
                    return result
                else:
                    result = response.text
                    print("\nText Response:")
                    print(result)
                    return result
            else:
                print(f"Error: {response.status_code}")
                print(f"Error message: {response.text}")
                return None
        except Exception as e:
            print(f"Exception occurred: {str(e)}")
            return None