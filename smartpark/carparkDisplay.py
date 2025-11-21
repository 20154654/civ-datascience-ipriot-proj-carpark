from interfaces import CarparkDataProvider
from windowDisplay import WindowedDisplay
import threading
import time

class CarParkDisplay:
    """Provides a simple display of the car park status. This is a skeleton only. 
    The class is designed to be customizable without requiring and understanding of tkinter or threading."""
    # determines what fields appear in the UI
    fields = ['Available bays', 'Temperature', 'At']

    def __init__(self,root, title: str):
        self.window = WindowedDisplay(root,
            title, CarParkDisplay.fields)
        self.window.show()
        self._provider=None
    
    @property
    def data_provider(self):
        return self._provider
    @data_provider.setter
    def data_provider(self,provider):
        if isinstance(provider,CarparkDataProvider):
            self._provider=provider
            self.update_display

    def update_display(self):
        field_values = dict(zip(CarParkDisplay.fields, [
            f'{self._provider.available_spaces:03d}',
            # update so the temperature not formated into integer but float
            #f'{self._provider.temperature:02d}℃',
            f'{self._provider.temperature:.1f}℃',
            time.strftime("%H:%M:%S",self._provider.current_time)
        ]))
        self.window.update(field_values)


