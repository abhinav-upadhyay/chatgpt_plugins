import openai
import requests
import json
from typing import List, Dict
import uuid
from .plugins.plugin import PluginInterface
from .plugins.websearch import WebSearchPlugin
from .plugins.webscraper import WebScraperPlugin
from .plugins.pythoninterpreter import PythonInterpreterPlugin

GPT_MODEL = "gpt-3.5-turbo-0613"
SYSTEM_PROMPT = """
    You are a helpful AI assistant. You answer the user's queries.
    When you are not sure of an answer, you take the help of functions provided to you.
    NEVER make up an answer if you don't know, just respond with "I don't know" when you don't know.
"""

class Conversation:
    """
    This class represents a conversation with the ChatGPT model.
    It stores the conversation history in the form of a list of messages.
    """
    def __init__(self):
        self.conversation_history: List[Dict] = []

    def add_message(self, role, content):
        message = {"role": role, "content": content}
        self.conversation_history.append(message)
    

class ChatSession:
    
    def __init__(self):
        self.session_id = str(uuid.uuid4())
        self.conversation = Conversation()
        self.plugins: Dict[str, PluginInterface] = {}
        self.register_plugin(WebSearchPlugin())
        self.register_plugin(WebScraperPlugin())
        self.register_plugin(PythonInterpreterPlugin())
        self.conversation.add_message("system", SYSTEM_PROMPT)
    
    def register_plugin(self, plugin: PluginInterface):
        """
        Register a plugin for use in this session
        """
        self.plugins[plugin.get_name()] = plugin
    
    def get_messages(self) -> List[Dict]:
        """
        Return the list of messages from the current conversaion
        """
        if len(self.conversation.conversation_history) == 1:
            return []
        return self.conversation.conversation_history[1:]
    
    def _get_functions(self) -> List[Dict]:
        """
        Generate the list of functions that can be passed to the chatgpt
        API call.
        """
        return [self._plugin_to_function(p) for p in self.plugins.values()]

    def _plugin_to_function(self, plugin: PluginInterface) -> Dict:
        """
        Convert a plugin to the function call specification as required by 
        the ChatGPT API:
        https://platform.openai.com/docs/api-reference/chat/create#chat/create-functions
        """
        function = {}
        function["name"] = plugin.get_name()
        function["description"] = plugin.get_description()
        function["parameters"] = plugin.get_parameters()
        return function
    
    def _execute_plugin(self, func_call) -> str:
        func_name = func_call.get("name")
        if func_name in self.plugins:
            arguments = json.loads(func_call.get("arguments"))
            plugin_response = self.plugins[func_name].execute(**arguments)
        else:
            plugin_response = {"error": f"No plugin found with name {func_call}"}
        messages = list(self.conversation.conversation_history)
        messages.append({"role": "function", "content": json.dumps(plugin_response), "name": func_name})
        next_chatgpt_response = self._chat_completion_request(messages)
        if next_chatgpt_response.get("function_call"):
            return self._execute_plugin(next_chatgpt_response.get("function_call"))
        return next_chatgpt_response.get("content")


    def get_chatgpt_response(self, user_message: str) -> str:
        self.conversation.add_message("user", user_message)
        try:
            chatgpt_response = self._chat_completion_request(self.conversation.conversation_history)
            if chatgpt_response.get("function_call"):
                chatgpt_message = self._execute_plugin(chatgpt_response.get("function_call"))
            else:
                chatgpt_message = chatgpt_response.get("content")
            self.conversation.add_message("assistant", chatgpt_message)
            return chatgpt_message
        except Exception as e:
            print(e)
            return "something went wrong"

    def _chat_completion_request(self, messages: List[Dict]):
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + openai.api_key,
        }
        json_data = {"model": GPT_MODEL, "messages": messages, "temperature": 0.7}
        if self.plugins:
            json_data.update({"functions": self._get_functions()})
        try:
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=json_data,
            )
            return response.json()["choices"][0]["message"]
        except Exception as e:
            print("Unable to generate ChatCompletion response")
            print(f"Exception: {e}")
            return e

