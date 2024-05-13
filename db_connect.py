import mysql.connector
from datetime import datetime
import requests,json
from openai import OpenAI
import pandas as pd 
client = OpenAI(api_key="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")

current_time = datetime.now().strftime("%d-%m-%Y")


def get_trans(fullrecording):
    file = requests.get(fullrecording).content
    rp=get_dia(file)
    dia_data=rp.json()['speech_data']
    trans_rp=get_transcript(file,dia_data)
    trans_dict=trans_rp.json()['data']['transcript']
    trans_result=pd.DataFrame(trans_dict)[['start','end','lang_id','text','index','speaker_name','transliteration']].to_dict(orient='records')
    return trans_result

def get_duration(input_text):
    SYSTEM_PROMPT = f""" You are responsible for detecting the duration from the either Hindi or English sentence. The response should be in json format with key of duration in days with integer or float. If the user says date need to count from {current_time}. Note: convert months into days."""

    response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {
        "role": "system",
        "content": SYSTEM_PROMPT
        },
        {
        "role": "user",
        "content": input_text
        }
    ],
    temperature=0.7,
    max_tokens=100,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
    )

    return response.choices[0].message.content

def get_con(trans_result):
    full_text = ""
    for i,r in trans_result.iterrows():
        if r['index']%2 == 0:
            speaker_name = 'customer'
        else:
            speaker_name = "agent"
        full_text += f"{speaker_name}:{r['text']} \n"
    return full_text

def get_dia(file):
    dia_url = "http://office02.servicepack.ai:7999/duration_with_langid?lang_id=false"

    payload={"lang_code": []}
    files=[('file_name',file)]    
    repsonse=requests.post(url=dia_url,data=payload,files=files)
    return repsonse

def get_transcript(file,dia_data):
    trans_url = "https://222a-183-82-10-250.ngrok-free.app/transcript"
    payload={"lang_id":False,
            "language": "hi-IN",
            "agent_channel":1,
            "number_of_channel":1,
            "boost_words": [],
            "speech_data":json.dumps(dia_data)}
    files=[('file_name',file)]    
    repsonse=requests.post(url=trans_url,data=payload,files=files)
    
    return repsonse

def get_sentiment(input_text):
    system_prompt = f"""As analyst you job is to analyse the given text. The text is taken from a feedback survey in indian regional languages so you need analyse the text. As the text is converted from speech to text model from the audio message from the customer the text might not be proper and might not make any sense in some cases. In those scenarioes i request to strictly please mark it as 'NA'
    duration_in_days:
    ou are responsible for detecting the duration from the either Hindi or English sentence. The response should be in json format with key of duration in days with integer or float. If the user says date need to count from {current_time}. Note: convert months into days.
    sentiment:
    sentiment of the overall conversation.


    NOTE:The output response format should be compulsorily in json format.
    """
    url = "https://api.fireworks.ai/inference/v1/completions"
    payload = {
        "max_tokens": 250,
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
                "enum": ["positive", "negative", "Neutral", "NA"]
              }
            },
            "required": ["sentiment"]
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
        "authorization": "Bearer lUgDG0UF8rSmgad0cDBVYDV104L5jCXT6cqGbCZ3N1QQ3BzH"
    }
    response = requests.post(url, json=payload, headers=headers)
    final_response = response.json()['choices'][0]['text']
    return final_response



def get_lead_type(duration):
    if duration > 1 and duration <=30:
        return "hot"
    elif duration > 30 and duration <= 60:
        return "warm"
    elif duration > 60:
        return "cold"
    else:
        return "dead"


def retrieve_data(calluid):
    try:
        # Connect to MySQL database

        connection = mysql.connector.connect(
            host="122.176.155.244",
            user="remoteuser",
            password="XEg52YVerPX1otzE",
            database="voicebot",
            port=4406
        )

        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)

            # Retrieve data based on id
            query = f"SELECT * FROM userreply WHERE calluid = %s"
            cursor.execute(query, (calluid,))
            records = cursor.fetchone()

            for_duration=dict(records.items())["userresponse_5"]
            query_update = "UPDATE userreply SET sentiment = %s, days = %s,lead_type = %s WHERE calluid = %s"

            # Execute the query with the parameters

            # Commit the changes
            transcript=get_trans(records['fullrecording']) 
            con_text = get_con(pd.DataFrame(transcript))
            sentiment = json.loads(get_sentiment(con_text)).get('sentiment','NA')
            duration = json.loads(get_duration(for_duration)).get('duration',0)
            lead_type = get_lead_type(duration)
            cursor.execute(query_update, (sentiment, duration, lead_type,calluid))
        connection.commit()
        return {"data": f"for {calluid} {duration}"}
    except mysql.connector.Error as error:
        print("Error connecting to MySQL database:", error)

        return {"error": error}

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed.")


if __name__ == "__main__":
    pass
    # Example usage
    # data=retrieve_data("d7be0cc6-53ba-45aa-9485-5cfe1a18307e")  # Replace "your_table_name" with the actual table name
    # print(get_duration("बाईस जुलाई"))