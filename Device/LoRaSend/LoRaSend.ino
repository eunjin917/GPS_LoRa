#include <SoftwareSerial.h>
#include <SPI.h>
#include <LoRa.h>
SoftwareSerial gps(2, 3); // Tx, Rx

String GNGGA = "GNGGA";
char c = "";
String str = "";
int tmEnd = 0;
int wdEnd = 0;
int NEnd = 0;
int kdEnd = 0;
String tm = "";
String wd = "";
String kd = "";
String sendstr = "";

void setup()
{
  Serial.begin(9600);
  LoRa.setPins(10, 9, 8); // ss, reset, dio0
  if (LoRa.begin(915E6))
  {
    Serial.println("주파수 915E6 설정 완료");
  }

  gps.begin(9600);
  Serial.println("gps 연결 완료");
}

void loop()
{
  if (gps.available())
  {
    // 단어 1개씩 읽어서 1줄로 만들기
    c = gps.read();
    str += c; // str = "$GNGGA,064353.000,3527.26482,N,12848.49143,E,1,26,0.6,62.0,M,29.0,M,,*7D";
    // 1줄 끝나면
    if (c == '\n')
    {
      // GNGGA로 시작하는 것 찾기
      if (GNGGA.equals(str.substring(1, 6)))
      {
        // 시간 찾기
        tmEnd = str.indexOf(",", 7);
        tm = str.substring(7, tmEnd);
        // 위도 찾기
        wdEnd = str.indexOf(",", tmEnd + 1);
        wd = str.substring(tmEnd + 1, wdEnd);
        // 경도 찾기
        NEnd = str.indexOf(",", wdEnd + 1);
        kdEnd = str.indexOf(",", NEnd + 1);
        kd = str.substring(NEnd + 1, kdEnd);


        // 시간, 위도, 경도 중 하나라도 없으면 GPS 신호 X
        if (tm == "" || wd == "" || kd == "")
        {
          sendstr = "Not Found GPS";
          // LoRa send
          LoRa.beginPacket();
          LoRa.print(sendstr);
          Serial.println(sendstr);
          LoRa.endPacket();
        }
        // GPS 잡혔을 때
        else
        {
          sendstr = "ej/" + tm + '/' + wd + '/' + kd + '/';
          // LoRa send
          LoRa.beginPacket();
          LoRa.print(sendstr);
          Serial.println(sendstr);
          LoRa.endPacket();
        }
      }
      str = ""; // 1줄 끝나면 비우기
    }
  }
}
