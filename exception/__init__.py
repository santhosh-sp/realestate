import sys
from typing import Tuple

class APIException(Exception):
    
    def __init__(self, error_message:Exception,error_detail:sys): #type:ignore
        super().__init__(error_message)
        self.error_message, self.short_error_message =APIException.get_detailed_error_message(error_message=error_message,
                                                                       error_detail=error_detail
                                                                        )


    @staticmethod
    def get_detailed_error_message(error_message:Exception,error_detail:sys)->Tuple: # type:ignore
        """
         Description:
            method used to get the detailed error message with file name and line number , and also 
            to get the short error message 
         Args:
            error_message: Exception object
            error_detail: object of sys module
        
         Return:
            Retrns the tuple with error_message and the short error message
         
         Raise:
            None
        """

        short_error_message = error_message
        error_message = error_message
        try:

            _,_ ,exec_tb = error_detail.exc_info()

            if (exec_tb is not None):
                exception_block_line_number = exec_tb.tb_frame.f_lineno
                try_block_line_number = exec_tb.tb_lineno
                file_name = exec_tb.tb_frame.f_code.co_filename

                error_message = f"""
                Error occured in script: 
                [ {file_name} ] at 
                try block line number: [{try_block_line_number}] and exception block line number: [{exception_block_line_number}] 
                error message: [{error_message}]
                """
        except Exception as e:
            raise Exception(e.error_message) # type:ignore
        
        return (error_message,short_error_message)

    def __str__(self):
        return str(self.short_error_message)


    def __repr__(self) -> str:
        return APIException.__name__.str() # type:ignore

