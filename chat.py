from langchain.chat_models import ChatOpenAI
import os

OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]


def get_response(formatted_prompt, model="gpt-3.5-turbo", temp=1):
    model = ChatOpenAI(
        model_name=model, 
        temperature=0,
        openai_api_key=OPENAI_API_KEY
    )
    response = model(formatted_prompt).content
    return response

def get_batch_response(batch, model="gpt-3.5-turbo", temp=1):
    model = ChatOpenAI(model_name=model, temperature=temp, openai_api_key="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")
    batch_response = model.generate(batch)
    return [batch_response[i][0].message.content for i in range(len(batch))]