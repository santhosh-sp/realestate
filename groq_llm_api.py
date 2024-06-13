"""
groq llm api 

"""
import time
from groq import Groq
import json
from decouple import config

client = Groq(api_key=config("GROQ_API_KEY"))

def groq_api(all_intents, question, answer):

    completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {
                "role": "system",
                "content": f""" You are an real estate Hindi language AI assistant trained to categorize user answers into predefined categories. Your goal is to analyze customer answer , assign the most relevant one categories among the list associated with from listed below.  The output should be in json format key: "category", value: "value" The value should be in string format.\n\ncategories: {all_intents}\n """
            },
            {
                "role": "user",
                "content": f"Question: {question} \n Customer Answer: {answer} "
            }
        ],
        temperature=0.51,
        max_tokens=100,
        top_p=1,
        stream=False,
        response_format={"type": "json_object"},
        stop=None,
        seed=1,
    )

    try:
        return completion.choices[0].message.content

    except Exception as e:

        print("error on groq api :", str(e))
        return {}

def groq_conversation_intent_70b(question):
  print("groq llm:", question)

  completion = client.chat.completions.create(
      model="llama3-70b-8192",
      messages=[
          {
              "role": "system",
            "content": "You are a real estate Hindi language AI assistant trained to categorize user answers into predefined categories. Your goal is to analyze customer answers and assign the most relevant category from the list provided below. The output should be in JSON format with the key as \"category\" and the value as the assigned category. The value should be in string format.\n\nCategories: [\n  \"inquire_property_details\",\n  \"schedule_property_viewing\",\n  \"ask_property_availability\",\n  \"negotiate_price\",\n  \"request_mortgage_information\",\n  \"inquire_about_neighborhood\",\n  \"sell_property\",\n  \"rent_property\",\n  \"request_property_valuation\",\n  \"ask_about_property_documents\",\n  \"request_contact_with_agent\",\n  \"follow_up_on_previous_inquiry\",\n  \"inquire_property_management_services\",\n  \"ask_about_investment_opportunities\",\n  \"inquire_about_open_houses\",\n  \"request_virtual_tour\",\n  \"ask_for_property_recommendations\",\n  \"property_pricing\",\n  \"property_discount\",\n  \"ready_to_move\",\n  \"how_many_bhk\",\n  \"ready_to_move\",\n  \"location\"\n]\n"          },
          {
              "role": "user",
              "content": question
          }
      ],
      temperature=1,
      max_tokens=100,
      top_p=1,
      stream=False,
      response_format={"type": "json_object"},
      stop=None,
  )

  # print(completion.choices[0].message.content)

  return json.loads(completion.choices[0].message.content)


def groq_outbound_conversation(question, answer):
  
    print("groq outbound conversation llm:", question)



    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {
                "role": "system",
                "content": "You are a Hindi language AI assistant specialized in real estate domain. Your primary task is to analyze customer responses and determine if they are questions, direct answers to an agent's question, or statements. Based on this analysis, you will assign the most relevant category from the predefined list below. Additionally, you will specify if the response is a \"question\" or \"answer\". The output must be in JSON format with two keys: \"type\" and \"category\". The \"type\" key will have the value \"question\" or \"answer\", and the \"category\" key will have the assigned category as its value, formatted as a string.\n\nCategories: [\n\"inquire_property_details\",\n\"schedule_property_viewing\",\n\"ask_property_availability\",\n\"negotiate_price\",\n\"request_mortgage_information\",\n\"inquire_about_neighborhood\",\n\"sell_property\",\n\"rent_property\",\n\"request_property_valuation\",\n\"ask_about_property_documents\",\n\"request_contact_with_agent\",\n\"follow_up_on_previous_inquiry\",\n\"inquire_property_management_services\",\n\"ask_about_investment_opportunities\",\n\"inquire_about_open_houses\",\n\"request_virtual_tour\",\n\"ask_for_property_recommendations\",\n\"property_pricing\",\n\"property_discount\",\n\"ready_to_move\",\n\"how_many_bhk\",\n\"location\"\n]",          
            },
            {
                "role": "user",
                "content": question + "\n" + answer
            }
        ],
        temperature=0.3,
        max_tokens=100,
        top_p=1,
        stream=False,
        response_format={"type": "json_object"},
        stop=None,
    )

    # print(completion.choices[0].message.content)

    return json.loads(completion.choices[0].message.content)

def get_groq(system_prompt,input_text):
    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user","content": input_text}
        ],
        temperature=0.3,
        max_tokens=100,
        top_p=1,
        stream=False,
        response_format={"type": "json_object"},
        stop=None,
    )

    return completion.choices[0].message.content



if __name__ == "__main__":

    start = time.time()

    print(groq_api(all_intents=['yes', 'no', 'others', 'hello', 'looking', 'who'], 
                   question=" नमस्कार, मैं दोस्ती ग्रेटर थाने प्रोजैक्ट से बात कर रही हुँ। हमारी वेबसाइट पर अपना इंटरेस्ट दिखाने के लिए धन्यवाद।। मैं आपकी मदद करने के लिए यहाँ हूँ। क्या आप किसी घर की तलाश में हैं?",
                   answer="who is this "))

    print(time.time() - start)