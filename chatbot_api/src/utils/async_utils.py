import asyncio
from functools import wraps


def async_retry_generator(max_retries: int = 3, delay: int = 1):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            for attempt in range(1, max_retries + 1):
                try:
                    # Iterate over the original async generator
                    async for result in func(*args, **kwargs):
                        yield result
                    
                    # If we reach here, the iteration finished successfully
                    return 
                
                except Exception as e:
                    print(f"Attempt {attempt} failed: {str(e)}")
                    if attempt == max_retries:
                        raise ValueError(f"Failed after {max_retries} attempts")
                    
                    await asyncio.sleep(delay)
        return wrapper
    return decorator