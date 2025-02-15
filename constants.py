import importlib
import os
import Sensor

DB_FILENAME = "data.csv"

SENSORS: dict[str, Sensor.Sensor] = {}

for file in os.listdir(os.path.relpath("sensors")):
    if file.endswith(".py"):
        module = importlib.import_module(f"sensors.{file.replace('.py', '')}")

for cls in Sensor.Sensor.__subclasses__():
    SENSORS[cls.id] = cls()  # Actually create the class
