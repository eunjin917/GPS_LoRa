#include <SPI.h>
#include <LoRa.h>

void setup()
{
  Serial.begin(9600);
  LoRa.setPins(10, 9, 8); // ss, reset, dio0
  if (LoRa.begin(915E6))
  {
    Serial.println("주파수 915E6 설정 완료");
  }
}

void loop()
{
  int packetSize = LoRa.parsePacket();
//  Serial.println(LoRa.rssi());
//  Serial.println(packetSize);
  if (packetSize)
  {
    while (LoRa.available())
    {
      Serial.print((char)LoRa.read());
    }
    Serial.println();
  }
}
