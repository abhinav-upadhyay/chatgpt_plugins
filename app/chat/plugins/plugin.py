from abc import ABC, abstractmethod
from typing import Dict

class PluginInterface(ABC):

    @abstractmethod
    def get_name(self) -> str:
        """
        return the name of the plugin (should be snake case)
        """
        pass

    @abstractmethod
    def get_description(self) -> str:
        """
        return a detailed description of what the plugin does
        """
        pass

    @abstractmethod
    def get_parameters(self) -> Dict:
        """
        Return the list of parameters to execute this plugin in the form of
        JSON schema as specified in the OpenAI documentation:
        https://platform.openai.com/docs/api-reference/chat/create#chat/create-parameters
        """
        pass
    
    @abstractmethod
    def execute(self, **kwargs) -> Dict:
        """
        Execute the plugin and return a JSON serializable dict.
        The parameters are passed in the form of kwargs
        """
        pass
