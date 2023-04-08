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
            parser.add_argument('--fan', required=False)
            parser.add_argument('--status', required=False)
            args = parser.parse_args()
            aws_client = AWSClient(root_logger)
            value = args.fan
            status = args.status
            aws_client.run_client(devices, FAN, value, status)



        except Exception:
            root_logger.exception('exception occurs during execution')
            traceback.print_exc()
