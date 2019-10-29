"""
:file: cli.py
:author: Guillaume Sottas
:date: 28/10/2019
"""

import argparse

from pyecc import ECCGen, get_configuration


def main():
    parser = argparse.ArgumentParser(prog='pyecc',
                                     description='python command line utility for TI\'s ECC.',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('device',
                        type=str,
                        choices=[k for k in get_configuration().keys() if k not in ('shared_data',)],
                        help='target device')
    parser.add_argument('input_file', help='input file path')
    parser.add_argument('output_file', type=argparse.FileType('wb'), help='output file path')
    parser.add_argument('-endianness', type=str, default='little', choices=('big', 'little'))
    parser.add_argument('--version', action='version', version='%(prog)s {}'.format('0.1.0'))

    args = parser.parse_args()

    ecc = ECCGen(args.device)

    args.output_file.write(ecc.get_ecc_from_elf(args.input_file, endianness=args.endianness))


if __name__ == '__main__':
    main()
