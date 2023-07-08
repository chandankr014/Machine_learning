# from typing import List

# HYPHEN_E_DOT = "-e ."


# def get_requirements(file_path:str)->List[str]:
#     # this function will return the list of requirements
#     req = []
#     with open('requirements.txt') as file_obj:
#         req = file_obj.readlines()
#         req = [r.replace("\n", "") for r in req]
#         if HYPHEN_E_DOT in req:
#             req.remove(HYPHEN_E_DOT)
#     return req

# print(get_requirements('requirements.txt'))

import logging

logging.basicConfig(level=logging.DEBUG)
logging.debug('This will get logged')