# Load the lily sample in napari, save it as a tiff file, and load it again.
from napari import Viewer, run

viewer = Viewer()
viewer.open_sample(
    plugin="napari",
    sample="lily",
    reader_plugin="",
)
layers = viewer.layers
for layer in layers:
    layer.save(f"{layer.name}.png")

run()
