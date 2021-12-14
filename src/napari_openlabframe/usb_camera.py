import json
import logging
import time
from typing import Tuple

import requests

from napari.types import LayerDataTuple
from magicgui import magicgui, widgets

from .utilities import json_to_ndarray
from .conf import THING_URL

log = logging.getLogger(__name__)
log.addHandler(logging.StreamHandler())


@magicgui(auto_call=True)
def set_resolution(width: int = 640, height: int = 480) -> Tuple[int, ...]:
    """Defines the resolution of the acquired image"""
    req = requests.put(f"{THING_URL}/resolution", json=[width, height])
    log.info("setting resolution got reply %s", req.status_code)
    log.debug(req.json())
    return [width, height]


@magicgui
def get_image(n_averages: int = 3) -> LayerDataTuple:
    requests.post(f"{THING_URL}/actions/average", json={"averages": n_averages})
    while True:

        # wait for response
        responses = requests.get(f"{THING_URL}/actions/average").json()
        if not responses:
            time.sleep(0.01)
            continue

        response = responses[-1]
        completed = response["status"] == "completed"
        if completed:
            data = json_to_ndarray(json.loads(response["output"]))
            break
        time.sleep(0.01)
    return (data, {"name": "webcam image"}, "Image")
