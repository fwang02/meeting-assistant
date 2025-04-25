def remove_first_and_last_line(text: str) -> str:
    """
    Remove the first and last lines from the given text.
    """
    lines = text.split("\n")
    if len(lines) > 2:
        return "\n".join(lines[1:-1])
    return ""