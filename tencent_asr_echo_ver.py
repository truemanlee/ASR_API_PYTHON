# coding=utf-8
# 腾讯的echo版本语音识别api
# ASR api of Tencent with echo version

import hashlib
import time
import random
import string
import requests
import base64
from urllib.parse import quote

APPID = 'xxx' # APPID
APPKEY = 'XXXX' # APPKEY

def curlmd5(src):
    m = hashlib.md5(src.encode('utf-8'))
    return m.hexdigest().upper()

def get_params(file_name):
    # file_name: 字符串，包含完整的文件路径，例如'/home/lichm/data/sample.wav'
    # file_name: string, full path of the wav file, such as '/home/lichm/data/sample.wav'
    assert(file_name.split('.')[-1] == 'wav')
    with open(file_name, 'rb') as wav_file:
        wav = wav_file.read()
    b64wav = base64.b64encode(wav)
    # 时间戳
    # time_stamp
    t = time.time()
    time_stamp=str(int(t))
    nonce_str = ''.join(random.sample(string.ascii_letters + string.digits, 10))
    # 所有参数; All parametres that we need
    params = {
        'app_id': APPID,
        'time_stamp': time_stamp,
        'nonce_str': nonce_str,
        'speech': b64wav.decode('utf-8'),
        'rate':'16000',
        'format': '2'
    } # 更多信息请参考腾讯AI开放平台; Parametres information can be found in the website of Tencent open AI platform
    
    # 签名机制; Signature
    for key in sorted(params):
        sign_before += '{}={}&'.format(key, quote(params[key], safe=''))
    sign_before += 'app_key={}'.format(APPKEY)
    sign = curlmd5(sign_before)
    params['sign'] = sign
    return params
    
def get_content(plus_item):
    url = 'https://api.ai.qq.com/fcgi-bin/aai/aai_asr'
    plus_item = plus_item.encode('utf-8')
    payload = get_params(plus_item)
    r = requests.post(url, data=payload).json()
    return r['data'], r['ret']
    # 若成功识别，r['ret']==0;
    # if sucess, r['ret']==0
