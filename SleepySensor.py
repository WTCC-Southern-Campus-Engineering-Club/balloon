from __future__ import annotations

import asyncio
from random import randint

from Sensor import Sensor


class SleepySensor(Sensor):
    # Metadata
    id: str = "sleepy"  # Program ID for this sensor (e.g. bmp180)
    name: str = "SleepySensor (test)" # Human-readable name (e.g. BMP180 Pressure/Temperature/Humidity Sensor)
    description: str = "sensor that is sleepy"  # Purpose of the sensor (e.g. Read pressure, temperature, and humidity)
    cooldown: float = 5  # How many seconds in between data polls (e.g. 7.5 seconds)


    def __init__(self):
        """
        Sensors use this function to create all necessary
         attributes and connections necessary to interface with the sensor
        :return: None
        """
        super().__init__()



    async def poll(self) -> dict[str, int | float]:
        """
        Poll the sensor for data, and return a dictionary of the data. If this function fails,
         the sensor will be marked as "damaged" using exponential falloff

        :return: the data e.x. {"temperature": 34.7, "pressure": 106.4, "humidity": 0.56}
        """
        rng = randint(1, 5)
        self.logger.debug(f"Sleepy Sensor now sleeping for {rng} seconds")
        await asyncio.sleep(rng)
        self.logger.debug(f'Sleepy Sensor done sleeping for {rng} seconds')
        return {"slept_for": rng}

