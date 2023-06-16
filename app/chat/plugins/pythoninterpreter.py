from .plugin import PluginInterface
from typing import Dict
from io import StringIO
import sys
import traceback



class PythonInterpreterPlugin(PluginInterface):
    def get_name(self) -> str:
        """
        return the name of the plugin (should be snake case)
        """
        return "python_interpreter"
    
    def get_description(self) -> str:
        return """
        Execute the given python code return the result from stdout.
        """
    

    def get_parameters(self) -> Dict:
        """
        Return the list of parameters to execute this plugin in
        the form of JSON schema as specified in the
        OpenAI documentation:
        https://platform.openai.com/docs/api-reference/chat/create#chat/create-parameters
        """
        parameters = {
            "type": "object",
            "properties": {
                "code": {
                    "type": "string",
                    "description": "Python code which needs to be executed"
                }
            }
        }
        return parameters
    
    def execute(self, **kwargs) -> Dict:
        """
        Execute the plugin and return a JSON response.
        The parameters are passed in the form of kwargs
        """
        output = StringIO()
        # import pdb; pdb.set_trace()

        try:
            global_namespace = {}
            local_namespace = {}
            sys.stdout = output
            exec(kwargs['code'], local_namespace, global_namespace)
            result = output.getvalue()
            if not result:
                return {'error': 'Not result written to stdout. Please print result on stdout'}
            return {"result": result}
        except Exception:
            error = traceback.format_exc()
            return {"error": error}
        finally:
            sys.stdout = sys.__stdout__


        
