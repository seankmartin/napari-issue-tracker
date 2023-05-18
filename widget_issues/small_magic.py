from magicgui import magicgui
from magicgui.widgets import Container

@magicgui
def widget_a(param=1):
    pass

@magicgui
def widget_b(param='a'):
    # in here think of `widget_b` as the same as `self` in an instance method
    self = widget_b  # for clarity
    print(self._main_widget.widget_a.value, param)


class MyContainer(Container):
    def append(self, item):
        super().append(item)
        item._main_widget = self

widg = MyContainer(widgets=[widget_a, widget_b])
widg.show()

wait = input("Press enter to continue.")