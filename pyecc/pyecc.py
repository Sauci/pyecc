"""
:file: pyecc.py
:author: Guillaume Sottas
:date: 28/10/2019
"""

import os
import pyelf
import struct
import yaml

from math import floor


def get_configuration():
    with open(os.path.join(os.path.dirname(__file__), 'config.yaml'), 'r') as fp:
        config = yaml.safe_load(fp)
    return config


class ECCGen(object):
    def __init__(self, device):
        self._config = get_configuration()[device]

    @staticmethod
    def _xor_list(data):
        result = data[0]
        for d in data[1:]:
            result ^= d
        return result

    @property
    def address_mask(self):
        return self._config['participation_address_mask']

    @property
    def address_size(self):
        return '{:032b}'.format(self._config['participation_address_mask']).count('1')

    @property
    def data_size(self):
        return 64

    @property
    def parity_table(self):
        return tuple((lambda x: x) if p == 'even' else (lambda x: 0 if x else 1) for p in self._config['parity_table'])

    @property
    def participation_table(self):
        return tuple(p['address'] << 64 | (p['msw'] << 32) | p['lsw'] for p in self._config['participation_table'])

    def get_ecc_byte(self, data, data_size):
        ecc_byte = 0
        for ecc_bit_idx in range(8):
            p_idx = (i for i in range(data_size) if (self.participation_table[ecc_bit_idx] >> i) & 1 == 1)
            ecc_byte |= self.parity_table[ecc_bit_idx](
                self._xor_list(tuple((data >> i) & 1 for i in p_idx))) << ecc_bit_idx
        return ecc_byte

    def get_ecc_from_elf(self, elf_file):
        result = list()
        elf_file = pyelf.ElfFile(elf_file)
        for address in range(0, floor(len(elf_file.binary)), int(self.data_size / 8)):
            msw, lsw = struct.unpack('{}{}'.format('>' if elf_file.endianness == 'big' else '<',
                                                   'I' * int(self.data_size / 32)),
                                     elf_file.binary[address:address + int(self.data_size / 8)])
            if self.address_size:
                address_shift = len(bin(self.address_mask)) - len(bin(self.address_mask).rstrip('0'))
                address_mask = self.address_mask >> address_shift
                result.append(self.get_ecc_byte((((address >> address_shift) & address_mask) << self.data_size) |
                                                (msw << 32) |
                                                lsw,
                                                data_size=self.data_size + self.address_size))
            else:
                result.append(self.get_ecc_byte((msw << 32) |
                                                lsw,
                                                data_size=self.data_size))
        return bytearray(result)
