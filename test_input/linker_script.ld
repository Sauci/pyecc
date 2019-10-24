MEMORY
{
    FLASH_VEC (x) : ORIGIN = 0x00000000, LENGTH = 0x00000040
    FLASH_TCM (rx) : ORIGIN = 0x00000040, LENGTH = 0x003FFFC0
    RAM_TCM (rwx) : ORIGIN = 0x08000000, LENGTH = 512K
    RAM_EEC (rwx) : ORIGIN = 0x08400000, LENGTH = 512K
    PERIPH_FRAME_1 (rw) : ORIGIN = 0xFFF80000, LENGTH = 0xFFFFFFFF - 0xFFF80000
    PERIPH_FRAME_2 (rw) : ORIGIN = 0xFC000000, LENGTH = 0xFCFFFFFF - 0xFC000000
    PERIPH_FRAME_3 (rw) : ORIGIN = 0xFF000000, LENGTH = 0xFFF7FFFF - 0xFF000000
}


ENTRY(bootloader)

SECTIONS
{
    .flash_int_vector :
    {
        __LD_BOOTLOADER_CHECKSUM_START = .;
        KEEP(*(.flash_int_vector))
    } > FLASH_VEC

    .flash_bootloader 0x00000040 :
    {
        __LD_BOOTLOADER_START = .;
        *(.flash_bootloader)
        . = ALIGN(0x08);
        . = 0x00001000 - 0x08;
        QUAD(0x636865636B73756D)
        . = 0x00001000;
        __LD_BOOTLOADER_CHECKSUM_END = .;
        __LD_BOOTLOADER_CRC = .;
    } > FLASH_TCM
    .stack :
    {
        __LD_STACK_STOP = .;
        __LD_STACK_FIQ_STOP = .;
        . += 0x0100;
        __LD_STACK_FIQ_START = .;
        . = ALIGN(0x04);

        __LD_STACK_IRQ_STOP = .;
        . += 0x0100;
        __LD_STACK_IRQ_START = .;
        . = ALIGN(0x04);

        __LD_STACK_ABT_STOP = .;
        . += 0x0100;
        __LD_STACK_ABT_START = .;
        . = ALIGN(0x04);

        __LD_STACK_UND_STOP = .;
        . += 0x0100;
        __LD_STACK_UND_START = .;
        . = ALIGN(0x04);

        __LD_STACK_USR_STOP = .;
        . += 0x0100;
        __LD_STACK_USR_START = .;
        . = ALIGN(0x04);

        __LD_STACK_SVC_STOP = .;
        . += 0x0100;
        __LD_STACK_SVC_START = .;
        __LD_STACK_START = .;
    } > RAM_TCM

}
