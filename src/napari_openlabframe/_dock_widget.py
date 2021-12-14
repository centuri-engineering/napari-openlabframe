"""
Simple webcam controler from a labthing webcam server
"""
import logging

from magicgui import widgets
from napari_plugin_engine import napari_hook_implementation

from .utilities import json_to_ndarray
from .usb_camera import get_image, set_resolution
from .motors import set_position, Stepper

log = logging.getLogger(__name__)
log.addHandler(logging.StreamHandler())


class OlfControler(widgets.Container):
    # your QWidget.__init__ can optionally request the napari viewer instance
    # in one of two ways:
    # 1. use a parameter called `napari_viewer`, as done here
    # 2. use a type annotation of 'napari.viewer.Viewer' for any parameter
    def __init__(self, napari_viewer):
        super().__init__()
        self.viewer = napari_viewer
        self.extend([get_image, set_resolution])
        self.extend([set_position, Stepper()])
        # self.extend([set_position])


@napari_hook_implementation
def napari_experimental_provide_dock_widget():
    # you can return either a single widget, or a sequence of widgets
    return OlfControler
