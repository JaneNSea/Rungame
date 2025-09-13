from setuptools import setup, find_packages

setup(
    name="pixel-runner-game",
    version="1.0.0",
    description="A fun pixel-style endless runner game",
    author="Aura",
    author_email="aura@example.com",
    packages=find_packages(),
    install_requires=[
        "pygame>=2.5.0",
        "numpy>=1.24.0",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "pixel-runner=src.main:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
