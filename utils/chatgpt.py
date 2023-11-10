import requests
import os
import sys
import json
 
current_dir = os.getcwd()    # obtain work dir
sys.path.append(current_dir) # add work dir to sys path
from config.base_settings import CHATGPT_URL,CHATGPT_TOKEN
from loguru import logger



def openai_http_api(message):
    model = "text-davinci-003"

    url = 'https://{}/v1/completions'.format(CHATGPT_URL)
    headers = {
        "Authorization": "Bearer " + CHATGPT_TOKEN,
        "Content-Type": "application/json"
    }
    data = {
        "model": model,
        "prompt": message,
        "temperature": 0.8,
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    print(response.json())
    print(response.json()['choices'][0]['text'])
    return response.json()['choices'][0]['text']


def openai_stream_chat_http_api(message):
    model = "gpt-3.5-turbo"

    url = 'https://{}/v1/chat/completions'.format(CHATGPT_URL)
    headers = {
        "Authorization": "Bearer " + CHATGPT_TOKEN,
        "Content-Type": "application/json"
    }
    data = {
        "model": model,
        "messages": [{"role": "user", "content": message}],
        "temperature": 0.8,
        "stream": True
    }
    response = requests.post(url, headers=headers, json=data, stream=True, verify=False)
    for chunk in response.iter_lines():
        response_data = chunk.decode("utf-8").strip()
        if not response_data:
            continue
        try:
            if response_data.endswith("data: [DONE]"):
                break
            data_list = response_data.split("data: ")
            if len(data_list) > 2:
                json_data = json.loads(data_list[2])
            else:
                json_data = json.loads(response_data.split("data: ")[1])
            if 'content' in json_data["choices"][0]["delta"]:
                msg = json_data["choices"][0]["delta"]['content']
                print(msg, end='', flush=True)
        except:
            logger.error('json load error:', response_data)


def openai_chat_http_api(message):
    model="gpt-3.5-turbo"
    url = 'https://{}/v1/chat/completions'.format(CHATGPT_URL)
    headers = {
        "Authorization": "Bearer " + CHATGPT_TOKEN,
        "Content-Type": "application/json"
    }
    data = {
        "model": model,
        "messages": [{"role": "user", "content": message}],
        "temperature": 0.8,
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    logger.info(response.json()['choices'][0]['message']['content'])
    return response.json()['choices'][0]['message']['content']

if __name__ == "__main__":
    openai_chat_http_api("你是谁，是什么模型")