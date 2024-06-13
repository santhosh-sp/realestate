from datetime import datetime
from decouple import config
import pandas as pd 
import json


from groq_llm_api import get_groq
from utils import *


current_time = datetime.now().strftime("%d-%m-%Y")



class Demo:
    def __init__(self) -> None:
        pass

    def get_real_estate(self,conversation):
        prompt = f"""
    As analyst you job is to analyse the given text. The text is taken from a feedback survey in indian regional languages so you need analyse the text. As the text is converted from speech to text model from the audio message from the customer the text might not be proper and might not make any sense in some cases. In those scenarioes i request to strictly please mark it as 'NA'.
    sentiment:
    sentiment of the overall conversation.positive: If the customer responds for more than 3 questions from agent and interested or planning to buy. negative: If there is no responses and not interested to buy. neutral: If the customer is responds for few questions.
    duration_in_days:
    You are responsible for detecting the duration from the either Hindi or English sentence. The response should be in json format with key of duration_in_days with integer. If the customer says date or month or year or some kind of duration need to count from {current_time}.NOTE:Convert duration into days. If there is no duration mentioned from the customer respond with -1. If customer wants it immediately respond with 0.
    """
        output_format = """
    Expected Json output format:
        {"sentiment":"positive,negative,neutral,NA",
        "duration_in_days": "number"}
    NOTE:The output response format should be compulsorily in json format Without any extra explanation.
    """
        full_text = full_conversation(conversation=conversation)
        rp = get_groq(input_text=full_text,system_prompt=prompt+output_format)
        features = json.loads(rp)
        lead_type = get_realestate_leadtype(duration=features.get("duration_in_days", -1))
        features["lead_type"] = lead_type

        return features
    

    def get_loan(self,conversation):
        full_text = full_conversation(conversation=conversation)
        prompt = f"""
    As analyst you job is to analyse the given text. The text is taken from a feedback survey in indian regional languages so you need analyse the text. As the text is converted from speech to text model from the audio message from the customer the text might not be proper and might not make any sense in some cases. In those scenarioes i request to strictly please mark it as 'NA'.
    sentiment:
    sentiment of the overall conversation.positive: If the customer responds for more than 3 questions from agent and interested or planning to buy. negative: If there is no responses and not interested to buy. neutral: If the customer is responds for few questions.if not found please return NA.
    loan_amount:
    Get the customer loan amount form the given conversation accurately in integers.if not found please return -1.
    employment_status:
    Get the customer employment status form the given conversation and categories into salaried,self_employed.if not found please return NA.
    cibil_score:
    Get the cibil score form the given conversation intent if cibil score is found in number good:706-800, average:600-705,poor:0-600.if not found please return NA.
    """
        output_format="""
    Expected in Json output format:
    {"loan_amount": "(big number) in numbers",
    "employment_status":"string",
    "cibil_score": "good/average/bad/NA",
    "sentiment":"positive,negative,neutral,NA"}
    NOTE:The output response format should be compulsorily in json format Without any extra explanation.
    """
        rp = get_groq(input_text=full_text,system_prompt=prompt+output_format)
        rp_dict = json.loads(rp)
        print(rp_dict)
        features = get_loan_leadtype(rp_dict)
        return features
 
