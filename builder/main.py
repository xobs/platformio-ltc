"""
    Build script for ltc
"""

from os.path import join
from SCons.Script import AlwaysBuild, Builder, Default, DefaultEnvironment

env = DefaultEnvironment()

# A full list with the available variables
# http://www.scons.org/doc/production/HTML/scons-user.html#app-variables
env.Replace(
    AR="arm-none-eabi-ar",
    AS="arm-none-eabi-as",
    CC="arm-none-eabi-gcc",
    CXX="arm-none-eabi-g++",
    OBJCOPY="arm-none-eabi-objcopy",
    RANLIB="arm-none-eabi-ranlib",
    SIZETOOL="arm-none-eabi-size",

    ARFLAGS=["rcs"],

    ASFLAGS=["-x", "assembler-with-cpp"],
    CCFLAGS=[
             "-I.",
             "-g",
             "-Iinc",
             "-fsingle-precision-constant",
             "-Wall",
             "-Wextra",
             "-march=armv6s-m",
             "-mthumb",
             "-mfloat-abi=soft",
             "-fno-builtin",
             "-ffunction-sections",
             "-fdata-sections",
             "-fno-common",
             "-fomit-frame-pointer",
             "-nostdlib",
             "-Os"],
    CXXFLAGS=[
              "-std=c++11",
              "-fno-rtti",
              "-fno-exceptions"],
    LINKFLAGS=[
              "-fsingle-precision-constant",
              "-g",
              "-mcpu=cortex-m0plus",
              "-mfloat-abi=soft",
              "-mthumb",
              "-fno-builtin",
              "-ffunction-sections",
              "-fdata-sections",
              "-fno-common",
              "-fomit-frame-pointer",
              "-falign-functions=16",
              "-Os",
              "-nostartfiles",
              "-nostdlib",
              "-nodefaultlibs", \
              "-Wl,--gc-sections,--no-warn-mismatch,--build-id=none"],

    CPPDEFINES=["VERSION=\"v1.0\""],
)

env.Append(
    BUILDERS=dict(
        ElfToHex=Builder(
            action=" ".join([
                "$OBJCOPY",
                "-O",
                "ihex",
                "$SOURCES",
                "$TARGET"]),
            suffix=".hex"
        )
    )
)

# The source code of "platformio-build-tool" is here
# https://github.com/platformio/platformio-core/blob/develop/platformio/builder/tools/platformio.py

#
# Target: Build executable and linkable firmware
#
target_elf = env.BuildProgram()

#
# Target: Build the .hex file
#
target_hex = env.ElfToHex(join("$BUILD_DIR", "firmware"), target_elf)

#
# Target: Define targets
#
Default(target_hex)
