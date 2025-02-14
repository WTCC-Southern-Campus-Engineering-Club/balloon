from __future__ import annotations

import asyncio
from random import randint

import bme280
from smbus2 import SMBus

from Sensor import Sensor


class BME280(Sensor):
    # Metadata
    id: str = "bme280"  # Program ID for this sensor (e.g. bmp180)
    name: str = "BME280 (Pressure/Temp/Hum)" # Human-readable name (e.g. BMP180 Pressure/Temperature/Humidity Sensor)
    description: str = "bme280, for pressure, temp, and humidity"  # Purpose of the sensor (e.g. Read pressure, temperature, and humidity)
    cooldown: float = 5  # How many seconds in between data polls (e.g. 7.5 seconds)


    def __init__(self):
        """
        Sensors use this function to create all necessary
         attributes and connections necessary to interface with the sensor
        :return: None
        """
        self.bus = SMBus(1)
        self.qnh = 1054.44149  # can recalculate
        self.sensor = bme280.BME280(i2c_addr=0x76, i2c_dev=self.bus)
        super().__init__()
        self.has_setup = False
        self.setup()

    def setup(self):
        try:
            for i in range(10):
                self.sensor.get_temperature()  # get the sensor ready
                self.sensor.get_pressure()
                self.sensor.get_humidity()
                self.sensor.get_altitude()
            self.has_setup = True
        except RuntimeError:
            return  # Doesn't matter




    async def poll(self) -> dict[str, int | float]:
        """
        Poll the sensor for data, and return a dictionary of the data. If this function fails,
         the sensor will be marked as "damaged" using exponential falloff

        :return: the data e.x. {"temperature": 34.7, "pressure": 106.4, "humidity": 0.56}
        """
        if not self.has_setup:
            self.setup()
            if not self.has_setup:  # Setup failed
                return None  # None indicates failure to read

        return {"temperature": self.sensor.get_temperature(), "pressure": self.sensor.get_pressure(),
                "humidity": self.sensor.get_humidity(), "bme-altitude": self.sensor.get_altitude(qnh=self.qnh)}

