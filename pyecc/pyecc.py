import argparse
import pyelf
import struct

from math import floor


class ECCGen(object):
    def __init__(self, elf_file=None, endianness='little'):
        self._elf_file = None
        if elf_file:
            self._elf_file = pyelf.ElfFile(elf_file)
        self.endianness = endianness

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

    @property
    def participation(self):
        le_code = [(0x0A7554EA << 64) | (0xB4D1B4D1 << 32) | 0x4B2E4B2E,
                   (0x1D68BAD1 << 64) | (0x15571557 << 32) | 0x15571557,
                   (0x14DAA9B5 << 64) | (0xA699A699 << 32) | 0xA699A699,
                   (0x13C6A78D << 64) | (0x38E338E3 << 32) | 0x38E338E3,
                   (0x0FC19F83 << 64) | (0xC0FCC0FC << 32) | 0xC0FCC0FC,
                   (0x1FC07F80 << 64) | (0xFF00FF00 << 32) | 0xFF00FF00,
                   (0x003FFF80 << 64) | (0xFF0000FF << 32) | 0xFF0000FF,
                   (0x1FC0007F << 64) | (0x00FFFF00 << 32) | 0xFF0000FF]
        if self.endianness == 'big':
            be_code = list()
            for code in le_code:
                reversed_endianness = struct.unpack('<III', struct.pack('>III',
                                                                        (code >> 64) & 0x1FFFFFFF,
                                                                        (code >> 32) & 0xFFFFFFFF,
                                                                        code & 0xFFFFFFFF))
                be_code.append((reversed_endianness[0] << 64) | (reversed_endianness[1] << 32) | reversed_endianness[2])
            return be_code
        return le_code

    @property
    def endianness(self):
        return self._endianness

    @endianness.setter
    def endianness(self, value):
        if value not in ('big', 'little'):
            raise ValueError('endianness must be either \'big\' or \'little\'')
        self._endianness = value

    def get_ecc_byte(self, data, data_size=64):
        ecc_byte = 0
        for ecc_bit_idx in range(len(self.participation)):
            p_idx = tuple(i for i in range(data_size) if (self.participation[ecc_bit_idx] >> i) & 1 == 1)
            ecc_byte |= self.parity[ecc_bit_idx](self._xor_list(tuple((data >> i) & 1 for i in p_idx))) << ecc_bit_idx
        return ecc_byte

    def get_ecc_from_elf(self, data_size=64, addr_size=32):
        result = list()
        binary = self._elf_file.binary
        for data_index in range(0, floor(len(binary)), data_size):
            msw, lsw = struct.unpack('{}{}'.format('>' if self.endianness == 'big' else '<',
                                                   'I' * int(data_size / 32)),
                                     binary[data_index:data_index + int(data_size / 8)])
            result.append(self.get_ecc_byte((msw << 32) | lsw, data_size=data_size))
        return bytearray(result)


if __name__ == '__main__':
    e = ECCGen(endianness='little')
    r = e.get_ecc_byte((0x954F6D2F << 32) |
                       0x2992A9B6, 64)
    b = e.get_ecc_from_elf('/Users/guillaumesottas/Documents/Github/hacky/cmake-build-debug/bin/boot.elf')
    print('0x{:02X}'.format(r))
