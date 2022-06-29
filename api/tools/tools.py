import requests
import time


def make_request(url: str):
    session = requests.session()
    request_results = session.get(url).json()["posts"]
    return request_results


def threadify(input_array: list, api_url: str, thread_lock, func):
    thread_lock.acquire()
    req_results = func(api_url)
    input_array.extend(req_results)
    time.sleep(1)
    thread_lock.release()


def get_uniques(array):
    return [
        _value for _key, _value in enumerate(array) if _value not in array[_key + 1 :]
    ]


def sort_array(array, sort_value, sort_direction):
    if sort_value is None:
        return sorted(
            array,
            key=lambda x: x["id"],
            reverse=True if sort_direction == "desc" else False,
        )

    elif sort_value in ["id", "reads", "likes", "popularity"]:
        return sorted(
            array,
            key=lambda x: x[sort_value],
            reverse=True if sort_direction == "desc" else False,
        )

    else:
        return {"error": "sortBy parameter is invalid"}
