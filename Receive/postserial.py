from serial import Serial   # pip install pyserial
import requests

# 시리얼통신
ser = Serial('COM7', 9600)
while True:
    if ser.readable(): 
        info = ser.readline().decode()  # "ej/00:00:00/3527.26482/12848.49143"
        # 유효한 정보만 골라내기
        if info[:2] == "ej":
            # 서버에 POST통신
            data = {
                "info":info
            }
            url = "https://eunjinit-ytflh.run.goorm.io/receivepage"
            response = requests.post(url, data)
            print(response)
        print(info)