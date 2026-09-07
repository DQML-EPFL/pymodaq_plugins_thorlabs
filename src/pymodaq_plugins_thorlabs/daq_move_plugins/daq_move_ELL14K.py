from pymodaq.control_modules.move_utility_classes import DAQ_Move_base, main, DataActuator, DataActuatorType, comon_parameters_fun
from pymodaq.utils.daq_utils import ThreadCommand
from thorlabs_elliptec import ELLx
import numpy as np

class DAQ_Move_ELL14K(DAQ_Move_base):
    is_multiaxes = False
    _controller_units = '°'
    _epsilon = 0.2
    data_actuator_type = DataActuatorType.DataActuator
    params = comon_parameters_fun(is_multiaxes, epsilon=_epsilon)

    def ini_attributes(self):
        self.controller: ELLx = None

    def ini_stage(self, controller=None):
        self.ini_stage_init(slave_controller=controller)
        if self.is_master:
            self.controller = ELLx("COM6")
            self.controller.home(blocking=True)
        return "ELL14K initialized", True

    def get_actuator_value(self):
        pos = self.controller.get_position()
        return DataActuator(data=pos)

    def move_abs(self, value: DataActuator):
        value = self.check_bound(value)
        self.target_value = value

        # Convert from GUI units (rad) → hardware units (deg)
        #hw_value_deg = np.deg2rad(value.value())
        hw_value_deg= value.value()
        print(hw_value_deg)
        self.controller.move_absolute(hw_value_deg, blocking=True)

        # Emit in GUI units
        self.move_done_signal.emit(value)
        self.emit_status(ThreadCommand('Update_Status', [f"Moved to {hw_value_deg:.2f} °"]))

    def move_rel(self, rel_value: DataActuator):
        current_deg = self.controller.get_position()
        print(current_deg)
        delta_deg = np.deg2rad(rel_value.value())  # Convert from GUI units → hardware
        print(delta_deg)
        target_deg = current_deg + delta_deg
        print(target_deg)
        # Convert from GUI units (rad) → hardware units (deg)
        hw_value_deg = target_deg
        self.controller.move_absolute(hw_value_deg, blocking=True)

        # Emit in GUI units
        self.move_done_signal.emit(DataActuator(hw_value_deg))
        self.emit_status(ThreadCommand('Update_Status', [f"Moved to {hw_value_deg:.2f} °"]))

        #target_actuator = DataActuator(np.rad2deg(target_deg)) # Emit in GUI units (rad)
        #self.move_abs(target_actuator)



    def stop_motion(self):
        self.emit_status(ThreadCommand('Update_Status', ['Stop requested (not supported)']))

    def close(self):
        self.controller.close()

if __name__ == '__main__':
    main(__file__)


