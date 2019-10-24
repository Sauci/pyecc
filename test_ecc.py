import pytest

from pyecc import ECCGen


@pytest.mark.parametrize('msw, lsw, expected', [pytest.param(0x954F6D2F, 0x2992A9B6, 0xAA),
                                                pytest.param(0x8F8342C3, 0xE7DE1D53, 0x14),
                                                pytest.param(0x554B0A86, 0xA8F07BDB, 0x41),
                                                pytest.param(0x19F2DA66, 0x14780AF1, 0x60),
                                                pytest.param(0x5D80C176, 0xA04CFED0, 0x01),
                                                pytest.param(0x2B54902B, 0xC4E77D0F, 0x84),
                                                pytest.param(0x9190D774, 0x01AEA191, 0x97),
                                                pytest.param(0xD072D410, 0xBD4E690F, 0xCF),
                                                pytest.param(0x8F7FF177, 0x6D1AD8A0, 0x4F),
                                                pytest.param(0x2F92B288, 0xD3E1A7BD, 0xDD)])
def test_little_endian_ecc_byte_without_address_participation(msw, lsw, expected):
    """
    test if generated ECC byte is correct when address value does not participate to ECC value
    note: see http://www.ti.com.cn/cn/lit/an/spna126/spna126.pdf
    """

    ecc = ECCGen(endianness='little')
    assert ecc.get_ecc_byte((msw << 32) | lsw, data_size=64) == expected


@pytest.mark.parametrize('msw, lsw, expected', [pytest.param(0x2F6D4F95, 0xB6A99229, 0xAA),
                                                pytest.param(0xC342838F, 0x531DDEE7, 0x14),
                                                pytest.param(0x860A4B55, 0xDB7BF0A8, 0x41),
                                                pytest.param(0x66DAF219, 0xF10A7814, 0x60),
                                                pytest.param(0x76C1805D, 0xD0FE4CA0, 0x01),
                                                pytest.param(0x2B90542B, 0x0F7DE7C4, 0x84),
                                                pytest.param(0x74D79091, 0x91A1AE01, 0x97),
                                                pytest.param(0x10D472D0, 0x0F694EBD, 0xCF),
                                                pytest.param(0x77F17F8F, 0xA0D81A6D, 0x4F),
                                                pytest.param(0x88B2922F, 0xBDA7E1D3, 0xDD)])
def test_big_endian_ecc_byte_without_address_participation(msw, lsw, expected):
    """
    test if generated ECC byte is correct when address value does not participate to ECC value
    note: see http://www.ti.com.cn/cn/lit/an/spna126/spna126.pdf
    """

    ecc = ECCGen(endianness='big')
    assert ecc.get_ecc_byte((msw << 32) | lsw, data_size=64) == expected


@pytest.mark.parametrize('addr, msw, lsw, expected', [# pytest.param(0x002415D8, 0xF126E546, 0x9A03FA6F, 0x7C),
                                                      # pytest.param(0x000952B8, 0x21D94D7E, 0xB18B4F04, 0x3A),
                                                      pytest.param(0x0002C580, 0xF70C3A2D, 0xEC8835ED, 0x60),
                                                      pytest.param(0x00117B40, 0x0ED9FB58, 0x3E03C60D, 0x6B),
                                                      pytest.param(0x003DDB80, 0x02324C15, 0xA80EFA23, 0x20),
                                                      pytest.param(0x0035D008, 0xC34B6BF3, 0x8FBD9E0F, 0x4F),
                                                      pytest.param(0x003F7180, 0xFC31972C, 0xD3EB454F, 0xE9),
                                                      pytest.param(0x003EED68, 0x7BAF4225, 0x4DEE03BB, 0xB3),
                                                      pytest.param(0x00263938, 0x446F1271, 0x8DA56AF6, 0xF0),
                                                      pytest.param(0x0021A9B8, 0x98A582BA, 0xEF7C951D, 0xE8)])
def test_little_endian_ecc_byte_with_address_participation(addr, msw, lsw, expected):
    """
    test if generated ECC byte is correct when address value does participate to ECC value
    note: see http://www.ti.com.cn/cn/lit/an/spna126/spna126.pdf
    """

    ecc = ECCGen(endianness='little')
    assert ecc.get_ecc_byte(((addr >> 3) << 64) | (msw << 32) | lsw, data_size=64 + 21) == expected


@pytest.mark.parametrize('addr, msw, lsw, expected', [pytest.param(0x002415D8, 0x46E526F1, 0x6FFA039A, 0x7C),
                                                      # pytest.param(0xB8520900, 0x7E4DD921, 0x044F8BB1, 0x3A),
                                                      pytest.param(0x0002C580, 0x2D3A0CF7, 0xED3588EC, 0x60),
                                                      pytest.param(0x00117B40, 0x58FBD90E, 0x0DC6033E, 0x6B),
                                                      pytest.param(0x003DDB80, 0x154C3202, 0x23FA0EA8, 0x20),
                                                      pytest.param(0x0035D008, 0xF36B4BC3, 0x0F9EBD8F, 0x4F),
                                                      pytest.param(0x003F7180, 0x2C9731FC, 0x4F45EBD3, 0xE9),
                                                      pytest.param(0x003EED68, 0x2542AF7B, 0xBB03EE4D, 0xB3),
                                                      pytest.param(0x00263938, 0x71126F44, 0xF66AA58D, 0xF0),
                                                      pytest.param(0x0021A9B8, 0xBA82A598, 0x1D957CEF, 0xE8)
                                                      ])
def test_big_endian_ecc_byte_with_address_participation(addr, msw, lsw, expected):
    """
    test if generated ECC byte is correct when address value does participate to ECC value
    note: see http://www.ti.com.cn/cn/lit/an/spna126/spna126.pdf
    """

    ecc = ECCGen(endianness='big')
    assert ecc.get_ecc_byte(((addr >> 3) << 64) | (msw << 32) | lsw, data_size=64 + 21) == expected
