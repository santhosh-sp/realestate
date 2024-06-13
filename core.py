""" 
all core modules to be declared here 
"""
# import torch
import traceback
import logging, ast, sys, json
from exception import APIException

#### internal 
import models
import custom_features
from llm_api import fireworks_mixtral_intent, fireworks_llm, fireworks_intent_70b
from groq_llm_api import groq_api, groq_conversation_intent_70b, groq_outbound_conversation

logger = logging.getLogger("core")

def find_usecase(instance,usecase):
    usecase_name = "get_" + usecase.lower().replace("-", "_").replace(" ","_")
    fetch_usecase = getattr(instance, usecase_name)
    return fetch_usecase

def find_client(class_name,usecase):
    try:
        my_class = getattr(custom_features,class_name.capitalize())
        fetch_team = find_usecase(my_class(),usecase)
        return fetch_team
    except Exception as e:
        raise APIException(e, sys) from e

did_numbers = {
    "+911214296124": ["naveen_realesate.json", "userreply_naveen"], # callflow, customer_table 
    "+911214296123": ["realestate_demo.json", "userreply"],
    "101": ["realestate_outbound_conversation.json", "no_table"]
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
    

class OutBoundConversation:

    ALL_INTENTS = {'inquire_property_details': 'k1',
                    'schedule_property_viewing': 'k2',
                    'ask_property_availability': 'k3',
                    'negotiate_price': 'k4',
                    'request_mortgage_information': 'k5',
                    'inquire_about_neighborhood': 'k6',
                    'sell_property': 'k7',
                    'rent_property': 'k8',
                    'request_property_valuation': 'k9',
                    'ask_about_property_documents': 'k10',
                    'request_contact_with_agent': 'k11',
                    'follow_up_on_previous_inquiry': 'k12',
                    'inquire_property_management_services': 'k13',
                    'ask_about_investment_opportunities': 'k14',
                    'inquire_about_open_houses': 'k15',
                    'request_virtual_tour': 'k16',
                    'ask_for_property_recommendations': 'k17',
                    'property_pricing': 'k18',
                    'property_discount': 'k19',
                    'ready_to_move': 'k20',
                    'how_many_bhk': 'k21',
                    'location': 'k22'}



    def __init__(self, call_id, did, customer_answer, question_number) -> None:

        self.call_id = call_id
        self.did = did
        self.customer_answer = customer_answer
        self.question_number = question_number

        try:
            file_path = did_numbers.get(self.did, None)[0]  # fetching call flow json file 

        except Exception as e:

            raise Exception(f"Invalid did number: {self.did}, Please check valid DID number... ")

        
        with open(f"./clients/{file_path}", 'r') as rfile:
            
          self.main_dict = json.load(rfile)


    def main(self): 

        next_question = self.main_dict[str(self.question_number)]['next']
        # defualt_intents = self.main_dict[str(self.question_number)]['intents']

        print("Question: ", self.main_dict[str(self.question_number)]['text'])

        print(f"Customer Answer: {self.customer_answer}")

        # print(defualt_intents)
        
    #     output_value = f"""
    # categories: {list(defualt_intents.keys())}
    # Question :  {self.main_dict[str(self.question)]['text']}
    # Customer Answer: {self.customer_answer}
    # """

        next_question = self.main_dict[str(self.question_number)]['next']

        try:   
            rp = groq_outbound_conversation(question = self.main_dict[str(self.question_number)]['text'],
                                            answer = self.customer_answer)
            type_response = rp["type"]
            
            if type_response == "question":
                
                return {"intent": rp["category"], 
                        "question": True,
                        "next_question" : self.ALL_INTENTS[rp["category"]],
                        "current_question": self.question_number
                        }

            elif type_response == "answer":

                return {"intent": rp["category"], 
                        "question": False,
                        "next_question" : next_question,
                        "current_question": self.question_number
                        }

            else:

                return {"intent": "no", 
                        "question": False,
                        "next_question" : next_question,
                        "current_question": self.question_number
                        }
        
        except Exception as e:
            logging.info(traceback.format_exc())
            logging.error(str(e))
            # raise APIException(e, sys) from e
            return {"error": True, "message": str(e)}
    
    
    def get_agent_intent(self,customer_intent, intent_mapping):
        print(intent_mapping,customer_intent)
        return intent_mapping.get(customer_intent, "positive")



def call_analysis(calldata: models.CallAnalysisModel):

    call_method = find_client(class_name=calldata.schema_name,usecase=calldata.usecase)
    features=call_method(calldata.conversation)
    
    return {"call_id": calldata.call_id,
            "features": features}

def conversation_intent(question):

    # intent = fireworks_intent_70b(input_text=question)

    intent = groq_conversation_intent_70b(question=question)

    print("Intent:", intent)

    category = intent.get("category", "others")

    return {"intent": category, "question": question}
