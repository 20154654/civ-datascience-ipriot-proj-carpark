from interfaces import CarparkSensorListener
import tkinter as tk

class CarDetectorWindow:
    """Provides a couple of simple buttons that can be used to represent a sensor detecting a car. This is a skeleton only."""

    def __init__(self,root):
        self.root=root
        self.root.title("Car Detector ULTRA")

        self.btn_incoming_car = tk.Button(
            self.root, text='🚘 Incoming Car', font=('Arial', 50), cursor='right_side', command=self.incoming_car)
        self.btn_incoming_car.grid(padx=10, pady=5,row=0,columnspan=2)
        self.btn_outgoing_car = tk.Button(
            self.root, text='Outgoing Car 🚘',  font=('Arial', 50), cursor='bottom_left_corner', command=self.outgoing_car)
        self.btn_outgoing_car.grid(padx=10, pady=5,row=1,columnspan=2)
        self.listeners=list()
        self.temp_label=tk.Label(
            self.root, text="Temperature", font=('Arial', 20)
        )
        self.temp_label.grid(padx=10, pady=5,column=0,row=2)
        self.temp_var=tk.StringVar()
        # update original code so the temperature only update when the value is valid
        self.temp_var.trace_add("write", self._on_temp_change)
        #self.temp_var.trace_add("write",lambda x,y,v: self.temperature_changed(float(self.temp_var.get())))
        self.temp_box=tk.Entry(
            self.root,font=('Arial', 20),textvariable=self.temp_var
        )
        self.temp_box.grid(padx=10, pady=5,column=1,row=2)

        self.plate_label=tk.Label(
            self.root, text="License Plate", font=('Arial', 20)
        )
        self.plate_label.grid(padx=10, pady=5,column=0,row=3)
        self.plate_var=tk.StringVar()
        self.plate_box=tk.Entry(
            self.root,font=('Arial', 20),textvariable=self.plate_var
        )
        self.plate_box.grid(padx=10, pady=5,column=1,row=3)
    

    def _on_temp_change(self, *args):
        value = self.temp_var.get().strip()

        if value =="":
            return
        
        try:
            temp = float(value)
        except ValueError:
            print(f"Invalid temperature input: {value}")
            return
        
        self.temperature_changed(temp)


    @property
    def current_license(self):
        return self.plate_var.get()

    def add_listener(self,listener):
        if isinstance(listener,CarparkSensorListener):
            self.listeners.append(listener)

    def incoming_car(self):
        for listener in self.listeners:
            listener.incoming_car(self.current_license)

    def outgoing_car(self):
        for listener in self.listeners:
            listener.outgoing_car(self.current_license)

    def temperature_changed(self,temp):
        for listener in self.listeners:
            listener.temperature_reading(temp)

