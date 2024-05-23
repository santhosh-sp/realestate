import logging
import ast 
import json
import requests
from datetime import datetime

import sys

from decouple import config

token = config("FIRE_API")

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



def fireworks_llm(input_text):
    current_time = datetime.now().strftime("%d-%m-%Y")

    print("llm started ..")
    system_prompt = f"""
    As analyst you job is to analyse the given text. The text is taken from a feedback survey in indian regional languages so you need analyse the text. As the text is converted from speech to text model from the audio message from the customer the text might not be proper and might not make any sense in some cases. In those scenarioes i request to strictly please mark it as 'NA'.
    sentiment:
    sentiment of the overall conversation.positive: If the customer responds for more than 3 questions from agent and interested or planning to buy. negative: If there is no responses and not interested to buy. neutral: If the customer is responds for few questions.
    duration_in_days:
    You are responsible for detecting the duration from the either Hindi or English sentence. The response should be in json format with key of duration in days with integer or float. If the user says date, need to count from {current_time}. 
    Note: Convert months into days. If there is no duration mentioned from the customer respond with -1. If customer wants it immediately respond with 0.

    NOTE:The output response format should be compulsorily in json format Without any extra explanation.
    """
    url = "https://api.fireworks.ai/inference/v1/completions"
    payload = {
        "max_tokens": 100,
        "logprobs": None,
        "echo": False,
        "temperature": 0.8,
        "top_p": 1,
        "frequency_penalty": 0,
        "presence_penalty": 0,
        "n": 1,
        "stop": None,
        "response_format": {
            "type": "json_object",
            "schema":{
            "type": "object",
            "properties": {
              "sentiment": {
                "type": "string",
                "enum": ["positive", "negative", "neutral", "NA"]
              },
                "duration_in_days":{
                    "type": "integer"
                }
            },
            "required": ["sentiment","duration_in_days"]
          }
        },
    #     "response_format":{"type":"text"},
        "stream": False,
        "model": "accounts/fireworks/models/llama-v3-70b-instruct",
        "prompt": system_prompt+input_text
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {token}"
    }
    response = requests.post(url, json=payload, headers=headers)
    final_response = response.json()['choices'][0]['text']
    return final_response

