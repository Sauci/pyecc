.global bootloader

.section .flash_int_vector, "ax", %progbits
.arm

bootloader:
    .word   0x954F6D2F
    .word   0x2992A9B6
    .word   0x8F8342C3
    .word   0xE7DE1D53