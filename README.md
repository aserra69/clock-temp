# clock-temp
Frustrated with not having a visible clock and wanting to show exatly how hot my office was getting, I hacked this together over a weekend of spare parts I had in my kit.  It uses:
  Pi Zero W
  Adafruit 7-Segment display (http://adafru.it/812)
  BMP180 sensor
  button (220 ohm resistor) connected to GPIO17 to allow for proper shutdown of piZeroW when needing to unplug
  
Libraries are:
  
  seven segment backpack: git clone https://github.com/adafruit/Adafruit_Python_LED_Backpack.git
  
  BMP180: git clone https://github.com/adafruit/Adafruit_Python_BMP.git
  
And this from a Pi prompt:
  
  git clone https://github.com/aserra69/clock-temp.git
  cd clock-temp
  sudo python ClockTemp.py
