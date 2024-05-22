import logging
import ast 
import json
import requests

import sys

from decouple import config

def fireworks_mixtral_intent(prompt,token=config("FIRE_API")):
    url = "https://api.fireworks.ai/inference/v1/completions"
    payload = {
        "max_tokens": 150,
        "logprobs": None,
        "echo": False,
        "temperature": 0.5,
        "top_p": 1,
        "frequency_penalty": 0,
        "presence_penalty": 0,
        "n": 1,
        "stop": None,
        "response_format":{ 
            "type": "json_object",
                "schema":{
                        "type": "object",
                        "properties": {                            
                        "categorie": {
                            "type": "string"
                            }
                    },
                "required": ["categorie"]
            }
    },
    "stream": False,
        "model": "accounts/fireworks/models/llama-v3-8b-instruct-hf",
        "prompt": str(prompt)
        
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {token}"
    }
    response = requests.post(url, json=payload, headers=headers)
    try:
        return response.json()['choices'][0]['text']
    except Exception as e :
        # print("output error",response.text)
        return response.text   

