from asyncio.constants import LOG_THRESHOLD_FOR_CONNLOST_WRITES
from fastapi import FastAPI, Depends, HTTPException, status, Request, BackgroundTasks
import uvicorn
import traceback
# from app.loggers import logging
import models
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
import uuid
import shutil
import os
import core
from fastapi import FastAPI, Depends, HTTPException, status, Request, UploadFile, File
from typing import List
from db_connect import retrieve_data


# log  = logging.getLogger("uvicorn")

app = FastAPI()



@app.get("/")
async def read_main():
    return JSONResponse(status_code=status.HTTP_200_OK, content={"msg": "Hello World"})



@app.post("/intent")
async def get_intent(info : models.Intent):
    """ 
    Use to get_intent  to every text        
    """

    try:
        # logging.info("inside intent api ....")
        agent_obj = core.Intentfinder(customer_answer= info.customer_answer,
                                      question=info.question,
                                      did = info.did)
        final_data = agent_obj.main()
        # logging.info(final_datafinal_data)
        return JSONResponse(status_code=status.HTTP_200_OK, 
                            content= {"error": False, **final_data})
    
    except Exception as e:
        # import traceback
        # logging.error(traceback.format_exc())
        msg = str(e.error_message if hasattr(e, 'error_message') else e)

        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, 
                            content= {"error": True, "data": msg})


@app.post("/anlysis")
async def get_analysis(info: models.AnalysisModel, background_tasks: BackgroundTasks):
    """
    Use to get_intent  to every text
    """
    try:
        # logging.info("inside intent api ....")
        background_tasks.add_task(retrieve_data, info.call_id, info.did)
        # final_data = retrieve_data(calluid=info.call_id)
        # logging.info(final_datafinal_data)
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content= {"error": False, "data":"Success!!!"})
    except Exception as e:
        import traceback
        # logging.error(traceback.format_exc())
        msg = str(e.error_message if hasattr(e, 'error_message') else e)
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content= {"error": True, "data": msg})
    

@app.post("/call_analysis")
async def get_call_analysis(info: models.CallAnalysisModel):
    """
    Use to get call analysis to the conversation

    """

    print("callid:", info.call_id)
    try:

        ca = core.call_analysis(calldata=info)

        return JSONResponse(status_code=status.HTTP_200_OK,
                            content= {"error": False, "data": ca})
    except Exception as e:
        # import traceback
        # logging.error(traceback.format_exc())
        msg = str(e.error_message if hasattr(e, 'error_message') else e)
        traceback.print_exc()
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content= {"error": True, "data": msg})
    


@app.post("/conversation_intent")
async def get_conversation_intent(info: models.ConversationIntentModel):
    """
    Use to get_intent  to every text

    """

    print("conversation question :", info.customer_answer)
    try:

        ca = core.conversation_intent(question = info.customer_answer)

        return JSONResponse(status_code=status.HTTP_200_OK,
                            content= {"error": False, "data": ca})
    except Exception as e:
        # import traceback
        # logging.error(traceback.format_exc())
        msg = str(e.error_message if hasattr(e, 'error_message') else e)
        traceback.print_exc()
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content= {"error": True, "data": msg})



@app.post("/outbound_conversation")
async def get_outbound_conversation(info: models.OutboundConversationModel):
    """
        outbound_conversation for evry question 
    """

    print("conversation question :", info.customer_answer)
    try:

        ca = core.OutBoundConversation(call_id = info.call_id,
                                       did = info.did,
                                       customer_answer = info.customer_answer,
                                       question_number = info.question_number
                                       )
        
        result = ca.main()

        return JSONResponse(status_code=status.HTTP_200_OK,
                            content= {"error": False, "data": result})
    except Exception as e:
        # import traceback
        # logging.error(traceback.format_exc())
        msg = str(e.error_message if hasattr(e, 'error_message') else e)
        traceback.print_exc()
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content= {"error": True, "data": msg})

if  __name__ == "__main__":
    uvicorn.run(app,host="0.0.0.0",port=9000)
