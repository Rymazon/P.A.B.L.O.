#include <Servo.h>
const unsigned int MAX_MESSAGE_LENGTH = 12;
Servo baseservo;
Servo balldropper;
//const int LED = 11;
const double offset = 45;
void setup()
{
  Serial.begin(9600);
  baseservo.attach(9);
  //pinMode(LED,OUTPUT);
  balldropper.attach(11);
 // baseservo.write(90)
}

void loop()
{
balldropper.write(180);

 //// rotationnnnnnnnnnnnnnnnnnnnnnnnnnnn
  while(Serial.available())
  {
    static char message[MAX_MESSAGE_LENGTH];
    static unsigned int message_pos = 0;

    char inByte = Serial.read();
    
    if ( inByte != '\n' && (message_pos < MAX_MESSAGE_LENGTH - 1) )
    {
      //Add the incoming byte to message
      message[message_pos] = inByte;
      message_pos++;
    }
    //Full message received...
    else
    {
      //Add null character to string
      message[message_pos] = '\0';

      //
      int int_value = atoi(message); 
      double angle = ((1 - int_value / 255.0)  * 180)*0.4 + 180*0.3;
      baseservo.write(angle);
      delay(100);
      balldropper.write(0);
      delay(45);
      balldropper.write(180);
    }
 

  }
  

}