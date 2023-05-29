from magicgui.types import FileDialogMode
from magicgui.widgets import CheckBox, FileEdit, Slider, Table
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (QApplication, QComboBox, QLabel, QPushButton,
                             QVBoxLayout, QWidget)


class segment_with_czann(QWidget):
    """Widget allows selection of an Image layer, a model file
    and the desired border width and returns as many new layers
    as the segmentation model has classes.
    For a regression model is return the processed image. Currently only one
    output channel is supported for regression models aka "Image-2-Image"

    Important: Segmentation and processing is done Slice-by-Slice.

    """

    def __init__(self, napari_viewer):
        """Initialize widget
        Parameters
        ----------
        napari_viewer : napari.utils._proxies.PublicOnlyProxy
            public proxy for the napari viewer object
        """
        super().__init__()
        self.viewer = napari_viewer

        # set default values
        self.min_overlap: int = 128
        self.model_metadata = None
        self.model_type = "Segmentation"
        self.czann_file: str = ""
        self.dnn_tile_width = 1024
        self.dnn_tile_height = 1024
        self.dnn_channel_number = 1
        self.scaling = (1.0, 1.0)
        self.use_gpu: bool = True
        self.input_shape = (1024, 1014, 1)
        self.output_shape = (1024, 1024, 2)

        # create a layout
        self.setLayout(QVBoxLayout())

        # add a label
        self.layout().addWidget(QLabel("Model File Selection"))

        # define filter based on file extension
        model_extension = "*.czann"

        # create the FileEdit widget and add to the layout and connect it
        self.filename_edit = FileEdit(
            mode=FileDialogMode.EXISTING_FILE, value="", filter=model_extension
        )

        self.layout().addWidget(self.filename_edit.native)

        # add table for model metadata
        self.model_metadata_label = QLabel("Model Metadata")
        self.model_metadata_label.setFont(QFont("Arial", 9, QFont.Normal))

        # setting up background color and border
        # self.model_metadata_label.setStyleSheet("background-color: yellow;border: 1px solid black;")
        self.layout().addWidget(self.model_metadata_label)

        self.model_metadata_table = Table()
        # self.model_metadata_table.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        # self.model_metadata_table.setFixedSize(QSize(275, 250))
        self.layout().addWidget(self.model_metadata_table.native)

        # add button for reading the model metadata
        self.read_modeldata_btn = QPushButton("Reload minimum overlap")
        self.layout().addWidget(self.read_modeldata_btn)

        # add label and slider for adjusting the minimum overlap
        self.min_overlap_label = QLabel("Adjust minimum overlap")
        self.min_overlap_slider = Slider(
            orientation="horizontal",
            label="Minimum Overlap",
            value=128,
            min=1,
            max=256,
            step=1,
            readout=True,
            tooltip="Adjust the desired min. overlap",
            tracking=False,
        )

        self.layout().addWidget(self.min_overlap_label)
        self.layout().addWidget(self.min_overlap_slider.native)

        # add the checkbox the use the GPU for the inference
        self.use_gpu_checkbox = CheckBox(
            name="Use GPU (experimental)",
            visible=True,
            enabled=True,
            value=self.use_gpu,
        )
        self.layout().addWidget(self.use_gpu_checkbox.native)

        # make button for reading the model metadata
        self.segment_btn = QPushButton("Segment or Process selected Image Layer")
        self.segment_btn.setEnabled(False)
        self.segment_btn.clicked.connect(self._segment)
        self.layout().addWidget(self.segment_btn)

        self.enable_button = QPushButton("Enable")
        self.enable_button.clicked.connect(self._enable_button)
        self.layout().addWidget(self.enable_button)
    
    def _segment(self):
        print("Segmenting")
    
    def _enable_button(self):
        self.segment_btn.setEnabled(True)


import napari

viewer = napari.Viewer()
viewer.window.add_dock_widget(segment_with_czann(viewer), name="Segment with CZANN")
napari.run()
