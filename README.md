# Package description
This tool generates the ECC data to be programmed into flash 
[ECC](https://en.wikipedia.org/wiki/Error_detection_and_correction) of 
[Hercules](http://www.ti.com/microcontrollers/hercules-safety-mcus/overview.html) Platform Series microcontrollers.
  
# Installation  
  
## using `pip`
install the most recent version of the package (master branch) by running the following command:
`pip install git+https://github.com/Sauci/pyecc.git@master`
  
## from source
this package uses [bincopy](https://bincopy.readthedocs.io/en/latest/), 
[PyYAML](https://pyyaml.org/wiki/PyYAMLDocumentation) and [pyelf](https://github.com/Sauci/pyelf) packages. if it is not
already installed, install them first.
once the above prerequisite is installed:
- download the [pyecc](https://github.com/Sauci/pyecc/archive/master.zip) package  
- unzip it  
- move to the directory containing the setup.py file  
- run the command `python setup.py install`

**note:** the above command might require privileged access to succeed.

# Example of usage

## from command line
pyecc is invokable from command line, as it is probably invoked during the build process. Bellow, some invocation
examples:

### get invocation parameters
```bash
$ pyecc --help
usage: pyecc [-h] [-endianness {big,little}] [--version]
             {spna106_le_no_address,spna106_be_no_address,spna106_le_with_address,spna106_be_with_address,tms570lc4357}
             input_file output_file

python command line utility for TI's ECC.

positional arguments:
  {spna106_le_no_address,spna106_be_no_address,spna106_le_with_address,spna106_be_with_address,tms570lc4357}
                        target device
  input_file            input file path (*.bin, *.elf, *.srec)
  output_file           output file path (*.bin)

optional arguments:
  -h, --help            show this help message and exit
  -endianness {big,little}
  --version             show program's version number and exit
```

### generate ECC flash from binary file
The bellow example will generate the ECC flash content for [TMS650LC4357](http://www.ti.com/product/TMS570LC4357) target
device in big endian format.
```bash
$ echo -n -e \\x00\\x01\\x02\\x03\\x04\\x05\\x06\\x07 > input_file.bin
$ pyecc tms570lc4357 input_file.bin output_file.bin -endianness big
```

# Limitations
- Currently, the ECC flash content generator only supports 64 bits-aligned data. If not aligned, the script will raise a
  ```ValueError```
- The generated ECC flash content has been tested on following device(s):
  - [TMS650LC4357](http://www.ti.com/product/TMS570LC4357)