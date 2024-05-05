def error_result(err_msg: str):
    """
    shorthand to return an error with your error message
    """
    return {
        "success": False,
        "msg": err_msg
    }