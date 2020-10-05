from concurrent import futures
from functools import wraps


def threaded(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        with futures.ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(func)
        frame = future.result()
        return frame

    return wrapper
