from setuptools import setup

with open("README.md", "r") as fp:
    long_description = fp.read()

setup(
    name="spty",
    version="0.1.3",
    py_modules=["cli", "config", "volume", "play", "services"],
    install_requires=["spotipy", "click", "click-aliases", "ruamel.yaml"],
    entry_points="""
        [console_scripts]
        spty=cli:cli
    """,
    author="Renzo Gabriel Bongocan",
    author_email="gabrielbongocan@gmail.com",
    description="A simple spotify cli",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rgbongocan/spty",
)
