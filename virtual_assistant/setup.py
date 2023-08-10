from setuptools import setup, find_packages

setup(
    name='your_package_name',
    version='1.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'virtual_assistant=virtual_assistant.main:main',  # Replace with your entry point
        ],
    },
)
