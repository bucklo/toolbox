import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="toolbox",
    version="0.0.1",
    author="Simon Richardson",
    author_email="simon@richardson.nu",
    descriptioon="A collection of tools for use in my projects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bucklo/toolbox",
    packages=['toolbox'],
    install_requires=[
        'requests',
        'pyVim',
        'pyVmomi',
        'ssl',
        'json'
    ],
)
