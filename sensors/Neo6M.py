from __future__ import annotations

import asyncio
import io
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
        self.sio = io.TextIOWrapper(io.BufferedRWPair(self.serial, self.serial))
        self.reader = pynmea2.NMEAStreamReader()
        super().__init__()



    async def poll(self) -> dict[str, int | float]:
        """
        Poll the sensor for data, and return a dictionary of the data. If this function fails,
         the sensor will be marked as "damaged" using exponential falloff

        :return: the data e.x. {"temperature": 34.7, "pressure": 106.4, "humidity": 0.56}
        """

        while 1:
            try:
                line = self.sio.readline()
                msg = pynmea2.parse(line)
                self.logger.critical(repr(msg))
            except serial.SerialException as e:
                self.logger.critical('Device error: {}'.format(e))
                break
            except pynmea2.ParseError as e:
                self.logger.critical('Parse error: {}'.format(e))
                continue
        return {"finished": 1}

