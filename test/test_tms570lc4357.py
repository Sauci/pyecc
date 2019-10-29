import os
import pytest

from pyecc import ECCGen


@pytest.mark.parametrize('addr, msw, lsw, expected', [pytest.param(0x00000000, 0x954F6D2F, 0x2992A9B6, 0x5A),
                                                      pytest.param(0x00000008, 0x8F8342C3, 0xE7DE1D53, 0x62),
                                                      pytest.param(0x00000010, 0x2F6D4F95, 0xB6A99229, 0xCB),
                                                      pytest.param(0x00000018, 0xC342838F, 0x531DDEE7, 0xEB),
                                                      pytest.param(0x00000020, 0x00000000, 0x00000000, 0x80),
                                                      pytest.param(0x00000028, 0x00000000, 0x00000000, 0x1E),
                                                      pytest.param(0x00000030, 0x00000000, 0x00000000, 0x11),
                                                      pytest.param(0x00000038, 0x00000000, 0x00000000, 0x8F),
                                                      pytest.param(0x00001030, 0x00000000, 0x00000000, 0x6B)])
def test_values_from_crt0_against_uniflash_values(addr, msw, lsw, expected):
    """
    test if generated ECC byte is correct when address value does participate to ECC value
    note: see http://www.ti.com.cn/cn/lit/an/spna126/spna126.pdf
    """

    ecc = ECCGen('tms570lc4357')
    assert ecc.get_ecc_byte(((addr >> 3) << 64) | (msw << 32) | lsw, data_size=64 + 29) == expected


@pytest.mark.skip
def test_ecc_values_between_generated_binary_and_uniflash_binary():
    ecc = ECCGen('tms570lc4357')
    ecc_pyecc = ecc.get_ecc_from_elf(os.path.join(os.path.dirname(__file__), 'bin', 'program.elf'))
    with open(os.path.join(os.path.dirname(__file__), 'bin', 'program_ecc_uniflash.bin'), 'rb') as fp:
        ecc_uniflash = fp.read()
    assert len(ecc_pyecc) == len(ecc_uniflash)
    for ecc_byte_pyecc, ecc_byte_uniflash in zip(ecc_pyecc, ecc_uniflash):
        assert ecc_byte_pyecc == ecc_byte_uniflash
