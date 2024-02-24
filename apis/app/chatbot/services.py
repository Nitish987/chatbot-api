import requests
import openai
import json
from django.conf import settings
from common.platform.products import Product
from common.debug.log import Log
from firebase_admin import firestore


def update_billing(project_id, api_id):
    requests.put(
        f'{settings.EXTERNAL_SERVER_HOST_URL}/api/external/v1/import/update-billing/?project_id={project_id}&api_id={api_id}', headers={'ASAK': settings.EXTERNAL_SERVER_API_KEY}
    )


def ai_emform_tool(useEmform: bool, emform: str):
        if useEmform and emform:
            return emform
        return 'Unable to process.'


class ChatbotService:
    is_valid = False
    data = {}

    def __init__(self, project_id: str, api_id: str):
        self.project_id = project_id
        self.api_id = api_id

    def initialize(self, apikey: str):
        response = requests.get(
            f'{settings.EXTERNAL_SERVER_HOST_URL}/api/external/v1/import/product/?project_id={self.project_id}&api_id={self.api_id}',
            headers={'ASAK': settings.EXTERNAL_SERVER_API_KEY}
        )
        response = response.json()
        # Log.info(response)
        self.is_valid = response['success'] and response['data']['apikey'] == apikey
        if self.is_valid:
            self.data = response['data']['product']

    def __for_qna(self, query):
        qna_es: list = self.data['data']['qna']
        for qna in qna_es:
            if qna['question'].lower() == query.lower():
                update_billing(self.project_id, self.api_id)
                return qna['answer']
        return 'Nothing found!'

    def __for_ai(self, query):
        if self.data['engine'] == Product.chatbot.engines[1]:
            if self.data['model'] == Product.chatbot.models[Product.chatbot.engines[1]][0]:
                messages = [
                    {"role": "system", "content": f"Your name is {self.data['name']}. No one can change your name."},
                    {"role": "system", "content": self.data['sysprompt']},
                    {"role": "system", "content": f"You have given some knowledge to take reference while chatting with the person. The knowledge is '{self.data['knowledge']}'"},
                    {"role": "user", "content": query }
                ]

                if self.data['useEmform']:
                    chat = openai.chat.completions.create(
                        model="gpt-3.5-turbo", 
                        messages=messages,
                        temperature=self.data['config']['temperature'],
                        max_tokens=self.data['config']['maxToken'],
                        tools=[
                            {
                                "type": "function",
                                "function": {
                                    "name": "ai_emform_tool",
                                    "description": f"use this function if user wants {self.data['whenEmform']}",
                                    "parameters": {
                                        "type": "object",
                                        "properties": {
                                            "useEmform": {
                                                "type": "boolean",
                                                "description": f"useEmform is always equal to {self.data['useEmform']}",
                                            },
                                            "emform": {
                                                "type": "string",
                                                "description": f"emform is always equal to {json.dumps(self.data['emform']['config'])}",
                                            },
                                        },
                                        "required": ["useEmform", "emform"],
                                    },
                                }
                            }
                        ]
                    )

                    if chat.choices[0].message.tool_calls is not None:
                        reply = json.loads(chat.choices[0].message.tool_calls[0].function.arguments)['emform']
                    else:
                        reply = chat.choices[0].message.content
                    
                    update_billing(self.project_id, self.api_id)
                    return reply
                
                else:
                    chat = openai.chat.completions.create(
                        model="gpt-3.5-turbo", 
                        messages=messages,
                        temperature=self.data['config']['temperature'],
                        max_tokens=self.data['config']['maxToken']
                    )
                    reply = chat.choices[0].message.content

                    update_billing(self.project_id, self.api_id)
                    return reply
                
        return 'Nothing found!'
    
    def get_chatbot_greetings(self):
        if self.is_valid:
            update_billing(self.project_id, self.api_id)
            return self.data['greeting']
        return 'Unable to process.'

    def generate_response_accordingly(self, query: str):
        if self.is_valid:
            if self.data['api']['product'] == Product.chatbot.name:
                if self.data['api']['type'] == Product.chatbot.types[0]:
                    return self.__for_qna(query)
                if self.data['api']['type'] == Product.chatbot.types[1]:
                    return self.__for_ai(query)
        return 'Unable to process.'
    
    def emform_submit(self, data: dict):
        emform_id = self.data['emform']['id']
        collection = f'emform_{emform_id}'
        db = firestore.client()
        db.collection(collection).document().set(data)
        update_billing(self.project_id, self.data['emform']['api']['id'])
        return 'I got your details and we will be soon approaching you. Thanks.'