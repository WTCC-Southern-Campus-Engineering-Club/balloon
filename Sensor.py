from __future__ import annotations

import asyncio
import logging


class Sensor:
    # Metadata
    id: str  # Program ID for this sensor (e.g. bmp180)
    name: str # Human-readable name (e.g. BMP180 Pressure/Temperature/Humidity Sensor)
    description: str  # Purpose of the sensor (e.g. Read pressure, temperature, and humidity)
    cooldown: float  # How many seconds in between data polls (e.g. 7.5 seconds)


    # Attributes set during runtime by mainloop
    running: asyncio.Lock = asyncio.Lock()  # Whether the sensor is currently being polled
    disabled: bool = False  # Whether the sensor has been disabled in software
    last_time_started: float = -1  # Last time the sensor poll started
    last_time_finished: float = -1  # Last time the sensor poll finished
    consecutive_failures: int = 0  # Number of consecutive failures (exponential backoff)

    def __init__(self):
        """
        Sensors use this function to create all necessary
        attributes and connections necessary to interface with the sensor
        :return: None
        """
        self.logger = logging.getLogger(f"balloon.sensors.{self.__class__.__name__}")



    async def poll(self) -> dict[str, int | float]:
        """
        Poll the sensor for data, and return a dictionary of the data. If this function fails,
     the sensor will be marked as "damaged" using exponential falloff

        :return: the data e.x. {"temperature": 34.7, "pressure": 106.4, "humidity": 0.56}
        """
        pass

