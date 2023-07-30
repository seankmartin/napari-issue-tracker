# Load the lily sample in napari, save it as a tiff file, and load it again.
import numpy as np
import tifffile
from napari import Viewer, run

viewer = Viewer()
viewer.open_sample(
    plugin="napari",
    sample="lily",
    reader_plugin="",
)
layers = viewer.layers
image_shape = layers[0].data.shape
array_size = (image_shape[0], image_shape[1], 4)
data = np.zeros(shape=array_size, dtype=np.uint16)
for i, layer in enumerate(layers):
    data[:, :, i] = layer.data

tifffile.imwrite("lily.tif", data)
viewer.layers.clear()
loaded_data = tifffile.imread("lily.tif", key=0, series=0, is_ome=False, aszarr=False)
viewer.add_image(
    loaded_data,
    channel_axis=-1,
    colormap=["red", "green", "gray", "blue"],
    name=["lily-R", "lily-G", "lily-W", "lily-B"],
)
run()
