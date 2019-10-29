import argparse
import pyelf
import struct

from math import floor


class ECCGen(object):
    def __init__(self, elf_file=None):
        self._elf_file = None
        if elf_file:
            self._elf_file = pyelf.ElfFile(elf_file)

    @staticmethod
    def _xor_list(data):
        result = data[0]
        for d in data[1:]:
            result ^= d
        return result

    @property
    def parity(self):
        return (lambda x: x,
                lambda x: x,
                lambda x: 0 if x else 1,
                lambda x: 0 if x else 1,
                lambda x: 0 if x else 1,
                lambda x: 0 if x else 1,
                lambda x: 0 if x else 1,
                lambda x: 0 if x else 1)

    @staticmethod
    def get_participation(ecc_bit_index, endianness='little'):
        if endianness == 'big':
            return ((0x0A7554EA << 64) | (0xD1B4D1B4 << 32) | 0x2E4B2E4B,
                    (0x1D68BAD1 << 64) | (0x57155715 << 32) | 0x57155715,
                    (0x14DAA9B5 << 64) | (0x99A699A6 << 32) | 0x99A699A6,
                    (0x13C6A78D << 64) | (0xE338E338 << 32) | 0xE338E338,
                    (0x0FC19F83 << 64) | (0xFCC0FCC0 << 32) | 0xFCC0FCC0,
                    (0x1FC07F80 << 64) | (0x00FF00FF << 32) | 0x00FF00FF,
                    (0x003FFF80 << 64) | (0xFF0000FF << 32) | 0xFF0000FF,
                    (0x1FC0007F << 64) | (0x00FFFF00 << 32) | 0xFF0000FF)[ecc_bit_index]
        elif endianness == 'little':
            return ((0x0A7554EA << 64) | (0xB4D1B4D1 << 32) | 0x4B2E4B2E,
                    (0x1D68BAD1 << 64) | (0x15571557 << 32) | 0x15571557,
                    (0x14DAA9B5 << 64) | (0xA699A699 << 32) | 0xA699A699,
                    (0x13C6A78D << 64) | (0x38E338E3 << 32) | 0x38E338E3,
                    (0x0FC19F83 << 64) | (0xC0FCC0FC << 32) | 0xC0FCC0FC,
                    (0x1FC07F80 << 64) | (0xFF00FF00 << 32) | 0xFF00FF00,
                    (0x003FFF80 << 64) | (0xFF0000FF << 32) | 0xFF0000FF,
                    (0x1FC0007F << 64) | (0x00FFFF00 << 32) | 0xFF0000FF)[ecc_bit_index]
        else:
            raise ValueError('endianness must be either \'big\' or \'little\'')

    def get_ecc_byte(self, data, data_size=64, endianness='little'):
        ecc_byte = 0
        for ecc_bit_idx in range(8):
            p_idx = tuple(
                i for i in range(data_size) if (self.get_participation(ecc_bit_idx, endianness) >> i) & 1 == 1)
            ecc_byte |= self.parity[ecc_bit_idx](self._xor_list(tuple((data >> i) & 1 for i in p_idx))) << ecc_bit_idx
        return ecc_byte

    def get_ecc_from_elf(self, data_size=64, addr_size=32):
        result = list()
        for data_index in range(0, floor(len(self._elf_file.binary)), int(data_size / 8)):
            msw, lsw = struct.unpack('{}{}'.format('>' if self._elf_file.endianness == 'big' else '<',
                                                   'I' * int(data_size / 32)),
                                     self._elf_file.binary[data_index:data_index + int(data_size / 8)])
            result.append(self.get_ecc_byte((msw << 32) | lsw, data_size=data_size))
            print('data_index: 0x{:08X} ECC: 0x{:02X}'.format(data_index, result[-1]))
        return bytearray(result)
