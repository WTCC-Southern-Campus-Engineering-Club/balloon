import importlib
import os
import inspect
import Sensor

DB_FILENAME = "data.csv"

SENSORS: dict[str, Sensor.Sensor] = {}

for file in os.listdir(os.path.relpath("sensors")):
    if file.endswith(".py"):
        module = importlib.import_module(f"sensors.{file.replace('.py', '')}")
        for cls in [obj for name, obj in inspect.getmembers(module, inspect.isclass) if obj.__module__ == module.__name__]:
            if cls.__bases__ == (Sensor.Sensor,):
                SENSORS[cls.id] = cls
