cmake_minimum_required(VERSION 3.9)

project(hacky VERSION 0.0.1 LANGUAGES C ASM)

find_package(PythonInterp 3.6 REQUIRED)

set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/bin)

add_executable(program.elf crt0.S)
target_compile_options(program.elf
    PRIVATE -mbig-endian
    PRIVATE -nostdlib
    PRIVATE -march=armv7-r
    PRIVATE -mfloat-abi=hard
    PRIVATE -mfpu=vfpv3-d16)
target_link_options(program.elf
    PRIVATE -mbig-endian
    PRIVATE -nostdlib)
set_target_properties(program.elf PROPERTIES
    LINK_FLAGS -T${CMAKE_CURRENT_SOURCE_DIR}/linker_script.ld
    LINK_DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/linker_script.ld)

add_custom_target(program.bin ALL
    DEPENDS program.elf
    COMMAND ${OBJCOPY} -O binary program.elf program.bin
    WORKING_DIRECTORY ${CMAKE_RUNTIME_OUTPUT_DIRECTORY})

add_custom_target(program.srec ALL
    DEPENDS program.elf
    COMMAND ${OBJCOPY} -O srec program.elf program.srec
    WORKING_DIRECTORY ${CMAKE_RUNTIME_OUTPUT_DIRECTORY})

add_custom_target(program_ecc_pyecc.bin ALL
    DEPENDS program.elf
    COMMAND ${PYTHON_EXECUTABLE} pyecc/cli.py
    tms570lc4357
    ${CMAKE_RUNTIME_OUTPUT_DIRECTORY}/program.elf
    ${CMAKE_RUNTIME_OUTPUT_DIRECTORY}/program_ecc_pyecc.bin
    WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}/..
    COMMENT "Generating ECC binary using pyecc")
