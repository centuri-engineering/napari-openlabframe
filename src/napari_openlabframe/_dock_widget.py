"""
Simple webcam controler from a labthing webcam server
"""
import json
import logging
import time
from typing import Tuple

import requests


from napari_plugin_engine import napari_hook_implementation
from napari.types import LayerDataTuple
from magicgui import magicgui, widgets
from olf_control.things.utilities import json_to_ndarray

THING_URL = "http://localhost:7485"
log = logging.getLogger(__name__)
log.addHandler(logging.StreamHandler())


class WebcamControler(widgets.Container):
    # your QWidget.__init__ can optionally request the napari viewer instance
    # in one of two ways:
    # 1. use a parameter called `napari_viewer`, as done here
    # 2. use a type annotation of 'napari.viewer.Viewer' for any parameter
    def __init__(self, napari_viewer):
        super().__init__()
        self.viewer = napari_viewer
        self.extend([get_image, set_resolution])


@magicgui(auto_call=True)
def set_resolution(width: int = 640, height: int = 480) -> Tuple[int, ...]:

    req = requests.put(f"{THING_URL}/resolution", json=[width, height])
    log.info(req.status_code)
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


@napari_hook_implementation
def napari_experimental_provide_dock_widget():
    # you can return either a single widget, or a sequence of widgets
    return WebcamControler
