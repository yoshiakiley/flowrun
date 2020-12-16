import traceback
from contextlib import ContextDecorator


class error_suppress(ContextDecorator):

    def __init__(self, error_func, ):
        self.error_msg = error_func

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.error_msg()


def false():
    print('发送 echoer 错误', traceback.format_exc())
    return False


def connect_false():
    print('发送 echoer 错误', traceback.format_exc())
