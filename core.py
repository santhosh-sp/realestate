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
from groq_llm_api import groq_api
import time

logger = logging.getLogger("core")


did_numbers = {
    "+911214296124": ["naveen_realesate.json", "userreply_naveen"], # callflow, customer_table 
    "+911214296123": ["realestate_demo.json", "userreply"]
}

class Intentfinder:

    def __init__(self, question, customer_answer, did) -> None:
        self.customer_answer = customer_answer
        self.question = question
        self.did = did

        try:
            file_path = did_numbers.get(self.did, None)[0]  # fetching call flow json file 

        except Exception as e:

            raise Exception(f"Inavlid did number: {self.did} ")

        
        with open(f"./clients/{file_path}", 'r') as rfile:
            
          self.main_dict = json.load(rfile)

    def main(self): 
        next_question = self.main_dict[str(self.question)]['next']
        defualt_intents = self.main_dict[str(self.question)]['intents']

        print("categories:", list(defualt_intents.keys()))

        print("Question: ", self.main_dict[str(self.question)]['text'])

        print(f"Customer Answer: {self.customer_answer}")

        # print(defualt_intents)
        prompt = """You are an real estate Hindi and english language AI assistant trained to categorize user answers into predefined categories. Your goal is to analyze customer answer , assign the most relevant one categorie associated with from listed below.  The output should be in json format {"categorie": "value"}. The value should be in string format."""
        output_value = f"""
    categories: {list(defualt_intents.keys())}
    Question :  {self.main_dict[str(self.question)]['text']}
    Customer Answer: {self.customer_answer}
    """
        final_prompt = prompt+output_value
        try:   
            rp=fireworks_mixtral_intent(prompt=final_prompt)
            intent = json.loads(rp)['categorie']
            
            # start = time.time()
            # rp = groq_api(all_intents=list(defualt_intents.keys()), 
            #               question=self.main_dict[str(self.question)]['text'],
            #               answer=self.customer_answer
            #               )
            # print("Time taken for groq api: ", time.time() - start)
            
            # intent = json.loads(rp)['category']

            action=self.get_agent_intent(intent, defualt_intents)
            return {"intent":intent,"action":action, "next_question" : next_question}
        
        except Exception as e:
            logging.info(traceback.format_exc())
            logging.error(str(e))
            # raise APIException(e, sys) from e
            return {"error": True, "message": str(e)}
    
    
    def get_agent_intent(self,customer_intent, intent_mapping):
        print(intent_mapping,customer_intent)
        return intent_mapping.get(customer_intent, "positive")

    def get_filename_intent(self,agent_intent,filemame_mapping):
        return filemame_mapping.get(agent_intent, "novoice.mp3")
    