import napari
from magicgui import magic_factory


def _on_init(widget):
    @widget.other_button.clicked.connect
    def do_something_with_other_button():
        # Perform other run button function here
        print("Clicked the other button")


@magic_factory(
    widget_init=_on_init,
    other_button=dict(widget_type="PushButton", text="Other run button"),
    call_button="Main run button",
)
def my_two_button_widget(other_button):
    # Peform main run button function here
    print("Clicked the main button")


v = napari.Viewer()
v.window.add_dock_widget(my_two_button_widget(), name="Two button widget")
napari.run()
