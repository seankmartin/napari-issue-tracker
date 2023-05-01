import napari
import numpy as np
from magicgui import magic_factory

# private module, so this might break in the future!
from napari.utils._magicgui  import find_viewer_ancestor

CHOICES = [1,2,3,4,5]

def _get_choices(self):
    """
    Return available choices
    """
    # get the viewer (self will be the widget!)
    viewer = find_viewer_ancestor(self.native)
    if not viewer:
        return []

    layer = viewer.layers.selection.active
    if not layer:
        return []

    # this ensures used labels are absent
    labels = np.unique(layer.features.get('label', []))
    
    return sorted([l for l in CHOICES if l not in labels])


def _on_init(self):
    """
    equivalent to writing this in the __init__ of our widget
    """
    # this decorator ensures this is ran every time the widget is added to the viewer
    @self.parent_changed.connect
    def _connect_events():
        viewer = find_viewer_ancestor(self.native)
        if viewer:
            viewer.layers.selection.events.connect(self.current_label.reset_choices)


@magic_factory(
    widget_init=_on_init,
    current_label=dict(widget_type='ComboBox', choices=_get_choices)
)
def my_widget(layer: napari.layers.Points, current_label):
    ... # do stuff
    print(layer, current_label)

v = napari.Viewer()
v.window.add_dock_widget(my_widget())
v.add_points()