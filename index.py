import requests
import json
from utils import *
apikey = "42a3250f51524e4cab1e2fe7e2a4d115"
serviceId = 195

def reg_truecaller():

    phone = None
    request_id = None
    for i in range(3):
        phone, request_id = get_phone_number(apikey, serviceId)
        if phone:
            break
    if not phone:
        return      
    url = "https://account-asia-south1.truecaller.com/v2/sendOnboardingOtp"

    phoneNumber = f"+84{phone}"
    print("start: ",phoneNumber)
    device = get_random_device()

    payload_get_code = json.dumps({
    "countryCode": "VN",
    "dialingCode": 84,
    "installationDetails": {
        "app": {
        "buildVersion": 5,
        "majorVersion": 11,
        "minorVersion": 7,
        "store": "GOOGLE_PLAY"
        },
        "device": {
        "deviceId": generate_random_string(16),
        "language": "en",
        "manufacturer": device["manufacturer"],
        "model": device["model"],
        "osName": "Android",
        "osVersion": "10",
        "mobileServices": [
            "GMS"
        ]
        },
        "language": "en"
    },
    "phoneNumber": phoneNumber,
    "region": "region-2",
    "sequenceNo": 2
    })

    headers = {
    'user-agent': f'Truecaller/11.75.5 (Android;10)',
    'clientsecret': 'lvc22mp3l1sfv6ujg83rd17btt',
    'Content-Type': 'application/json'
    }
    response = requests.post(url, headers=headers, data=payload_get_code)
    res = response.json()
    print(res)
    requestId = res.get('requestId')
    ## get code 
    code = get_otp(apikey, request_id)
    print('code: ',code)
    url_verify = "https://account-asia-south1.truecaller.com/v1/verifyOnboardingOtp"
    payload = json.dumps({
        "countryCode": "VN",
        "dialingCode": 84,
        "phoneNumber": phoneNumber,
        "requestId": requestId,
        "token": code
    })
    headers = {
    'user-agent': 'Truecaller/11.75.5 (Android;10)',
    'clientsecret': 'lvc22mp3l1sfv6ujg83rd17btt',
    'Content-Type': 'application/json'
    }
    response = requests.post(url_verify, headers=headers, data=payload)
    res_verify = response.json()
    open('data_token.txt', 'a+').write(json.dumps(res_verify) + '\n')
    token = res_verify.get('installationId')
    if token:
        print(f'==> Reg successfully account: {phone}')
    else:
        print(f'==> Reg failed account: {phone}')
# reg_truecaller()

# for i in range(110):
#     reg_truecaller()
#     time.sleep(1)

import threading
def reg_acc_main():
    while True:
        reg_truecaller()
        time.sleep(2)

so_luong = 1
for vi_tri in range(so_luong):
    threading.Thread(target=reg_acc_main, args={}).start()
    time.sleep(1)