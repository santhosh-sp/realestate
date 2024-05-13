"""

all pydantic basic models to be declared here ..


"""

from pydantic import BaseModel
from typing import List, Dict

class Intent(BaseModel):
    customer_answer: str
    question:str

class AnalysisModel(BaseModel):
    call_id:str