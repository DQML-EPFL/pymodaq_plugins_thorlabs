
from typing import Union, List, Dict
from pymodaq.control_modules.move_utility_classes import (DAQ_Move_base, comon_parameters_fun,
                                                          main, DataActuatorType, DataActuator)

from pymodaq_utils.utils import ThreadCommand  # object used to send info back to the main thread
from pymodaq_gui.parameter import Parameter

import os
import time
import sys
import clr

# Add References to .NET libraries
clr.AddReference("C:\\Program Files\\Thorlabs\\Kinesis\\Thorlabs.MotionControl.Benchtop.PiezoCLI.dll")
clr.AddReference("C:\\Program Files\\Thorlabs\\Kinesis\\Thorlabs.MotionControl.DeviceManagerCLI.dll.")
clr.AddReference("C:\\Program Files\\Thorlabs\\Kinesis\\Thorlabs.MotionControl.GenericPiezoCLI.dll")

from Thorlabs.MotionControl.DeviceManagerCLI import *
from Thorlabs.MotionControl.Benchtop.PiezoCLI import *
from Thorlabs.MotionControl.Benchtop.PiezoCLI.PDXC2 import *
from Thorlabs.MotionControl.GenericPiezoCLI.Piezo import *


from Thorlabs.MotionControl.DeviceManagerCLI import DeviceManagerCLI

class DAQ_Move_PDXC2(DAQ_Move_base):
    """ Instrument plugin class for an actuator.
    
    This object inherits all functionalities to communicate with PyMoDAQ’s DAQ_Move module through inheritance via
    DAQ_Move_base. It makes a bridge between the DAQ_Move module and the Python wrapper of a particular instrument.

    TODO Complete the docstring of your plugin with:
        * The set of controllers and actuators that should be compatible with this instrument plugin.
        * With which instrument and controller it has been tested.
        * The version of PyMoDAQ during the test.
        * The version of the operating system.
        * Installation instructions: what manufacturer’s drivers should be installed to make it run?

    Attributes:
    -----------
    controller: object
        The particular object that allow the communication with the hardware, in general a python wrapper around the
         hardware library.
         
    # TODO add your particular attributes here if any

    """
    is_multiaxes = False  # TODO for your plugin set to True if this plugin is controlled for a multiaxis controller
    _axis_names: Union[List[str], Dict[str, int]] = ['Axis1', 'Axis2']  # TODO for your plugin: complete the list
    _controller_units: Union[str, List[str]] = 'mm'  # TODO for your plugin: put the correct unit here, it could be
    # TODO  a single str (the same one is applied to all axes) or a list of str (as much as the number of axes)
    _epsilon: Union[float, List[float]] = 0.01  # TODO replace this by a value that is correct depending on your controller
    # TODO it could be a single float of a list of float (as much as the number of axes)
    data_actuator_type = DataActuatorType.DataActuator  # wether you use the new data style for actuator otherwise set this
    # as  DataActuatorType.float  (or entirely remove the line)

    params = [ {'title': 'SN :', 'name': 'SN', 'type': 'str', 'value': '112563390', 'default': '112563390', 'readonly' : False},
               {'title': 'Speed :', 'name': 'Speed', 'type': 'int', 'value': 5000000, 'default': 5000000,
                'readonly': False, 'suffix':'nm/s'},
               {'title': 'Acceleration :', 'name': 'Acc', 'type': 'int', 'value': 10000000, 'default': 10000000,
'readonly': False, 'suffix': 'nm/s2'},

                ] + comon_parameters_fun(is_multiaxes, axis_names=_axis_names, epsilon=_epsilon)
    # _epsilon is the initial default value for the epsilon parameter allowing pymodaq to know if the controller reached
    # the target value. It is the developer responsibility to put here a meaningful value

    def ini_attributes(self):
        #  TODO declare the type of the wrapper (and assign it to self.controller) you're going to use for easy
        #  autocompletion

        #TODO declare here attributes you want/need to init with a default value
        pass

    def get_actuator_value(self) -> DataActuator:
        """Get the current value from the hardware with scaling conversion.

        Returns
        -------
        float: The position obtained after scaling conversion.
        """

        pos = DataActuator(data=self.controller.GetCurrentPosition()/1e6,  # when writing your own plugin replace this line
                           units=self.axis_unit)
        pos = self.get_position_with_scaling(pos)
        return pos

    def user_condition_to_reach_target(self) -> bool:
        """ Implement a condition for exiting the polling mechanism and specifying that the
        target value has been reached

       Returns
        -------
        bool: if True, PyMoDAQ considers the target value has been reached
        """
        # TODO either delete this method if the usual polling is fine with you, but if need you can
        #  add here some other condition to be fullfilled either a completely new one or
        #  using or/and operations between the epsilon_bool and some other custom booleans
        #  for a usage example see DAQ_Move_brushlessMotor from the Thorlabs plugin
        return True

    def close(self):
        """Terminate the communication protocol"""

        if self.is_master:
            self.controller.StopPolling()
            self.controller.Disconnect(True)


    def commit_settings(self, param: Parameter):
        """Apply the consequences of a change of value in the detector settings

        Parameters
        ----------
        param: Parameter
            A given parameter (within detector_settings) whose value has been changed by the user
        """

        if param.name() == 'Speed':
            closedLoopParams = self.controller.GetClosedLoopParameters()
            closedLoopParams.RefSpeed = self.settings.child('Speed').value()

            if param.name() == 'Acc':
                closedLoopParams = self.controller.GetClosedLoopParameters()
                closedLoopParams.RefSpeed = self.settings.child('Acc').value()


        elif param.name() == "a_parameter_you've_added_in_self.params":
           self.controller.your_method_to_apply_this_param_change()
        else:
            pass

    def ini_stage(self, controller=None):
        """Actuator communication initialization

        Parameters
        ----------
        controller: (object)
            custom object of a PyMoDAQ plugin (Slave case). None if only one actuator by controller (Master case)

        Returns
        -------
        info: str
        initialized: bool
            False if initialization failed otherwise True
        """
        DeviceManagerCLI.BuildDeviceList()
        # create new device
        serial_no = self.settings.child('SN').value() #str("112563390")  # Replace this line with your device's serial number
        device = InertiaStageController.CreateInertiaStageController(serial_no)

        # Connect, begin polling, and enable
        device.Connect(serial_no)
        time.sleep(0.25)
        device.StartPolling(250)  # 250ms polling rate
        time.sleep(0.25)  # wait statements are important to allow settings to be sent to the device

        device.EnableDevice()
        time.sleep(0.25)  # Wait for device to enable

        # Get Device information
        deviceInfo = device.GetDeviceInfo()
        print(deviceInfo.Description)
        device.SetPositionControlMode(PiezoControlModeTypes.CloseLoop)
        print("Connected in closed loop mode")

        # Wait for Settings to Initialise
        if not device.IsSettingsInitialized():
            device.WaitForSettingsInitialized(10000)  # 10 second timeout
            assert device.IsSettingsInitialized() is True

        # Get Device Configuration
        pdxc2Configuration = device.GetPDXC2Configuration(serial_no,
                                                          DeviceConfiguration.DeviceSettingsUseOptionType.UseDeviceSettings)
        # Not used directly in example but illustrates how to obtain device settings
        currentDeviceSettings = PDXC2Settings.GetSettings(pdxc2Configuration)

        if self.is_master:  # is needed when controller is master
            self.controller = device#  arguments for instantiation!)
            initialized = True  # todo
            # todo: enter here whatever is needed for your controller initialization and eventual
            #  opening of the communication channel
        else:
            self.controller = controller
            initialized = True

        info = "Whatever info you want to log"
        return info, initialized

    def move_abs(self, value: DataActuator):
        """ Move the actuator to the absolute target defined by value

        Parameters
        ----------
        value: (float) value of the absolute target positioning
        """

        value = self.check_bound(value)  #if user checked bounds, the defined bounds are applied here
        self.target_value = value
        value = self.set_position_with_scaling(value)  # apply scaling if the user specified one

        ## TODO for your custom plugin
        self.controller.SetClosedLoopTarget(int(value.value()*1e6))

        # Get and Set the velocity and acceleration
        # For linear stages, the unit is in nm/s and nm/s^2
        # For rotational stages, 360 degrees corresponds to 14400000 EnCnt. For example, 30 degrees/s = 1200000 EnCnt/s
        closedLoopParams = self.controller.GetClosedLoopParameters()
        closedLoopParams.RefSpeed = self.settings.child('Speed').value()
        closedLoopParams.Acceleration = self.settings.child('Acc').value()
        self.controller.SetClosedLoopParameters(closedLoopParams)

        # Move the stage
        self.controller.MoveStart()
        print("Moving the device to ", value.value())


        self.emit_status(ThreadCommand('Update_Status', [f'Moved PDXC2 absolute to {value}']))

    def move_rel(self, value: DataActuator):
        """ Move the actuator to the relative target actuator value defined by value

        Parameters
        ----------
        value: (float) value of the relative target positioning
        """
        print("move rel")
        value = self.check_bound(self.current_position + value) - self.current_position
        self.target_value = value + self.current_position
        value = self.set_position_relative_with_scaling(value)

        self.move_abs(self.target_value)  # when writing your own plugin replace this line
        self.emit_status(ThreadCommand('Update_Status', [f'Moved PDXC2 relative by {value}']))

    def move_home(self):
        """Call the reference method of the controller"""


        self.controller.Home(60000)  # 60 second timeout
        print("Homed the device")

        self.emit_status(ThreadCommand('Update_Status', ['Some info you want to log']))

    def stop_motion(self):
        """Stop the actuator and emits move_done signal"""

        ## TODO for your custom plugin
        raise NotImplementedError  # when writing your own plugin remove this line
        self.controller.your_method_to_stop_positioning()  # when writing your own plugin replace this line
        self.emit_status(ThreadCommand('Update_Status', ['Some info you want to log']))


if __name__ == '__main__':
    main(__file__)
