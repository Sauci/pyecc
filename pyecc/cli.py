"""
:file: cli.py
:author: Guillaume Sottas
:date: 28/10/2019
"""

import argparse

from pyecc import ECCGen


def main():
    parser = argparse.ArgumentParser(prog='pya2l', description='python command line utility for TI\'s ECC.')
    parser.add_argument('device', help='target device')
    parser.add_argument('input_file', help='input file path')
    parser.add_argument('output_file', type=argparse.FileType('wb'), help='output file path')

    args = parser.parse_args()

    ecc = ECCGen(args.device)

    args.output_file.write(ecc.get_ecc_from_elf(args.input_file))


if __name__ == '__main__':
    main()
