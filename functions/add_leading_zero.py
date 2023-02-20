def add_leading_zero(code):
    if code < 10:
        code = "0" + str(code)
    return code
