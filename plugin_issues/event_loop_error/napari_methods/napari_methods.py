# See https://forum.image.sc/t/package-pyqt-in-napari-plugin-not-work-due-to-event-loop/71219/3

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import *
from qtpy.QtWidgets import QTreeView, QDirModel
import napari
from aicsimageio import AICSImage
import json


class uic(object):
    def init(self, viewer):
        super(uic, self).init()
        self.viewer = viewer
        self.labelwidgets = []
        self.valuewidgets = []
        self.initUI()
        self.initTrigger()
        self.row = -1
        self.kws = []
        self.vws = []
        self.PARAMS = {}
        self.kvsi = 0
        self.filename = ""
        self.imgfilepath = ""
        self.meta_dim = []
        self.paramkey = []
        self.paramvalue = []
        self.hswidgets = []
        self.customized_setting = {}

    def initUI(self):
        self.headcontentlayout = QVBoxLayout()
        self.headcontentwidget = QWidget()
        self.headcontentwidget.setLayout(self.headcontentlayout)

        self.head1 = QHBoxLayout()
        self.inputimglb = QLabel("Image")
        self.head1.addWidget(self.inputimglb)
        self.imgfilele = QLineEdit()
        self.head1.addWidget(self.imgfilele)
        self.selbtn1 = QPushButton("Select File")
        self.head1.addWidget(self.selbtn1)
        self.headcontentlayout.addLayout(self.head1)
        self.head2 = QHBoxLayout()
        self.jsonlb = QLabel("Micro Meta App json file")
        self.head2.addWidget(self.jsonlb)
        self.jsonfilele = QLineEdit()
        self.head2.addWidget(self.jsonfilele)
        self.selbtn = QPushButton("Select File")
        self.head2.addWidget(self.selbtn)
        self.headcontentlayout.addLayout(self.head2)

        self.labelwidgets.append(self.inputimglb)
        self.valuewidgets.append(self.imgfilele)
        self.labelwidgets.append(self.jsonlb)
        self.valuewidgets.append(self.jsonfilele)

        self.head3 = QHBoxLayout()
        self.runbtn = QPushButton("Run")
        self.head3.addWidget(self.runbtn)
        self.headcontentlayout.addLayout(self.head3)
        self.viewer.window.add_dock_widget(self.headcontentwidget, name="Select File")
        self.contentwidget = QWidget()
        self.contentlayout = QGridLayout()
        self.contentwidget.setLayout(self.contentlayout)
        self.contentwidget.setMinimumWidth(480)

    def initTrigger(self):
        self.selbtn1.clicked.connect(self.selctImgFile)
        self.selbtn.clicked.connect(self.selctJsonFile)
        self.runbtn.clicked.connect(self.run)

    def selctImgFile(self):
        self.imgfilepath = QFileDialog.getOpenFileName(
            self.contentwidget,
            "Select Json File",
            "",
            "img(*.tif *.png *.jpg);;All files (*.*)",
        )[0]
        print(self.imgfilepath)
        if self.imgfilepath:
            im = AICSImage(self.imgfilepath)
            self.viewer.open(self.imgfilepath)
            self.meta_dim = list(im.dims["X", "Y", "C", "Z", "T"])
            self.imgfilele.setText(self.imgfilepath)

    def selctJsonFile(self):
        self.filename = QFileDialog.getOpenFileName(
            self.contentwidget, "Select Json File", "", "Json(*.json)"
        )[0]
        print(self.filename)
        if self.filename:
            self.jsonfilele.setText(self.filename)

    def run(self):
        print("Run successfully.")


def methods_main():
    viewer = napari.Viewer()
    ui = uic(viewer)
    napari.run(max_loop_level=2)
