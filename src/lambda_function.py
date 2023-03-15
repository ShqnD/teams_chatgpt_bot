# coding:utf-8

import logging
import traceback
import os
import json
import openai

def getLogLevel(level:str):
    if level == 'info':
        return logging.INFO
    elif level == 'warn':
        return logging.WARN
    elif level == 'error':
        return logging.ERROR
    else:
        return logging.DEBUG

logger = logging.getLogger()
logger.setLevel(getLogLevel(os.environ['LOG_LEVEL']))

openai.api_key = os.environ['API_KEY']
BOT_NAME = os.environ['BOT_NAME']

def lambda_handler(event, context):
    try:
        logger.debug(event)
        bot_name = os.environ['BOT_NAME']
        body = json.loads(event['body'])
        text = body['text'].replace(bot_name, '').replace('@', '').strip()
        
        logger.debug(text)

        user_name = body['from']['name']

        msg = user_name + 'さん<br>'
       
        msg += chatgpt_response(text)

        payload = {
            'type': 'message',
            'text': msg.replace('。', '。<br>').replace('！', '！<br>').replace('♪', '♪<br>')
        }
        
        logger.debug(msg)
        
        response = {
            'statusCode': 200,
            'body': json.dumps(payload)
        }
        
        return response
        
    except:
        logger.error(traceback.format_exc())
        error_message = ''
        response = {
            'statusCode': 403,
            'body': json.dumps(error_message)
        }
        return response

def chatgpt_response(text) -> str:
    # 性格付け
    system_content = rf'あなたはChatbotとしてアドバイスをします。'\
    + rf'以下の制約条件を厳密に守ってアドバイスをしてください。'\
    + rf'制約条件:' \
    + rf'* Chatbotの名前は、{BOT_NAME}です。' \
    + rf'* {BOT_NAME}は日本語を話します。'\
    + rf'* {BOT_NAME}は丁寧ですが愛嬌もあります。'\
    + rf'* {BOT_NAME}は時々冗談を言います。'
 
    # 応答作成
    response = openai.ChatCompletion.create(model='gpt-3.5-turbo',messages=[{'role': 'system', 'content': system_content},{'role': 'user', 'content': text}])
    return_text = response["choices"][0]["message"]["content"].strip()

    return return_text
