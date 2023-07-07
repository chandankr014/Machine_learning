from setuptools import find_packages, setup
from typing import List

HYPHEN_E_DOT = "-e ."

def get_requirements(file_path:str)->List[str]:
    # this function will return the list of requirements
    req = []
    with open('requirements.txt') as file_obj:
        req = file_obj.readlines()
        req = [r.replace("\n", "") for r in req]

        if HYPHEN_E_DOT in req:
            req.remove(HYPHEN_E_DOT)
    return req


setup(
    name='MLproject',
    version='0.0.1',
    author='Chandan',
    author_email='chandankr014@gmail.com',
    packages=find_packages(),
    # install_requires=['pandas', 'numpy', 'seaborn']
    install_requires = get_requirements('requirements.txt')
)
