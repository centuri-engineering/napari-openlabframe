"""
Simple webcam controler from a labthing webcam server
"""
import json
import time
import requests

from napari_plugin_engine import napari_hook_implementation
from napari.types import LayerDataTuple
from magicgui import magicgui, widgets
from olf_control.things.utilities import json_to_ndarray


class WebcamControler(widgets.Container):
    # your QWidget.__init__ can optionally request the napari viewer instance
    # in one of two ways:
    # 1. use a parameter called `napari_viewer`, as done here
    # 2. use a type annotation of 'napari.viewer.Viewer' for any parameter
    def __init__(self, napari_viewer):
        super().__init__()
        self.viewer = napari_viewer
        self.labthing_url = "http://localhost:7485"
        self.extend([self.get_image, self.set_resolution])

    @magicgui
    def set_resolution(self, width: int = 640, height: int = 480):
        requests.post(
            f"{self.labthing_url}/resolution", data={"resolution": [width, height]}
        )

    @magicgui
    def get_image(self, n_averages: int = 3) -> LayerDataTuple:
        requests.post(
            f"{self.labthing_url}/actions/average", data={"averages": n_averages}
        )
        while True:
            response = requests.get(f"{self.labthing_url}/actions/average").json()[0]
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
