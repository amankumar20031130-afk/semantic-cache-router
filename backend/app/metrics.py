import time


def calculate_cost(model: str, input_tokens: int, output_tokens: int):
    """
    Calculate estimated cost for a request.

    Prices are estimates and can be updated later.
    """

    pricing = {
        "openai/gpt-oss-20b": {
            "input": 0.00000010,
            "output": 0.00000050
        },
        "openai/gpt-oss-120b": {
            "input": 0.00000015,
            "output": 0.00000060
        }
    }

    model_price = pricing.get(model)

    if not model_price:
        return 0.0

    input_cost = input_tokens * model_price["input"]
    output_cost = output_tokens * model_price["output"]

    return input_cost + output_cost


def start_timer():
    return time.perf_counter()


def calculate_latency(start_time):
    return round(
        (time.perf_counter() - start_time) * 1000,
        2
    )