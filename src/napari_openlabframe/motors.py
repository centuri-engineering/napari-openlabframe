import logging

import requests
from napari.types import LayerDataTuple
from magicgui import magicgui, widgets
from typing_extensions import Annotated

from .conf import THING_URL

log = logging.getLogger(__name__)
log.setLevel("INFO")
log.addHandler(logging.StreamHandler())


Pos = Annotated[float, {"min": -1.0, "max": 30.0, "step": 0.1}]
# labthing.add_view(Position, "/position")
# labthing.add_view(Step, "/actions/step")


@magicgui
def set_position(x: Pos = 0.0, y: Pos = 0.0):
    req = requests.put(f"{THING_URL}/position", json=[x, y])
    log.info("setting position got reply %s", req.status_code)


class Stepper(widgets.Container):
    def __init__(self):
        super().__init__(layout="vertical")

        left_btn = widgets.PushButton(name="Left", label="◀")
        left_btn.clicked.connect(self.move_left)

        right_btn = widgets.PushButton(name="Right", label="▶")
        right_btn.clicked.connect(self.move_right)
        leftright = widgets.Container(
            layout="horizontal", widgets=[left_btn, right_btn]
        )

        up_btn = widgets.PushButton(name="Up", label="▲")
        up_btn.clicked.connect(self.move_up)

        down_btn = widgets.PushButton(name="Down", label="▼")
        down_btn.clicked.connect(self.move_down)
        self.extend([up_btn, leftright, down_btn])

    def move_left(self, btn):
        req = requests.post(
            f"{THING_URL}/actions/step", json={"axis": "X", "step": -1.0}
        )
        log.info("steppin got reply %s", req.status_code)

    def move_right(self, btn):
        req = requests.post(
            f"{THING_URL}/actions/step", json={"axis": "X", "step": 1.0}
        )
        log.info("steppin got reply %s", req.status_code)

    def move_up(self, btn):
        req = requests.post(
            f"{THING_URL}/actions/step", json={"axis": "Y", "step": 1.0}
        )
        log.info("steppin got reply %s", req.status_code)

    def move_down(self, btn):
        req = requests.post(
            f"{THING_URL}/actions/step", json={"axis": "Y", "step": -1.0}
        )
        log.info("steppin got reply %s", req.status_code)