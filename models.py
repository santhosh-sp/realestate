"""

all pydantic basic models to be declared here ..


"""

from pydantic import BaseModel
from typing import List, Dict

class Intent(BaseModel):
    customer_answer: str
    question:str
    did: str = None

class AnalysisModel(BaseModel):
    call_id:str
    did : str

class CallAnalysisModel(BaseModel):
    call_id: str
    schema_name:str
    usecase:str
    conversation: list


class ConversationIntentModel(BaseModel):
    customer_answer: str

class OutboundConversationModel(BaseModel):
    call_id: str
    did : str
    customer_answer : str
    question_number : str
    