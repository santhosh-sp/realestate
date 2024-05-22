"""
groq llm api 

"""
import time
from groq import Groq
import json

client = Groq(api_key="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")

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


if __name__ == "__main__":

    start = time.time()

    print(groq_api(all_intents=['yes', 'no', 'others', 'hello', 'looking', 'who'], 
                   question=" नमस्कार, मैं दोस्ती ग्रेटर थाने प्रोजैक्ट से बात कर रही हुँ। हमारी वेबसाइट पर अपना इंटरेस्ट दिखाने के लिए धन्यवाद।। मैं आपकी मदद करने के लिए यहाँ हूँ। क्या आप किसी घर की तलाश में हैं?",
                   answer="who is this "))

    print(time.time() - start)