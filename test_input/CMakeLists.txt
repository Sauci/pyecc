cmake_minimum_required(VERSION 3.9)

project(hacky VERSION 0.0.1 LANGUAGES C ASM)

find_package(PythonInterp 3.6 REQUIRED)

set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/bin)

add_executable(armv7r_le.elf crt0.S)
target_compile_options(armv7r_le.elf
    PRIVATE -mlittle-endian
    PRIVATE -nostdlib
    PRIVATE -march=armv7-r
    PRIVATE -mfloat-abi=hard
    PRIVATE -mfpu=vfpv3-d16)
target_link_options(armv7r_le.elf
    PRIVATE -mlittle-endian
    PRIVATE -nostdlib)
set_target_properties(armv7r_le.elf PROPERTIES
    LINK_FLAGS -T${CMAKE_CURRENT_SOURCE_DIR}/linker_script.ld
    LINK_DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/linker_script.ld)

add_custom_command(TARGET armv7r_le.elf POST_BUILD
    COMMAND ${PYTHON_EXECUTABLE} pyecc/cli.py
    ${CMAKE_RUNTIME_OUTPUT_DIRECTORY}/armv7r_le.elf
    ${CMAKE_RUNTIME_OUTPUT_DIRECTORY}/armv7r_le.bin
    WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}/..
    COMMENT "Generating ECC binary for target armv7r_le.elf")

add_executable(armv7r_be.elf crt0.S)
target_compile_options(armv7r_be.elf
    PRIVATE -mbig-endian
    PRIVATE -nostdlib
    PRIVATE -march=armv7-r
    PRIVATE -mfloat-abi=hard
    PRIVATE -mfpu=vfpv3-d16)
target_link_options(armv7r_be.elf
    PRIVATE -mbig-endian
    PRIVATE -nostdlib)
set_target_properties(armv7r_be.elf PROPERTIES
    LINK_FLAGS -T${CMAKE_CURRENT_SOURCE_DIR}/linker_script.ld
    LINK_DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/linker_script.ld)

add_custom_command(TARGET armv7r_be.elf POST_BUILD
    COMMAND ${PYTHON_EXECUTABLE} pyecc/cli.py
    ${CMAKE_RUNTIME_OUTPUT_DIRECTORY}/armv7r_be.elf
    ${CMAKE_RUNTIME_OUTPUT_DIRECTORY}/armv7r_be.bin
    WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}/..
    COMMENT "Generating ECC binary for target armv7r_be.elf")
