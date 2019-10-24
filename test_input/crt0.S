.global int_vector
.global bootloader

.set CORE_PSR_BIT_F, (0x01 << 0x06)
.set CORE_PSR_BIT_I, (0x01 << 0x07)
.set CORE_PSR_BIT_A, (0x01 << 0x08)
.set CORE_PSR_BIT_E, (0x01 << 0x09)

.set FPU_FPEXC_EN, 0x1E
.set FPU_CPACR_CP10, 0x14
.set FPU_CPACR_CP11, 0x16

.set PMU_PMCR_X, 0x04

.set TCM_ACTLR_ATCMPCEN, 0x19

.set SYS1_CLKCNTL_PENA, (0x01 << 0x08)

.section .flash_int_vector, "ax", %progbits
.arm

int_vector:
    ldr     pc, [pc, #0x18] /* reset. */
    b       .//ldr     pc, [pc, #0x18] /* undefined instruction. */
    b       .//ldr     pc, [pc, #0x18] /* system call. */
    b       .//ldr     pc, [pc, #0x18] /* prefetch abort. */
    b       .//ldr     pc, [pc, #0x18] /* data abort. */
    b       .//ldr     pc, [pc, #0x18] /* reserved. */
    b       .//ldr     pc, [pc, #0x18] /* IRQ. */
    b       .//ldr     pc, [pc, #0x18] /* FIQ. */
    .word   __LD_BOOTLOADER_START
    .word   0x08000004
    .word   0x08000008
    .word   0x0800000C
    .word   0x08000010
    .word   0x08000014
    .word   0x08000018
    .word   0x0800001C

.section .flash_bootloader, "ax", %progbits
.arm

bootloader:

    /* The Hercules series of microcontrollers include dual Cortex-R4F CPUs running in a lock-step
     * operation mode. A core compare module (CCM-R4) compares the output signals from each R4F CPU.
     * Any difference in the two CPUs’ outputs is flagged as a fault of a high-severity level. The
     * CPU internal registers are not guaranteed to power up in the same state for both the CPUs.
     * The CPU pushes the internal registers on to the stack on a function call, which could lead to
     * the detection of a core compare error. Therefore, the CPU internal core registers need to be
     * initialized to a predefined state before any function call is made. */
    mov     r0, #0x00000000 /* move initialization value into r0. */
    vmov    d0, r0, r0 /* FPU register. */
    vmov    d1, r0, r0 /* FPU register. */
    vmov    d2, r0, r0 /* FPU register. */
    vmov    d3, r0, r0 /* FPU register. */
    vmov    d4, r0, r0 /* FPU register. */
    vmov    d5, r0, r0 /* FPU register. */
    vmov    d6, r0, r0 /* FPU register. */
    vmov    d7, r0, r0 /* FPU register. */
    vmov    d8, r0, r0 /* FPU register. */
    vmov    d9, r0, r0 /* FPU register. */
    vmov    d10, r0, r0 /* FPU register. */
    vmov    d11, r0, r0 /* FPU register. */
    vmov    d12, r0, r0 /* FPU register. */
    vmov    d13, r0, r0 /* FPU register. */
    vmov    d14, r0, r0 /* FPU register. */
    vmov    d15, r0, r0 /* FPU register. */

    mov     r0, lr /* save lr to initialize lr of other modes. */

    cps     #0x11 /* switch to FIQ mode. */
    mov     r8, #0x00000000 /* banked. */
    mov     r9, #0x00000000 /* banked. */
    mov     r10, #0x00000000 /* banked. */
    mov     r11, #0x00000000 /* banked. */
    mov     r12, #0x00000000 /* banked. */
    ldr     sp, = __LD_STACK_FIQ_START /* initialize sp of FIQ mode. */
    mov     lr, r0 /* move r0 into lr of FIQ mode. */
    mrs     r1, cpsr /* move current program status register (CPSR) into r1. */
    msr     spsr_cxsf, r1 /* move r1 into saved program status register (SPSR) of FIQ mode. */
    cps     #0x12 /* switch to IRQ mode. */
    ldr     sp, = __LD_STACK_IRQ_START /* initialize sp of IRQ mode. */
    mov     lr, r0 /* move r0 into lr of IRQ mode. */
    mrs     r1, cpsr /* move current program status register (CPSR) into r1. */
    msr     spsr_cxsf, r1 /* move r1 into saved program status register (SPSR) of IRQ mode. */
    cps     #0x13 /* switch to supervisor mode. */
    ldr     sp, = __LD_STACK_SVC_START /* initialize sp of supervisor mode. */
    mov     lr, r0 /* move r0 into lr of supervisor mode. */
    mrs     r1, cpsr /* move current program status register (CPSR) into r1. */
    msr     spsr_cxsf, r1 /* move r1 into saved program status register (SPSR) of supervisor mode. */
    cps     #0x1B /* switch to undefined instruction mode. */
    ldr     sp, = __LD_STACK_UND_START /* initialize sp of undefined instruction mode. */
    mov     lr, r0 /* move r0 into lr of undefined instruction mode. */
    mrs     r1, cpsr /* move current program status register (CPSR) into r1. */
    msr     spsr_cxsf, r1 /* move r1 into saved program status register (SPSR) of undefined instruction mode. */
    cps     #0x17 /* switch to data/prefetch abort mode. */
    ldr     sp, = __LD_STACK_ABT_START /* initialize sp of data/prefetch abort mode. */
    mov     lr, r0 /* move r0 into lr of data/prefetch abort mode. */
    mrs     r1, cpsr /* move current program status register (CPSR) into r1. */
    msr     spsr_cxsf, r1 /* move r1 into saved program status register (SPSR) of data/prefetch abort mode. */
    cps     #0x1F /* switch to system mode. */
    ldr     sp, = __LD_STACK_USR_START /* initialize sp of system mode. */
    mov     lr, r0 /* move r0 into lr of system mode. */
    mrs     r1, cpsr /* move current program status register (CPSR) into r1. */
    msr     spsr_cxsf, r1 /* move r1 into saved program status register (SPSR) of system mode. */
    mov     lr, r0 /* move r0 into lr of system mode. */
    mov     r0, #0x00000000 /* shared. */
    mov     r1, #0x00000000 /* shared. */
    mov     r2, #0x00000000 /* shared. */
    mov     r3, #0x00000000 /* shared. */
    mov     r4, #0x00000000 /* shared. */
    mov     r5, #0x00000000 /* shared. */
    mov     r6, #0x00000000 /* shared. */
    mov     r7, #0x00000000 /* shared. */
    mov     r8, #0x00000000 /* shared. */
    mov     r9, #0x00000000 /* shared. */
    mov     r10, #0x00000000 /* shared. */
    mov     r11, #0x00000000 /* shared. */
    mov     r12, #0x00000000 /* shared. */

    /* The CPU’s call-return stack consists of a 4-entry circular buffer. When the CPU pre-fetch
     * unit (PFU) detects a taken procedure call instruction, the PFU pushes the return address onto
     * the call-return stack. The instructions that the PFU recognizes as procedure calls are, in
     * both the ARM and Thumb instruction sets:
     * - BL immediate
     * - BLX immediate
     * - BLX Rm */
    bl      call_return_stack_entry_1
    call_return_stack_entry_1:
    bl      call_return_stack_entry_2
    call_return_stack_entry_2:
    bl      call_return_stack_entry_3
    call_return_stack_entry_3:
    bl      call_return_stack_entry_4
    call_return_stack_entry_4:
test_point_startup_1:

    bl      main
    b       .

main:
    b       .