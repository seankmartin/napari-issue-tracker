import napari
from napari.utils.notifications import show_info
from magicgui import magicgui
from pathlib import Path
import pandas as pd


def _get_select1_list(df):
    return df.columns


def _get_select2_list(df):
    return df["SampleID"].drop_duplicates()


def _update_choices_on_file_changes(parent_widget, select_widget, get_choices_function):
    filename = parent_widget.filename.value
    df = pd.read_csv(filename)
    choices = get_choices_function(df)
    select_widget.dropdown.choices = choices


def my_two_widget_holder(widget1, widget2):
    @magicgui(
        filename={
            "label": "CSV file to select based on",
            "mode": "r",
            "filter": "*.csv",
        },
        call_button="Update selection options",
    )
    def widget(viewer: napari.Viewer, filename=Path.home()):
        if Path.home() != filename:
            _update_choices_on_file_changes(widget, widget1, _get_select1_list)
            _update_choices_on_file_changes(widget, widget2, _get_select2_list)

    return widget


def my_select_widget(label):
    @magicgui(
        dropdown={"widget_type": "ComboBox", "choices": (), "label": label},
    )
    def widget(viewer: napari.Viewer, dropdown):
        if dropdown != "None":
            show_info(f"{dropdown} is chosen for {label}")

    return widget


viewer = napari.Viewer()
w1 = my_select_widget("Select1")
w2 = my_select_widget("Select2")
w3 = my_two_widget_holder(w1, w2)
viewer.window.add_dock_widget(w1, name="Select1")
viewer.window.add_dock_widget(w2, name="Select2")
viewer.window.add_dock_widget(w3, name="Select1 and Select2")
napari.run()
