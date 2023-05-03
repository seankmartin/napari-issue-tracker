import napari
from magicgui import magicgui


def my_two_button_widget():
    @magicgui(
        other_button=dict(widget_type="PushButton", text="Other run button"),
        call_button="Main run button",
        select=dict(widget_type="Select", choices=["a", "b", "c"])
    )
    def widget(other_button, select):
        print("Clicked the main button")
        print("Choices are ", select)
    
    @widget.other_button.changed.connect
    def do_something_with_other_button(event=None):
        print("Clicked the other button")
        print("Choices are ", widget.select.value)
    
    return widget

v = napari.Viewer()
v.window.add_dock_widget(my_two_button_widget(), name="Two button widget")
napari.run()
