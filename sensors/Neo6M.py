from __future__ import annotations

import asyncio
from random import randint

import pynmea2

from Sensor import Sensor
import serial



class Neo6M(Sensor):
    # Metadata
    id: str = "gps"  # Program ID for this sensor (e.g. bmp180)
    name: str = "NEO6M (gps)" # Human-readable name (e.g. BMP180 Pressure/Temperature/Humidity Sensor)
    description: str = "to return GPS information"  # Purpose of the sensor (e.g. Read pressure, temperature, and humidity)
    cooldown: float = 1  # How many seconds in between data polls (e.g. 7.5 seconds)


    def __init__(self):
        """
        Sensors use this function to create all necessary
         attributes and connections necessary to interface with the sensor
        :return: None
        """
        self.port = "/dev/ttyAMA0"
        self.serial = serial.Serial(self.port, baudrate=9600, timeout=0.5)
        self.reader = pynmea2.NMEAStreamReader()
        super().__init__()



    async def poll(self) -> dict[str, int | float]:
        """
        Poll the sensor for data, and return a dictionary of the data. If this function fails,
         the sensor will be marked as "damaged" using exponential falloff

        :return: the data e.x. {"temperature": 34.7, "pressure": 106.4, "humidity": 0.56}
        """

        while True:
            newdata = self.serial.readlines()
            for line in newdata:
                if line[0:6] == "$GPRMC":
                    newmsg = pynmea2.parse(line)
                    lat = newmsg.latitude
                    lng = newmsg.longitude
                    return {"latitude": lat, "longitude": lng}


