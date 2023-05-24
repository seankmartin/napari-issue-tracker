import napari
import pandas as pd
from magicgui.widgets import ComboBox, Container, FileEdit, PushButton


class DropdownSetupWidget(Container):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._dropdown_choices = ()
        self.append(
            ComboBox(name="Dropdown", choices=self.get_dropdown_choices, label="Select")
        )
        self.append(
            FileEdit(
                name="CSVSelect",
                label="CSV file to select based on",
                mode="r",
                filter="*.csv",
            )
        )
        self.append(PushButton(name="CSVButton", text="Update selection options"))

        self.CSVButton.changed.connect(self.update_dropdown_choices)

    def get_dropdown_choices(self, dropdown_widget):
        return self._dropdown_choices

    def update_dropdown_choices(self):
        path = self.CSVSelect.value
        if path.is_file():
            df = pd.read_csv(path)
            self._dropdown_choices = list(df.columns)
            self.Dropdown.reset_choices()

viewer = napari.Viewer()
viewer.window.add_dock_widget(DropdownSetupWidget())
napari.run()
