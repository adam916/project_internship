# [START cloudrun_pubsub_server]
import base64
import json
import os

from flask import Flask, request

import image

app = Flask(__name__)
# [END cloudrun_pubsub_server]


# [START cloudrun_pubsub_handler]
# [START run_pubsub_handler]
@app.route("/", methods=["POST"])
def index():
    """Receive and parse Pub/Sub messages."""
    envelope = request.get_json()
    if not envelope:
        msg = "no Pub/Sub message received"
        print(f"error: {msg}")
        return f"Bad Request: {msg}", 400

    if not isinstance(envelope, dict) or "message" not in envelope:
        msg = "invalid Pub/Sub message format"
        print(f"error: {msg}")
        return f"Bad Request: {msg}", 400

    pubsub_message = envelope["message"]

    
    if isinstance(pubsub_message, dict) and "data" in pubsub_message:
        try:
            data = json.loads(base64.b64decode(pubsub_message['data']).decode())

        except Exception as e:
           msg = (
                "invalid Pub/Sub message: "
                "data property is not valid base64 encoded JSON"
           )
           print(f"error: {e}")
           return f"Bad Request: {msg}", 400
        
        # validate the message is a cloud storage event
        if not data["name"] or not data["bucket"]:
            msg = (
                "invalid cloud storage notification: "
                "expected name and bucket properties"
            )
            print(f"error: {e}")
            return f"Bad Request: {msg}", 400

        try:
            image.blur_offensive_images(data)
            return ("", 204)

        except Exception as e:
            print(f'error: {e}')
            return ("", 500)

    return ("", 500)
    

# [END run_pubsub_handler]
# [END cloudrun_pubsub_handler]
