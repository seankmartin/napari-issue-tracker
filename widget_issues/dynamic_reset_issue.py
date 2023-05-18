# See https://forum.image.sc/t/dynamic-select-options-reset/81159

import napari
import os
from magicgui import magicgui
from napari.utils.notifications import show_info
from skimage.io import imread
from pathlib import Path
import pandas as pd

root_directory_path = r"C:\Users\user\Documents\GitHub\Napari-Cell-Labeling\Napari-Cell-Labeling\test_data"


def get_proteins_list(df):
    proteins_list = df.columns.tolist()
    return proteins_list


DEFAULT_CHOICES_PATIENTS = []


def patient_selection():
    @magicgui(
        dropdown=dict(
            widget_type="ComboBox",
            choices=DEFAULT_CHOICES_PATIENTS,
            label="Patient:",
        ),
        call_button="Select Patient",
    )
    def widget(viewer: napari.Viewer, dropdown):
        global patient_number
        patient_number = int(dropdown)
        show_info(f"patient {patient_number} is chosen")

        directory_path = os.path.join(root_directory_path, str(patient_number))
        files = os.listdir(directory_path)
        list_img = [(os.path.join(directory_path, file)) for file in files]
        colors = list(napari.utils.colormaps.AVAILABLE_COLORMAPS)
        for img in list_img:
            channel_image = imread(img)
            img_name = os.path.basename(img)
            viewer.add_image(channel_image, name=img_name, colormap=colors[0])
        show_info(f"patient images uploaded successfully")
        find_anomaly_button.setVisible(True)

    return widget


DEFAULT_CHOICES_find_anomalies = []


def find_anomlay():
    @magicgui(
        dropdown=dict(
            widget_type="ComboBox",
            choices=DEFAULT_CHOICES_find_anomalies,
            label="Proteins Options",
        ),
        call_button="Find anomalies",
    )
    def widget(viewer: napari.Viewer, dropdown):
        protein = dropdown
        show_info(f"{protein} is chosen")
        # proteins_list = get_proteins_list(df)
        # inside this function we will add some images to the viewer:
        # find_anomaly.main(viewer, patient_number, protein, proteins_list)

    return widget


def upload_CellTable_and_cellLabelImage(patients_widget, find_anomaly_widget):
    @magicgui(
        filename={
            "label": "CSV file with proteins to predict",
            "mode": "r",
            "filter": "*.csv",
        },
        foldername={
            "label": "folder with cellLabeled Images of the patients",
            "mode": "d",
        },
        call_button="Update files Uploading",
    )
    def widget(viewer: napari.Viewer, filename=Path.home(), foldername=Path.home()):
        if Path.home() != filename:
            show_info(f"cellTable uploaded successfully")
        if Path.home() != foldername:
            show_info(f"cellLabelImages uploaded successfully")
        if filename != Path.home() and foldername != Path.home():
            _update_protein_choices_on_file_changes(widget, find_anomaly_widget)
            _update_patient_choices_on_file_changes(widget, patients_widget)
            patient_selection_button.setVisible(True)

    return widget


def _update_protein_choices_on_file_changes(filename_widget, dropdown_widget):
    filename = filename_widget.filename.value
    df = pd.read_csv(filename)
    choices = get_proteins_list(df)
    dropdown_widget.dropdown.choices = choices


def _update_patient_choices_on_file_changes(filename_widget, patients_widget):
    filename = filename_widget.filename.value
    df = pd.read_csv(filename)
    choices = df["SampleID"].drop_duplicates()
    patients_widget.dropdown.choices = choices


viewer = napari.Viewer()
find_anomaly_widget = find_anomlay()
patients_widget = patient_selection()
upload_csv_button = viewer.window.add_dock_widget(
    upload_CellTable_and_cellLabelImage(patients_widget, find_anomaly_widget),
    name="Upload cellTable and cellLabelImages",
)
patient_selection_button = viewer.window.add_dock_widget(patients_widget, area="right")
find_anomaly_button = viewer.window.add_dock_widget(find_anomaly_widget, area="right")

napari.run()