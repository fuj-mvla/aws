# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.F

import logging
import argparse
import json
import traceback
from datetime import datetime
from aws_client import AWSClient

# initialize logger
LOG_DIR = './logs/intern_assignment_{datetime}.log'
now = datetime.now()
root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)
handler = logging.FileHandler(LOG_DIR.format(datetime=now.strftime("%Y-%m-%d %H-%M-%S")), 'w', 'utf-8')
formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
handler.setFormatter(formatter)
root_logger.addHandler(handler)

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(formatter)
root_logger.addHandler(consoleHandler)

FAN = 'motor_speed'

if __name__ == '__main__':
    config = None
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
    except IOError:
        root_logger.error('unable to open config.json')
        traceback.print_exc()
        config = None
    if config:
        try:
            devices = config.get('devices')

            parser = argparse.ArgumentParser()
            parser.add_argument('--fan', required=True, default=0)
            args = parser.parse_args()
            value = args.fan

            aws_client = AWSClient(root_logger)
            aws_client.run_client(devices, FAN, value)
        except Exception:
            root_logger.exception('exception occurs during execution')
            traceback.print_exc()















