"""
:file: cli.py
:author: Guillaume Sottas
:date: 28/10/2019
"""

import argparse

from pyecc import ECCGen


def main():
    parser = argparse.ArgumentParser(prog='pya2l', description='python command line utility for TI\'s ECC.')
    parser.add_argument('input_file', help='input file path (*.elf)')
    parser.add_argument('output_file', type=argparse.FileType('wb'), help='output file path (*.bin)')
    parser.add_argument('-O',
                        dest='output_format',
                        metavar='output format',
                        action='store',
                        default='binary',
                        nargs='?',
                        help='output file format')

    args = parser.parse_args()

    ecc = ECCGen(args.input_file)

    if args.output_format == 'binary':
        args.output_file.write(ecc.get_ecc_from_elf())


if __name__ == '__main__':
    main()
