#See https://forum.image.sc/t/pytest-make-napari-viewer-changes-selected-layer-when-initializing-custom-key-binding/79798/2

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

    def func(self, _: napari.viewer.Viewer):
        print("Shift-E pressed")
    
    def print(self):
        print("The layer changed")
        self.layer_changed = True

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
    return widget


if __name__ == "__main__":
    widget = test_creating_widget_with_data(napari.Viewer)
    print("Layer changed" if widget.layer_changed else "Layer unchanged")
    napari.run()
