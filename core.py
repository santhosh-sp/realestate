""" 
all core modules to be declared here 
"""
# import torch
import logging, ast
import traceback
import requests
import json
import sys
from llm_api import fireworks_mixtral_intent


logger = logging.getLogger("core")


class Intentfinder:

    def __init__(self, question,customer_answer) -> None:
        self.customer_answer = customer_answer
        self.question = question
        self.main_dict = {
    "q1": {
      "text": "नमस्कार, मैं दोस्ती ग्रेटर थाने प्रोजैक्ट से बात कर रही हुँ। हमारी वेबसाइट पर अपना इंटरेस्ट दिखाने के लिए धन्यवाद।। मैं आपकी मदद करने के लिए यहाँ हूँ। क्या आप किसी घर की तलाश में हैं?",
      "intents": { "yes": "positive", "no": "positive", "others": "negative", "hello": "positive", "looking": "positive"},
      "next": "2"
    },
    "q2": {
      "text": "बहुत बढ़िया। आप कितने BHK का फ्लैट देखना चहाते है ?",
      "intents": { "bhk": "positive", "not_interested": "negative","others": "negative", "hello": "positive"},
      "next": "3"
    },
    "q3": {
      "text": "ठीक है। क्या मैं आपका बजट जान सकती हूँ?",
      "intents": { "budget": "positive", "not_interested": "negative","others": "negative"},
      "next": "4"
    },
    "q4": {
      "text": "ठीक है, आप यह घर अपने लिए खरीदना चाहते हैं या investment purpose के लिए?",
      "intents": { "purpose": "positive", "not_interested": "negative","others": "negative"},
      "next": "5"
    },
    "q5": {
      "text": "आप इसे कब तक खरीदना चाहते हैं?",
      "intents": { "duration": "close", "not_interested": "negative","others": "negative" },
      "next": "end"
    }
  }
  

    def main(self): 
        next_question = self.main_dict[str(self.question)]['next']
        defualt_intents = self.main_dict[str(self.question)]['intents']

        print(defualt_intents)
        prompt = """You are an real estate Hindi language AI assistant trained to categorize user answers into predefined categories. Your goal is to analyze customer answer , assign the most relevant one categorie associated with from listed below.  The output should be in json format {"categorie": "value"}. The value should be in string format."""
        output_value = f"""
    categories: {list(defualt_intents.keys())}
    Question :  {self.main_dict[str(self.question)]['text']}
    Customer Answer: {self.customer_answer}
    """
        final_prompt = prompt+output_value
        try:   
            rp=fireworks_mixtral_intent(prompt=final_prompt)
            intent = json.loads(rp)['categorie']
            action=self.get_agent_intent(intent,defualt_intents)
            return {"intent":intent,"action":action, "next_question" : next_question}
        
        except Exception as e:
            logging.info(traceback.format_exc())
            logging.error(str(e))
            raise APIException(e, sys) from e
    
    
    def get_agent_intent(self,customer_intent,intent_mapping):
        print(intent_mapping,customer_intent)
        return intent_mapping.get(customer_intent, "Unknown Intent")

    def get_filename_intent(self,agent_intent,filemame_mapping):
        return filemame_mapping.get(agent_intent, "novoice.mp3")
    