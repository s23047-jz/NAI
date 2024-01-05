"""
Authors:
    Jakub Żurawski: https://github.com/s23047-jz/NAI/
    Mateusz Olstowski: https://github.com/Matieus/NAI/

---
"""

import time
import platform
import subprocess

import cv2 as cv
import mediapipe as mp
import numpy as np
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume


class MediaPlayer:
    def __init__(self):
        self.process_name = "Microsoft.Media.Player.exe"
        self.increase_reduce = 0.1
        self.volume_interface = self._get_volume_interface()
        self._valid_volume_interface()

    def _get_volume_interface(self):
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            if session.Process and session.Process.name() == self.process_name:
                return session._ctl.QueryInterface(ISimpleAudioVolume)
        return None

    def _valid_volume_interface(self):
        if self.volume_interface == None or self.volume_interface == '':
            raise Exception("Couldn't find an app")

    def is_media_player_playing(self):
        if self.volume_interface:
            return self.volume_interface.GetMute()

    def reduce_volume(self):
        if self.volume_interface:
            current_volume = self.volume_interface.GetMasterVolume()
            new_volume = max(0.0, current_volume - self.increase_reduce)
            self.volume_interface.SetMasterVolume(new_volume, None)

    def increase_volume(self):
        if self.volume_interface:
            current_volume = self.volume_interface.GetMasterVolume()
            new_volume = min(1.0, current_volume + self.increase_reduce)
            self.volume_interface.SetMasterVolume(new_volume, None)


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
        subprocess.run(['pactl', 'set-sink-volume', self.id, '-10%'])

    def increase_volume(self):
        subprocess.run(['pactl', 'set-sink-volume', self.id, '+10%'])


def main():
    system = platform.system().lower()
    print(f"Detected system: {system}")
    match system:
        case 'linux':
            celluloid = Celluloid()
            command = ''
            while command != 'q':
                command = input(f"[{system.upper()}] Enter '-' to reduce the sound level, '+' to increase or 'q' "
                                f"to quit: ")
                if command == '-':
                    celluloid.reduce_volume()
                elif command == '+':
                    celluloid.increase_volume()
        case 'windows':
            media_player = MediaPlayer()
            command = ''
            while command != 'q':
                command = input(f"[{system.upper()}] Enter '-' to reduce the sound level, '+' to increase, '!' to "
                                f"pause or resume, 'q' to quit: ")
                if command == '-':
                    media_player.reduce_volume()
                elif command == '+':
                    media_player.increase_volume()
                elif command == '!':
                    if media_player.is_media_player_playing():
                        pass
        case _:
            raise Exception("Unsupported os!")


if __name__ == '__main__':
    main()
