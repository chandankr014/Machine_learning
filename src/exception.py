import sys
from src.logger import logging


def error_message_detail(error, error_detail:sys):
    _1, _2, exc_tb = error_detail.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename
    error_message = "Error occured in python script [{0}] at line [{1}] error msg [{2}]".format(
        file_name, exc_tb.tb_lineno, str(error)
    )
    return error_message

class CustomException(Exception):
    # when 2 params are given into CustomException it goes here
    def __init__(self, error_message, error_detail:sys):
        super().__init__(error_message)
        self.error_message = error_message_detail(error=error_message, error_detail=error_detail)

    # when one param(string) is provided it goes here
    def __str__(self):
        return self.error_message
    
# main function
if __name__ == "__main__":
    try:
        # a = 1/0
        f = open('myfile.txt')
    except Exception as e:
        logging.info("file not found")
        raise CustomException(e, sys)

