from setuptools import setup

setup(
    name='pyecc',
    version='0.1.0',
    packages=['pyecc'],
    url='https://github.com/Sauci/pyecc',
    license='BBSD',
    author='Guillaume Sottas',
    author_email='guillaumesottas@gmail.com',
    description='This tool generates the ECC data to be programmed into flash ECC of TMS570 Platform Series microcontrollers',
    entry_points={
        'console_scripts': ['pyecc=pyecc:main']
    },
    dependency_links=['http://github.com/Sauci/pyelf/tarball/master#egg=pyelf-0.1.0'],
    install_requires=['PyYAML==5.1.2'],
    include_package_data=True
)
