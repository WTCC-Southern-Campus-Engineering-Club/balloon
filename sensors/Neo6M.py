from __future__ import annotations

import asyncio
import io
import traceback
from random import randint

import pynmea2

from Sensor import Sensor
import serial



class Neo6M_GPS(Sensor):
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
        try:
            self.serial = serial.Serial(self.port, baudrate=9600, timeout=0.5)
        except serial.SerialException:
            raise FileNotFoundError(f"Neo6M serial port ({self.port}) not found. This is a critical error.")
        self.sio = io.TextIOWrapper(io.BufferedRWPair(self.serial, self.serial))
        self.reader = pynmea2.NMEAStreamReader()
        super().__init__()



    async def poll(self) -> dict[str, int | float] | None:
        """
        Poll the sensor for data, and return a dictionary of the data. If this function fails,
         the sensor will be marked as "damaged" using exponential falloff

        :return: the data e.x. {"temperature": 34.7, "pressure": 106.4, "humidity": 0.56}
        """

        while True:
            try:
                line = self.sio.readline()
                msg = pynmea2.parse(line)
                if msg.sentence_type == "GGA":  # Only type that contains lat, long, and alt

                    # .latitude and .longitude function as helpers
                    return {"latitude": msg.latitude, "longitude": msg.longitude, "altitude": msg.altitude}

            except pynmea2.ParseError:
                self.logger.critical(f'Trying to parse data {line!r} error: {traceback.format_exc()}')
                continue
            except serial.SerialException:
                self.logger.critical(f'Failed to read: device error: {traceback.format_exc()}')
                break
        return None  # None value indicates failure to read device




class Neo6M_SATS(Sensor):
    # Metadata
    id: str = "satellites"  # Program ID for this sensor (e.g. bmp180)
    name: str = "NEO6M (satellites)" # Human-readable name (e.g. BMP180 Pressure/Temperature/Humidity Sensor)
    description: str = "to return GPS satellite information"  # Purpose of the sensor (e.g. Read pressure, temperature, and humidity)
    cooldown: float = 1  # How many seconds in between data polls (e.g. 7.5 seconds)


    def __init__(self):
        """
        Sensors use this function to create all necessary
         attributes and connections necessary to interface with the sensor
        :return: None
        """
        self.port = "/dev/ttyAMA0"
        try:
            self.serial = serial.Serial(self.port, baudrate=9600, timeout=0.5)
        except serial.SerialException:
            raise FileNotFoundError(f"Neo6M serial port ({self.port}) not found. This is a critical error.")
        self.sio = io.TextIOWrapper(io.BufferedRWPair(self.serial, self.serial))
        self.reader = pynmea2.NMEAStreamReader()
        super().__init__()



    async def poll(self) -> dict[str, int | float] | None:
        """
        Poll the sensor for data, and return a dictionary of the data. If this function fails,
         the sensor will be marked as "damaged" using exponential falloff

        :return: the data e.x. {"temperature": 34.7, "pressure": 106.4, "humidity": 0.56}
        """

        while True:
            try:
                line = self.sio.readline()
                msg = pynmea2.parse(line)
                if msg.sentence_type == "GGA":  # Only type that contains lat, long, and alt

                    # .latitude and .longitude function as helpers
                    return {"latitude": msg.latitude, "longitude": msg.longitude, "altitude": msg.altitude}

            except pynmea2.ParseError:
                self.logger.critical(f'Trying to parse data {line!r} error: {traceback.format_exc()}')
                continue
            except serial.SerialException:
                self.logger.critical(f'Failed to read: device error: {traceback.format_exc()}')
                break
        return None  # None value indicates failure to read device


