
def full_conversation(conversation):

    full_text = " "

    # print(conversation, type(conversation))

    for con in conversation:
        # print(con["speaker"], con["text"])
        full_text += f'{con["speaker"]}: {con["text"]} \n'

    return full_text

def check_employment_status(employment_status:str):
    if employment_status =="salaried":
        return "hot"
    
    elif employment_status =="self_employed":
        return "warm"
    
    else:
        return "NA"

def check_loan_amount(loan_amount:int):
    if 0 < loan_amount <= 10000000:
        return "hot"
    elif 500000 >= loan_amount <= 10000000 and loan_amount > 0:
        return "warm"
    elif 0 <= loan_amount < 500000:
        return "cold"
    else:
        return "NA"

def check_cibil_score(cibil_score):

    if 0 < cibil_score >= 600:
        return "good"
    
    elif 0 <= cibil_score <= 600:
        return "bad"
    
    else:
        return "NA"



################################   LeadType  ###################################33
def get_realestate_leadtype(duration):
    try:
        if duration >= 0 and duration <=30:
            return "hot"
        elif duration > 30 and duration <= 60:
            return "warm"
        elif duration > 60:
            return "cold"
        elif duration < 0:
            return "no_response"
        else:
            return "no_response"
    except Exception as e:
        return "no_response"


def get_loan_leadtype(response:dict):
    employment_status=check_employment_status(response.get("employment_status","NA").lower())
    loan_amount=check_loan_amount(int(response.get("loan_amount",-1)))
    cibil_score=response.get("cibil_score","NA")
    sentiment=response.get("sentiment","NA")
    lead_type = loan_priority(employment_status,loan_amount,cibil_score)
    return {
        "employment_lead_type":employment_status,
        "loan_amount":loan_amount,
        "check_cibil_score":cibil_score,
        "sentiment":sentiment,
        "lead_type":lead_type
        }


def loan_priority(employment_status,loan_amount,cibil_score):
    if employment_status =='NA' and loan_amount == "NA" and cibil_score== "NA":
        return "no_response"
    if loan_amount and loan_amount != "NA":
        return loan_amount
    if employment_status and employment_status != "NA":
        return employment_status
    if cibil_score and cibil_score != "NA":
        return cibil_score
    return "NA"
    

