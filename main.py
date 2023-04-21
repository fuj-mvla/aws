# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.F
import tkinter
from tkinter import *
from tkinter import ttk
import asyncio
import logging
from tkinter.ttk import *
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


    def update_fan_speed():
        fanb.configure(state=DISABLED)

        try:
            value = e.get()
            value = int(value)
            status = False

            aws_client = AWSClient(root_logger)

            aws_client.run_client(devices, FAN, value, status)
            fanb.configure(state=NORMAL)

        except Exception:
            root_logger.exception('exception occurs during execution')


    def check_connection():
        value = None
        status = True
        aws_client = AWSClient(root_logger)
        aws_client.run_client(devices, FAN, value, status)


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

            root = Tk()
            root.geometry("620x400")
            frm = Frame(root, padding=10)
            frm.pack(fill="both", expand=True, padx=200, pady=20)
            Label(frm, text="Enter Fan Speed").grid(column=0, row=0)
            e = Entry(frm, foreground="blue")
            e.grid(column=0, row=1, pady=20)
            fanb = Button(frm, text="Enter", width=25, command=update_fan_speed)
            fanb.grid(column=0, row=2)
            Button(frm, text="Check connection status", width=25, command=check_connection).grid(column=0, row=3,
                                                                                                 pady=10)

            root.mainloop()

        # aws_client.run_client(devices, FAN, value, status)

        except Exception:
            root_logger.exception('exception occurs during execution')
            traceback.print_exc()
