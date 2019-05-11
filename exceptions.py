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
        if exec is None and isinstance(msg, Exception):
            msg, exec = repr(msg), msg
        self.orig_exec = exec if isinstance(exec, Exception) else None
        self.orig_traceback = traceback.format_exc()
        msg = "%s: %s" %(self.msg, msg) if msg is not None else self.msg
        super(UdataError, self).__init__(msg)


class ModuleLoadError(UdataError):
    msg = "Error loading module"
    code = 1

class ElasticsearchConnectionError(UdataError):
    msg = "Cannot connect to Elasticsearch"
    code = 2