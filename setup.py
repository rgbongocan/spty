from setuptools import setup

setup(
    name="spty",
    version="0.1",
    py_modules=["cli", "config", "volume", "play", "services"],
    install_requires=["spotipy", "click", "click-aliases", "ruamel.yaml"],
    entry_points="""
        [console_scripts]
        spty=cli:cli
    """,
    author="Renzo Gabriel Bongocan",
    author_email="gabrielbongocan@gmail.com",
    description="A simple spotify cli",
    url="https://github.com/rgbongocan/spty",
)
