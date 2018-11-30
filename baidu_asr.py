import os
import requests
import base64
import json

auth_params = {
    'APPID': 'xxxx',
    'APIKey': 'xxxx',
    'SecretKey': 'xxxxx'
}
# 获取接入信息
# get the access information
url = 'https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials\
&client_id={}&client_secret={}'.format(auth_params['APIKey'], auth_params['SecretKey'])
access_info = requests.get(url).json()
access_token = access_info['access_token']

def get_content(file_name):
    with open(file_name, 'rb') as wav_file:
        wav = wav_file.read()
    b64wav = base64.b64encode(wav)
    params = {
        'format': 'wav',
        'rate': '16000',
        'channel': '1',
        'cuid': 'just_a_id',
        'token': access_token,
        'speech': b64wav.decode('ascii'),
        'len': len(wav) # 原生音频长度，单位byte; Length (byte) of raw wav file
    }
    r = requests.post('http://vop.baidu.com/server_api', data=json.dumps(params))
    return r.json()
    # r['err_msg'] == 'sucess.'代表返回成功
    # r['result']是识别出来的文字
    # r['err_msg'] == 'sucess.' means return sucessfully
    # r['result'] is the returned text
    


