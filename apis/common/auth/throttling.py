from rest_framework.throttling import AnonRateThrottle

class ChatbotThrottle(AnonRateThrottle):
    scope = 'chatbot'