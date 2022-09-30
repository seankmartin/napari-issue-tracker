"""
See https://forum.image.sc/t/how-to-place-multiple-widgets-with-one-command-in-naparis-npe2/71145/2
"""
from qtpy.QtWidgets import QVBoxLayout, QPushButton, QWidget


class Example1Widget(QWidget):
    def __init__(self, napari_viewer):
        super().__init__()
        self.viewer = napari_viewer

        self.btn = QPushButton("Click me 1!")
        self.btn.clicked.connect(self._on_click)

        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.btn)

    def _on_click(self):
        print(f"Clicked widget 1, there are {len(self.viewer.layers)} layers")


class Example2Widget(QWidget):
    def __init__(self, napari_viewer):
        super().__init__()
        self.viewer = napari_viewer

        self.btn = QPushButton("Click me 2!")
        self.btn.clicked.connect(self._on_click)

        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.btn)

    def _on_click(self):
        print(f"Clicked widget 2, there are {len(self.viewer.layers)} layers")


class ExampleQWidget(QWidget):
    """
    This is the widget that combines the first two widgets.

    It also provides an extra button to run the two widgets that
    are contained in this widget in sequence.
    """

    def __init__(self, napari_viewer):
        super().__init__()
        w1 = Example1Widget(napari_viewer)
        w2 = Example2Widget(napari_viewer)
        self._children = [w1, w2]

        self.btn = QPushButton("Run 1 then 2")
        self.btn.clicked.connect(self._on_click)

        self.setLayout(QVBoxLayout())
        for w in [w1, w2, self.btn]:
            self.layout().addWidget(w)

    def _on_click(self):
        for w in self._children:
            w.btn.click()
