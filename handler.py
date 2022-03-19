import json
import PIL.Image
import numpy as np

import PIL
def hello(event, context):
    dependencies = {
        "numpy": np.__version__,
        "Pillow": PIL.__version__
    }
    
    body = {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "input": event,
        "dependencies": dependencies
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response

    # Use this code if you don't use the http event with the LAMBDA-PROXY
    # integration
    """
    return {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "event": event
    }
    """
