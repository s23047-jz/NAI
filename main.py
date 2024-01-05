"""
Authors:
    Jakub Żurawski: https://github.com/s23047-jz/NAI/
    Mateusz Olstowski: https://github.com/Matieus/NAI/

---
"""

import os
import platform
import subprocess

import cv2 as cv
import mediapipe as mp
import numpy as np


class Celluloid:
    def __init__(self):
        self.app_name = "io.github.celluloid_player.Celluloid"
        self.id = self._set_app_id()
        self._valid_id()

    def _set_app_id(self):
        try:
            result = subprocess.run(['pactl', 'list', 'sink-inputs'], stdout=subprocess.PIPE)
            lines = result.stdout.decode('utf-8').split('\n')
            current_id = ''
            for line in lines:
                if "Sink:" in line:
                    current_id = line.split(': ')[1]
                if f'application.name = "{self.app_name}"' in line:
                    return current_id
        except Exception as e:
            raise Exception(f"Couldn't find an app {str(e)}")

    def _valid_id(self):
        if self.id == None or self.id == '':
            raise Exception("Couldn't find an app")

    def reduce_volume(self):
        print('ID', self.id)
        subprocess.run(['pactl', 'set-sink-volume', self.id, '-10%'])

    def increase_volume(self):
        print('ID', self.id)
        subprocess.run(['pactl', 'set-sink-volume', self.id, '+10%'])


def main():
    system = platform.system().lower()
    print(f"Detected system: {system}")
    match system:
        case 'linux':
            celluloid = Celluloid()
            command = ''
            while command != 'q':
                command = input("Enter '-' if you want to reduce the sound level or '+' if increase ('q' = quit): ")
                if command == '-':
                    celluloid.reduce_volume()
                elif command == '+':
                    celluloid.increase_volume()
        case 'windows':
            pass
        case _:
            raise Exception("Unsupported os!")


if __name__ == '__main__':
    main()
