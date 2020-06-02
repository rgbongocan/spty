from setuptools import setup

setup(
    name="spfy",
    version="0.1",
    py_modules=["cli"],
    install_requires=["spotipy", "click", "click-aliases"],
    entry_points="""
        [console_scripts]
        spfy=cli:cli
    """,
)
