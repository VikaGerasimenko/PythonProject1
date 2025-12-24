from setuptools import setup, find_packages

setup(
    name="snake-game",
    version="1.0",
    packages=find_packages(),
    install_requires=[
        'pygame>=2.5.0',
        'pytest-timeout>=2.0.0',
    ],
    python_requires='>=3.6',
)
