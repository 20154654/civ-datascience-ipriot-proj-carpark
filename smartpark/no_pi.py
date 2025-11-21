"""The following code is used to provide an alternative to students who do not have a Raspberry Pi.
If you have a Raspberry Pi, or a SenseHAT emulator under Debian, you do not need to use this code.
"""

import tkinter as tk
import carparkManager as carparkManager
import carparkDetector as carparkDetector
import carparkDisplay as carparkDisplay


if __name__ == '__main__':
    root = tk.Tk()

    carpark_manager=carparkManager.CarparkManager()

    display=carparkDisplay.CarParkDisplay(root, title=carpark_manager.location)
    display.data_provider=carpark_manager
    carpark_manager.register_display(display)

    detector=carparkDetector.CarDetectorWindow(root)
    detector.add_listener(carpark_manager)

    root.mainloop()
