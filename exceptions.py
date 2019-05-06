"""
Custom exceptions used by Udata
Error handling in Udata is done by Exceptions.
This file will define a variety of exceptions

There is UdataError which every other exception should subclass so that it is
distinguished from other kind of exceptions not raised explicitly by Udata code.

All exceptions should be named CamelCase and always use the Error as suffix.
"""

import traceback

class UdataError(Exception):
    """
    All custom dsio exceptions should subclass this one.
    When printed, this class UdataError will always print its default message plus
    the message provided during exception initialization, if provided.
    """
    msg = "Udata Error"
    code = -1

    def __init__(self, msg=None, exec=None):
