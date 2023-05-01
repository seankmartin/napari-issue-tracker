import pytest
import napari
from typing import Any
from qtpy.QtWidgets import QWidget
import numpy as np

class ChangeWidget(QWidget):

    def __init__(self, viewer: napari.viewer.Viewer):
        super().__init__()

        self.viewer = viewer
        self.layer_changed = False
        self.viewer.layers.selection.events.changed.connect(self.print)
        self.viewer.bind_key("Shift-E", self.func)
        self.viewer.bind_key("Shift-F", self.func)

    def func(self, _: napari.viewer.Viewer):
        print("Shift-E pressed")
    
    def print(self):
        print("The layer changed")
        print(list(self.viewer.keymap.keys()))

    def new_print(self):
        print("The layer changed after intialization")
        print(list(self.viewer.keymap.keys()))

def test_creating_widget_with_data(
    make_napari_viewer: Any,
) -> None:
    viewer = make_napari_viewer()
    viewer.add_image(
        np.zeros([3,3,3]),
        rgb=True,
    )
    widget = ChangeWidget(viewer)
    assert(not widget.layer_changed)

    print("We unselected the layer")
    viewer.layers.selection = []
    viewer.layers.selection.events.changed.disconnect()

    print("We selected the layer")
    viewer.layers.selection = [viewer.layers[0]]
    viewer.layers.selection.events.changed.connect(widget.new_print)