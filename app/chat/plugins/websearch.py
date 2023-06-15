from .plugin import PluginInterface
from typing import  Dict
import requests
import os

BRAVE_API_KEY = os.getenv("BRAVE_API_KEY")
BRAVE_API_URL = "https://api.search.brave.com/res/v1/web/search"


class WebSearchPlugin(PluginInterface):
    def get_name(self) -> str:
        """
        return the name of the plugin (should be snake case)
        """
        return "websearch"
    
    def get_description(self) -> str:
        return "Executes a web search for the given query and returns a list of snipptets of matching text from top 10 pages"
    

    def get_parameters(self) -> Dict:
        """
        Return the list of parameters to execute this plugin in the form of
        JSON schema as specified in the OpenAI documentation:
        https://platform.openai.com/docs/api-reference/chat/create#chat/create-parameters
        """
        parameters = {
            "type": "object",
            "properties": {
                "q": {
                    "type": "string",
                    "description": "the user query"
                }
            }
        }
        return parameters
    
    def execute(self, **kwargs) -> Dict:
        """
        Execute the plugin and return a JSON response.
        The parameters are passed in the form of kwargs
        """

        headers = {
            "Accept": "application/json",
            "X-Subscription-Token": BRAVE_API_KEY
        }
        import pdb; pdb.set_trace()

        params = {
            "q": kwargs["q"]
        }

        response = requests.get(BRAVE_API_URL, headers=headers, params=params)

        if response.status_code == 200:
            results = response.json()['web']['results']
            urls = [r['description'] for r in results]
            return {"web_search_results": urls}
        else:
            return {"error": f"Request failed with status code: {response.status_code}"}
        
