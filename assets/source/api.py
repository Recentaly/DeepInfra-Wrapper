# ---------------------------------------- IMPORTS ---------------------------------------- #

# this module allows us to get the headers from the get_headers function
from .headers.get_headers import get_headers

# this module allows us to get a random user agent
from fake_useragent import UserAgent

# this module allows us to generate random numbers
import secrets

# to make requests
import requests

# ---------------------------------------- FUNCTIONS ---------------------------------------- #
def non_streamed_format(model: str, content: str) -> dict[str]:

    return {
        "object": "chat.completion",
        "model": f"{model}",
        "choices": [{
            "index": 0,
            "message": {
                "role": "assistant",
                "content": f"{content}",
            },
            "finish_reason": "stop",
        }],
    }
# ---------------------------------------- API CLASS ---------------------------------------- #

class Api(object):

    # initialize the class and set some variables here
    def __init__(self) -> None:

        """initialize the class"""
        
        self.url: str = "https://api.deepinfra.com/v1/openai/chat/completions"

        self.headers = get_headers(UserAgent().random, secrets.randbelow(1000)) # get random headers

        self.session = requests.Session()

        # write some configuration here
        self.config = {
            'temperature': 1,
            'frequency_penalty': 0,
            'presence_penalty': 0,
            'repetition_penalty': 1,

            'top_p': 1,
            'top_k': 0,


            'max_tokens': 150,
            'stop': [''],

        }

        # codec for encoding and decoding
        self.codec = 'utf-8'

    def get_models(self) -> dict[list[str, str]]:

        """get all models"""

        return {'data': [
            {"id": "meta-llama/Llama-2-70b-chat-hf (keyword: gpt)"},
            {"id": "meta-llama/Llama-2-13b-chat-hf (keyword: gpt)"},
            {"id": "meta-llama/Llama-2-7b-chat-hf (keyword: gpt)"},
            {"id": "codellama/CodeLlama-34b-Instruct-hf (keyword: gpt)"},
            {"id": "jondurbin/airoboros-l2-70b-gpt4-1.4.1 (keyword: gpt)"},
            {"id": "mistralai/Mistral-7B-Instruct-v0.1 (keyword: gpt)"},
        ]}
    

    def chat(self, messages: list, model: str, stream: bool = True) -> str:

        """chat with the api"""

        # compile the data
        data = {
            'messages': messages,
            'model': model,
            'stream': stream,

            'temperature': self.config['temperature'],
            'max_tokens': self.config['max_tokens'],

            'top_p': self.config['top_p'],
            'top_k': self.config['top_k'],

            'presence_penalty': self.config['presence_penalty'],
            'frequency_penalty': self.config['frequency_penalty'],
        }

        # make a post request to the api
        with self.session.post(self.url, headers=self.headers, json=data) as response:

            # raise for status
            response.raise_for_status()

            # iterate over the response
            for chunk in response.iter_lines():

                # check if chunk is not empty
                if chunk:

                    # only yield if streaming is on
                    if stream:

                        # yield the chunk of the full response
                        yield chunk # already in correct OpenAI format

        # close the session and make a new one
        self.session.close()
        self.session = requests.Session()

# Path: assets/source/api.py