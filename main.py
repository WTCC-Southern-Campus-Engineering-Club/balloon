from __future__ import annotations

import asyncio
import functools
import sys
import time
import traceback

import logging

import formatter
from constants import *
from database import DataPoint, save_datapoint


# Configure root logger
root_logger = logging.getLogger("root")
root_logger.setLevel(logging.DEBUG)


logging.basicConfig(level=logging.DEBUG)
ch = logging.StreamHandler(stream=sys.stdout)
ch.setLevel(logging.DEBUG)

ch.setFormatter(formatter.Formatter())  # custom formatter

root_logger.handlers = [ch]  # Make sure to not double print
logger = logging.getLogger("balloon.main")

MAINLOOP_SLEEP = 2



def result_callback(future: asyncio.Task) -> None:
    result_logger = logging.getLogger("balloon.result")
    sensor_id = future.get_name()  # Get task name (= sensor id)
    sensor = SENSORS[sensor_id]
    sensor.running.release()  # Release the lock
    sensor.last_time_finished = time.time()  # Update last_time_finished
    try:
        result = future.result()
        if result is None:  # This means that the sensor failed
            raise Exception("Sensor result is None")

        result_logger.debug(f"Received data {result} from sensor {sensor.name!r}.")
        sensor.consecutive_failures = 0  # Reset consecutive failures
        save_datapoint(datapoint=DataPoint(**result)) # Save the data
    except Exception as e:
        result_logger.error(f"Failed to successfully execute poll for sensor {sensor.name!r} - {e} encountered."
                     f" \n EXC INFO: {traceback.format_exc()}")
        sensor.consecutive_failures += 1  # Increment failures




async def mainloop() -> None:
    running_tasks: dict[str, asyncio.Task | None] = {sensor_id: None for sensor_id in SENSORS}
    while True:
        logger.debug("Running mainloop now.")
        for sensor_name in SENSORS:
            current_time = time.time()
            sensor = SENSORS[sensor_name]
            # Should we update this sensor's data?
            enough_time_passed = (current_time - sensor.last_time_finished >
                                  sensor.cooldown * (2 ** sensor.consecutive_failures))
            sensor_is_enabled = not sensor.disabled

            not_currently_checking = not sensor.running.locked()

            logger.debug(f"Sensor id={sensor.id!r} on check: time_passed={current_time - sensor.last_time_finished},"
                         f" time_required={sensor.cooldown * (2 ** sensor.consecutive_failures)},"
                         f" consecutive_failures={sensor.consecutive_failures},"
                         f" enough_time_passed={enough_time_passed}, sensor_enabled={sensor_is_enabled},"
                         f" running={not not_currently_checking}")

            if enough_time_passed and sensor_is_enabled and not_currently_checking:
                logger.debug(f"Final decision on sensor id={sensor.id!r}: Start sensor polling.")
                await sensor.running.acquire()  # Acquire the running lock
                # Create the tak
                running_tasks[sensor.id] = asyncio.create_task(sensor.poll(), name=sensor.id)
                # Add the callback for the task completion
                running_tasks[sensor.id].add_done_callback(result_callback)
                logger.debug(f"Successfully started task {sensor.__class__.__name__}.poll() for sensor id={sensor.id!r}")
            else:
                reasons = []
                if not not_currently_checking:
                    reasons.append(f"Currently running")
                if not enough_time_passed:
                    reasons.append(f"Not enough time passed")
                if not sensor_is_enabled:
                    reasons.append(f"Not enabled")
                logger.debug(f"Final decision on sensor id={sensor.id!r}: Ignore this sensor. Reasons:"
                             f" {', '.join(reasons)}")

        logger.debug(f"Mainloop is now sleeping for {MAINLOOP_SLEEP} seconds")
        await asyncio.sleep(MAINLOOP_SLEEP)  # Take a break


# Mainloop
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(mainloop())
    except KeyboardInterrupt:
        logger.critical("Interrupted by user.")