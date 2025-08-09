from setuptools import setup, find_packages
from mypyc.build import mypycify


setup(
    name="complexint",

    # mypyc docs say to just set packages simply like this:
    #   packages=['complexint'],
    #
    # However: When I do that, complexint/__init__.py *itself* is included in the wheel which we don't want,
    #   because then the python version will be used instead of the mypyc-compiled pyd version.
    packages=find_packages(exclude=["complexint"]),

    ext_modules=mypycify([
        "complexint/__init__.py"
    ]),

    license="MIT",
)
