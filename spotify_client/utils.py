def iterate_array_in_chunks(arr, size: int):
    """Generator that splits the given array in chunks with a max length of "size"."""
    for i in range(0, len(arr), size):
        yield arr[i:i+size]


def clear_dict(d: dict) -> dict:
    """Given a dict, return a copy of it, excluding keys with None values.
    Does not recursively clear nested dicts."""
    # TODO delete if not used
    return {k: v for k, v in d.items() if v is not None}


def safe_dict(d: dict) -> dict:
    """Given a dict, return a copy of it, excluding keys that might hold sensitive information"""
    return {k: v for k, v in d.items() if not any(chunk in k for chunk in ["token"])}
