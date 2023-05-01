# https://forum.image.sc/t/select-button-update-options-dynamically/80367/3

from enum import Enum
from pathlib import Path

from magicgui import magicgui


class Options_Proteins(Enum):
    CD11b = "CD11b"


@magicgui(
    dropdown=dict(widget_type="Select", choices=Options_Proteins),
    call_button="Predict Proteins",
    filename={"label": "CSV file with proteins to predict", "mode": "r"},
)
def proteins_predict(dropdown=Options_Proteins.CD11b, filename=Path.home()):
    proteins_list_to_predict = [protein.name for protein in dropdown]
    print(proteins_list_to_predict)
    return
