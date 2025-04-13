from setuptools import setup, find_packages

setup(
    name="request-forwarder-client",
    version="1.0.1",
    packages=find_packages(),
    install_requires=[
        "paho-mqtt",
    ],
    entry_points={
        "console_scripts": [
            "request-forwarder-client=client.main:subscribe",
        ],
    },
    author="Andrii Andriichuk",
    author_email="andrey000mar@gmail.com",
    description="A client for consuming request forwarder server requests",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/avrilfanomar/request-forwarder-client",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
