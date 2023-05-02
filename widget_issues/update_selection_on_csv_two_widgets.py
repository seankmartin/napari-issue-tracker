# https://forum.image.sc/t/select-button-update-options-dynamically/80367/3

import napari
import pandas as pd
from napari.utils.notifications import show_warning
from pathlib import Path

from magicgui import magicgui


DEFAULT_CHOICES = ["CD11b", "CD11c", "CD16", "CD20", "CD31", "CD45", "CD45R0"]


def _update_choices_on_file_change(filename_widget, dropdown_widget):
    """Return available choices of proteins from csv headers"""
    filename = filename_widget.filename.value
    choices = None
    if filename.is_file():
        if filename.suffix == ".csv":
            df = pd.read_csv(filename)
            choices = df.columns
        else:
            show_warning(f"File {filename} is not a .csv file.")
    if choices is not None:
        dropdown_widget.dropdown.choices = choices


def proteins_predict():
    @magicgui(
        dropdown=dict(
            widget_type="Select", choices=DEFAULT_CHOICES, label="Proteins to predict"
        ),
        call_button="Predict Proteins",
    )
    def widget(viewer: napari.Viewer, dropdown):
        # Perform the prediction here
        proteins_list_to_predict = dropdown
        print(proteins_list_to_predict)

    return widget


def protein_options(protein_widget):
    @magicgui(
        filename={
            "label": "CSV file with proteins to predict",
            "mode": "r",
            "filter": "*.csv",
        },
        call_button="Set possible proteins from file",
    )
    def widget(viewer: napari.Viewer, filename=Path.home()):
        _update_choices_on_file_change(widget, protein_widget)

    return widget


v = napari.Viewer()
protein_widget = proteins_predict()
v.window.add_dock_widget(protein_widget, name="Predict proteins")
v.window.add_dock_widget(protein_options(protein_widget), name="Set proteins")
napari.run()
