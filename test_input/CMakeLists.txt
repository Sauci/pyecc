cmake_minimum_required(VERSION 3.9)

project(hacky VERSION 0.0.1 LANGUAGES C ASM)

find_package(PythonInterp 3.6 REQUIRED)

set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/bin)

add_executable(le32.elf crt0.S)
target_compile_options(le32.elf
    PRIVATE -mlittle-endian
    PRIVATE -nostdlib
    PRIVATE -march=armv7-a
    PRIVATE -mfloat-abi=hard
    PRIVATE -mfpu=vfpv3-d16)
target_link_options(le32.elf
    PRIVATE -mlittle-endian
    PRIVATE -nostdlib)
set_target_properties(le32.elf PROPERTIES
    LINK_FLAGS -T${CMAKE_CURRENT_SOURCE_DIR}/linker_script.ld
    LINK_DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/linker_script.ld)

add_custom_command(TARGET le32.elf POST_BUILD
    COMMAND ${PYTHON_EXECUTABLE} pyecc/cli.py
    ${CMAKE_RUNTIME_OUTPUT_DIRECTORY}/le32.elf
    ${CMAKE_RUNTIME_OUTPUT_DIRECTORY}/le32.bin
    WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}/..
    COMMENT "Generating ECC binary for target le32.elf")

add_executable(be32.elf crt0.S)
target_compile_options(be32.elf
    PRIVATE -mbig-endian
    PRIVATE -nostdlib
    PRIVATE -march=armv7-a
    PRIVATE -mfloat-abi=hard
    PRIVATE -mfpu=vfpv3-d16)
target_link_options(be32.elf
    PRIVATE -mbig-endian
    PRIVATE -nostdlib)
set_target_properties(be32.elf PROPERTIES
    LINK_FLAGS -T${CMAKE_CURRENT_SOURCE_DIR}/linker_script.ld
    LINK_DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/linker_script.ld)
