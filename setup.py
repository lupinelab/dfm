from setuptools import find_packages, setup

setup(
    name="dfm",
    version="0.1.0",
    author="Jed Williamson",
    author_email="jed@lupinelab.co.uk",
    description="A dot file manager",
    packages=find_packages("."),
    install_requires=[
        "click",
        "pyyaml",
        "xdg-base-dirs",
    ],
    entry_points={"console_scripts": ["dfm = dfm.cli:cli"]}
)
