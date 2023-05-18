import napari
from napari.utils.notifications import show_info
from magicgui import magicgui
from magicgui.widgets import Container
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


@magicgui(
    filename={
        "label": "CSV file to select based on",
        "mode": "r",
        "filter": "*.csv",
    },
    call_button="Update selection options",
)
def selection_update_widget(viewer: napari.Viewer, filename=Path.home()):
    self = selection_update_widget
    if Path.home() != filename:
        _update_choices_on_file_changes(
            self, self._main_widget.select_widget1, _get_select1_list
        )
        _update_choices_on_file_changes(
            self, self._main_widget.select_widget2, _get_select2_list
        )


@magicgui(
    dropdown={"widget_type": "ComboBox", "choices": (), "label": "Select1"},
)
def select_widget1(viewer: napari.Viewer, dropdown):
    self = select_widget1
    if dropdown != "None":
        show_info(f"{dropdown} is chosen for {self.label}")


@magicgui(
    dropdown={"widget_type": "ComboBox", "choices": (), "label": "Select2"},
)
def select_widget2(viewer: napari.Viewer, dropdown):
    self = select_widget2
    if dropdown != "None":
        show_info(f"{dropdown} is chosen for {self.label}")


class WidgetHolder(Container):
    def append(self, item):
        super().append(item)
        item._main_widget = self


viewer = napari.Viewer()
widgets = [select_widget1, select_widget2, selection_update_widget]
viewer.window.add_dock_widget(WidgetHolder(widgets=widgets), name="Select1 and Select2")
napari.run()
