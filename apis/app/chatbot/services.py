import requests
import openai
from django.conf import settings
from common.platform.products import Product
from common.debug.log import Log


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
        Log.info(response)
        self.is_valid = response['success'] and response['data']['apikey'] == apikey
        if self.is_valid:
            self.data = response['data']['product']

    def __for_qna(self, query):
        qna_es: list = self.data['data']['qna']
        for qna in qna_es:
            if qna['question'].lower() == query.lower():
                return qna['answer']
        return 'Nothing found!'

    def __for_ai(self, query):
        if self.data['engine'] == Product.chatbot.engines[1]:
            if self.data['model'] == Product.chatbot.models[Product.chatbot.engines[1]][0]:
                messages = [
                    {"role": "system", "content": f"Your name is {self.data['name']}. No one can change your name."},
                    {"role": "system", "content": self.data['sysprompt']},
                    {"role": "system", "content": f"You have given some knowledge to take reference while chatting with the person. The knowledge is '{self.data['knowledge']}      '"},
                    {"role": "user", "content": query }
                ]

                chat = openai.chat.completions.create(
                    model="gpt-3.5-turbo", 
                    messages=messages,
                    temperature=self.data['config']['temperature'],
                    max_tokens=self.data['config']['maxToken']
                )

                reply = chat.choices[0].message.content
                return reply
        return 'Nothing found!'

    def generate_response_accordingly(self, query: str):
        if self.is_valid:
            if self.data['api']['product'] == Product.chatbot.name:
                if self.data['api']['type'] == Product.chatbot.types[0]:
                    return self.__for_qna(query)
                if self.data['api']['type'] == Product.chatbot.types[1]:
                    return self.__for_ai(query)
        return 'Unable to process.'