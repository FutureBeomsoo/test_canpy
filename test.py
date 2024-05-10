import can


# With an error code (it also works with a specific error):
error = can.exceptions.CanOperationError(message="Failed to do the thing", error_code=42)
print(error)
'Failed to do the thing [Error Code 42]'

# Missing the error code:
plain_error = can.exceptions.CanError(message="Something went wrong ...")
print(plain_error)
'Something went wrong ...'