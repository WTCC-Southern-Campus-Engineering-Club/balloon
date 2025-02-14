import importlib
import os
import inspect
import Sensor

DB_FILENAME = "data.csv"

SENSORS: dict[str, Sensor.Sensor] = {}

for file in os.listdir(os.path.relpath("sensors")):  # Get all sensor files
    if file.endswith(".py"):
        module = importlib.import_module(f"sensors.{file.replace('.py', '')}")  # Import the file
        for cls in [obj for name, obj in inspect.getmembers(module, inspect.isclass)
                    if obj.__module__ == module.__name__]:  # Is it actually defined in the file
            if cls.__bases__ == (Sensor.Sensor,):  # Does it inherit Sensor and only Sensor
                SENSORS[cls.id] = cls()  # Actually create the class
