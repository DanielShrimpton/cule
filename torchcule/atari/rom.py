"""CuLE (CUda Learning Environment module)

This module provides access to several RL environments that generate data
on the CPU or GPU.
"""

import atari_py
import gym
import os
import site

from torchcule_atari import AtariRom

# def get_rom(roms_path, env_name):
def get_rom(env_name):
    # roms = [os.path.splitext(rom)[0] for rom in os.listdir(roms_path) if '.bin' in rom]
    roms = atari_py.list_games()
    for rom in roms:
        if env_name.lower().startswith(rom.lower().replace('_', '')):
            # return rom + '.bin'
            return atari_py.get_game_path(rom)

class Rom(AtariRom):

    def __init__(self, env_name):
        # # game_path = gym.make(env_name).env.game_path
        # roms_path = os.path.join(site.getsitepackages()[0], 'AutoROM', 'roms')
        # rom = get_rom(roms_path, env_name)
        # game_path = os.path.join(roms_path, rom)
        game_path = get_rom(env_name)
        if not os.path.exists(game_path):
            raise IOError('Requested environment (%s) does not exist '
                          'in valid list of environments:\n%s' \
                          % (env_name, ', '.join(sorted(atari_py.list_games()))))
        super(Rom, self).__init__(game_path)

    def __repr__(self):
        return 'Name       : {}\n'\
               'Controller : {}\n'\
               'Swapped    : {}\n'\
               'Left Diff  : {}\n'\
               'Right Diff : {}\n'\
               'Type       : {}\n'\
               'Display    : {}\n'\
               'ROM Size   : {}\n'\
               'RAM Size   : {}\n'\
               'MD5        : {}\n'\
               .format(self.game_name(),
                       'Paddles' if self.use_paddles() else 'Joystick',
                       'Yes' if self.swap_paddles() or self.swap_ports() else 'No',
                       'B' if self.player_left_difficulty_B() else 'A',
                       'B' if self.player_right_difficulty_B() else 'A',
                       self.type(),
                       'NTSC' if self.is_ntsc() else 'PAL',
                       self.rom_size(),
                       self.ram_size(),
                       self.md5())

