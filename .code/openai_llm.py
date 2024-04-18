import os
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
#from langchain.chat_models import ChatOpenAI

from langchain_community.chat_models import ChatYandexGPT
from langchain_core.messages import HumanMessage, SystemMessage

#api_token = os.getenv("OPENAI_TOKEN")


class MyChatOpenAI:
    
    def __init__(self,api_token,folder_id=None):
        #self.chat = ChatOpenAI(temperature=0, openai_api_key=api_token,max_tokens=4000)
        self.chat = ChatYandexGPT(api_key=api_token,temperature=0,folder_id=folder_id)
        self.api_token = api_token
        self.folder_id = folder_id
    def set_temperature(self,temperature):
        self.chat.temperature = temperature
    def reset(self):
        self.chat = ChatOpenAI(temperature=0, openai_api_key=self.api_token,max_tokens=200,folder_id=folder_id)
    def dialog(self,msg):
        response = self.chat.invoke(msg) # Assuming get_response method exists in ChatOpenAI
        return response
