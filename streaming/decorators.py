from concurrent import futures
from functools import wraps


def threaded(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        with futures.ThreadPoolExecutor() as executor:
            future = executor.submit(func, *args, **kwargs)
        frame = future.result()
        return frame

    return wrapper
