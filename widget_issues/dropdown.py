import napari
from magicgui import magicgui
import numpy as np


def my_widget():
    @magicgui(
        dropdown={"widget_type": "ComboBox", "choices": ()},
        text_input={"widget_type": "LineEdit"},
    )
    def widget(viewer: napari.Viewer, dropdown, text_input):
        print(widget.dropdown)
        if text_input != "":
            widget.dropdown.choices = np.append(widget.dropdown.choices, text_input)
            widget.dropdown.value = text_input

    return widget


viewer = napari.Viewer()
viewer.window.add_dock_widget(my_widget())
napari.run()
