"""
title: Llama Index Ollama Pipeline
author: open-webui
date: 2024-05-30
version: 1.0
license: MIT
description: A pipeline for retrieving relevant information from a knowledge base using the Llama Index library with Ollama embeddings.
requirements: requests
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
        print ("updated genrator")

    async def on_shutdown(self):
        # This function is called when the server is stopped.
        pass
      
    def pipe(self, user_message: str, model_id: str, messages: List[dict], body: dict) -> Union[str, Generator, Iterator]:
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
            response = requests.post(url, data=data,stream=True)
            
            print(f"Response status: {response.status_code}")
            
            if response.status_code == 200:
                # For text streaming, yield chunks as they come
                full_response = ""
                chunk=""
                for chunk in response.iter_content(decode_unicode=True, chunk_size=1024):
                    if chunk:
                        full_response += chunk
                        yield chunk
                print("\n\nStreaming complete")
                print({"openui_user_message:":user_message,"openui_messages":messages,"openui_body":body})
            else:
                print(f"Error: {response.status_code}")
                print(f"Error message: {response.text}")
                return response.text
        except Exception as e:
            print(f"Exception occurred: {str(e)}")
            yield f"Exception occurred: {str(e)}"