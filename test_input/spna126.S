.global bootloader

.section .flash_int_vector, "ax", %progbits
.arm

bootloader:
    /* little endian values. */
    .word   0x954F6D2F, 0x2992A9B6
    .word   0x8F8342C3, 0xE7DE1D53
    /* big endian values. */
    .word   0x2F6D4F95, 0xB6A99229
    .word   0xC342838F, 0x531DDEE7

    .word   0x00000000, 0x00000000
    .word   0x00000000, 0x00000000
    .word   0x00000000, 0x00000000
    .word   0x00000000, 0x00000000