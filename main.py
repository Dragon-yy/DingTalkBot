from dingtalkchatbot.chatbot import DingtalkChatbot, ActionCard, CardItem
import os
import sys
import hmac
import hashlib
import base64
current_dir = os.getcwd()    # obtain work dir
sys.path.append(current_dir) # add work dir to sys path
from config.base_settings import *
from utils.chatgpt import openai_chat_http_api
from flask import Flask, request, jsonify
import hmac
import hashlib
import base64
from loguru import logger

app = Flask(__name__)



@app.route('/', methods=['POST', 'GET'])
def robot():
    if request.method == 'POST':
        http_sign = request.headers.get('SIGN')
        http_timestamp = request.headers.get('TIMESTAMP')
        res = request.json
        print(res)
        # 用户输入钉钉的信息
        content = res.get("text", {}).get("content", "")

        string_to_sign = '{}\n{}'.format(http_timestamp, APP_SECRET)
        string_to_sign_enc = string_to_sign.encode('utf-8')
        hmac_code = hmac.new(APP_SECRET.encode("utf-8"), string_to_sign_enc, digestmod=hashlib.sha256).digest()
        sign = base64.b64encode(hmac_code).decode("utf-8")
        logger.info("sign {}".format(sign))
        logger.info("http_sign {}".format(http_sign))
        # 验证签名是否为钉钉服务器发来的
        if sign == http_sign:
            '''
            可以写一些执行逻辑，返回用户想要的信息，比如工资信息，可以去数据库查工资信息回给钉钉用户
            '''
            if "帮助" in content:
                 return jsonify({
                    "msgtype": "text",
                    "text": {
                        "content": "谢谢使用，此GPT3.5机器人，由阿龙开发".format(content)
                    }
                })
            else:
                return jsonify(
                    {
                        "msgtype": "text",
                        "text": {
                            "content": openai_chat_http_api("你是谁，是什么模型")
                        }
                    }
                )
        logger.error("签名验证失败")
        return jsonify({"error": "你没有权限访问此接口"}), 403
    elif request.method == 'GET':
        return "hello"




if __name__ == '__main__':
    # loguru日志保存
    logger.add('logs/log.log', rotation="100 MB")
    logger.add('logs/error.log', rotation="100 MB", retention="10 days", level="ERROR")
    logger.add('logs/info.log', rotation="100 MB", retention="10 days", level="INFO")
    
    app.run(debug=True,port=5001)
