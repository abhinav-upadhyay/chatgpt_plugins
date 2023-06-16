# ChatGPT Plugins using the Function Call Feature

The introduction of the function call features in the chat completions API of OpenAI opens up the possibilities of implmenting plugins similar to the plugins supported in ChatGPT. However,
OpenAI documentation does not show how this can be done. I took the opportunity to try to do this myself by building a chat application powered by GPT and then using the function call
feature to design and implment plugins.

This repo contains code for a [tutorial on building ChatGPT like plugins using the newly introduced function call feature.](https://codeconfessions.substack.com/p/creating-chatgpt-plugins-using-the)
In this tutorial we build a Flask based chat application using the ChatGPT APIs and then proceed to implement a web browsing and Python code interpreter plugin. 

Full write up for this tutorial available on my substack: [https://codeconfessions.substack.com/p/creating-chatgpt-plugins-using-the](https://codeconfessions.substack.com/p/creating-chatgpt-plugins-using-the)


## Structure of a Plugin
Creating a plugin in this system requires doing two things. 
- Extend the PluginInterface class, which defines the API that a plugin should follow
- Implement the 4 API methods expected by a plugin. These are:
  - get_name: Returns the name of the plugin
  - get_description: Provides a description of what the plugin does
  - get_parameters: Gives a JSON specification of the parameters of the plugin.
  - execute: This is the meat of the plugin, where it receives the parameters as declared by it in the get_parameters method and it executes its function.

Checkout the implmenetation of the [web search plugin](https://github.com/abhinav-upadhyay/chatgpt_plugins/blob/ee8d81ec3729b7cdc5f34b75f51ce44fa93ee18a/app/chat/plugins/websearch.py) for an example.


## Setup Requirements for Running This Locally
Install following Python packages in a virtual environment:

```shell
pip install openai --upgrade
pip install flask requests python-dotenv
```

### Create an OpenAI API Key
- Create an OpenAI account and generate a key from their accounts page: [https://platform.openai.com/account/api-keys](https://platform.openai.com/account/api-keys)
- Put the generated API key in the .env file in the root directory of your project as follows:
```shell
OPEN_AI_KEY="<your api key here>"
```

### Create Brave Search API Key
This is required for the web search/browser plugin. For this, you need to create an account with Brave at: [https://brave.com/search/api/](https://brave.com/search/api/). Next, you need to create an API key from Brave. You can select the Free plan to start with. The free plan allows 2000 requests per month. Once you have generated the key, put this also in the `.env` file as shown below:
```shell
BRAVE_API_KEY="<your Brave API key>"
```
### Generating a key for Flask
Flask also needs a secret key in order to create a user session. You can use something like uuid to generate the key. For example:
```python
import uuid
print(str(uuid.uuid4()))
```
Put the generated value from the above code in the .env, as shown below:
```shell
CHAT_APP_SECRET_KEY="<your secret key>"
```

## Running the Application
Use the following command to run the application:
```shell
flask --app run.py run
```

## Demo
Following is the web search plugin in action:
![Web search plugin in action](https://github.com/abhinav-upadhyay/chatgpt_plugins/blob/2388cb60ea93286127228a9145bef91482b5fbad/web-search-plugin-demo.gif)

