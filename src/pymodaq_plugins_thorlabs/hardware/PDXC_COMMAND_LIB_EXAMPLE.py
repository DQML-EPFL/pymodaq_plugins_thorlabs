try:
    from PDXC_COMMAND_LIB import pdxc
    import time
except OSError as ex:
    print("Warning:", ex)


# ------------ Example PDXC Joy Stick Params -------------- #
def joy_stick_params(pdxcobj):
    print("*** PDXC Joy Stick params setting example")
    value = [0]
    result = pdxcobj.GetJoystickConfig(0, value)
    if result < 0:
        print("pdxc Get Joystick Config failed")
    else:
        print("The JoyStick Config value is: ", value)


# ------------ Example PDXC D_Sub-PDX1/PDX2/PDX3/PDX4/PDXR/PDXZ1/PDX1A/PDX1AV/PDX1D/PDX1D/PDXG1 Stage -------------- #
def d_sub_pdx_stage(pdxcobj):
    print("*** PDXC PDX1/PDX2/PDX3/PDX4/PDXR/PDXZ1/PDX1A/PDX1AV/PDX1D/PDX1D/PDXG1 Stage example ***")

    # closed loop #
    print("*  closed loop mode  *")
    result = pdxcobj.SetLoop(0, 0)
    if result < 0:
        print("set loop to closed loop failed", result)
    else:
        print("set loop to closed loop")

    print("**  Manual Mode  **")
    result = pdxcobj.SetCurrentStatusInExternalTrigger(0, "AR/AF")
    if result < 0:
        print("set trigger mode to manual mode failed", result)
    else:
        print("set trigger mode to manual mode")

    homed = [0]
    result = pdxcobj.GetCalibrationIsCompleted(0, homed)
    if result < 0:
        print("get CalibrationIsCompleted failed", result)
    else:
        print("get CalibrationIsCompleted: ", homed[0])

    homed_value = 1 if str(homed[0]).find('Yes') != -1 else 0
    if homed_value == 0:
        result = pdxcobj.SetPositionCalibration(0, 1)  # Under closed loop,stage must be homed before move and jog
        if result < 0:
            print("set PositionCalibration home failed", result)
        else:
            print("set PositionCalibration home")

        homed_status = 0
        while homed_status == 0:
            homed_value = [0]
            pdxcobj.GetCalibrationIsCompleted(0, homed_value)
            homed_status = 1 if str(homed_value[0]).find('Yes') != -1 else 0
        print("Home is done!")

    sn2 = [0]
    pdxcobj.GetSN2(0, sn2)
    if 'PDXZ1' in str(sn2):
        pass
    else:
        result = pdxcobj.SetTargetSpeed(0, 10)
        if result < 0:
            print("set TargetSpeed to 10 failed", result)
        else:
            print("set TargetSpeed to 10")

    result = pdxcobj.SetTargetPosition(0, 2)
    if result < 0:
        print("set TargetPosition to 2 failed", result)
    else:
        print("set TargetPosition to 2 ")
    time.sleep(5)

    position = [0]
    result = pdxcobj.GetCurrentPosition(0, position)
    if result < 0:
        print("get CurrentPosition failed", result)
    else:
        print("get CurrentPosition: ", position)

    result = pdxcobj.SetStepPulseAndResponse(0, 1)
    if result < 0:
        print("Jog failed", result)
    else:
        print("Jog success ")

        # ------  Trigger Mode Example  ------#
    print("**  Trigger Mode Example  **")
    # Analog In #
    result = pdxcobj.SetCurrentStatusInExternalTrigger(0, "AR")  # AR: set Analog In mode with Rising edge; AF: set
    # Analog In mode with Falling edge
    if result < 0:
        print("set trigger mode to Analog In mode failed", result)
    else:
        print("set trigger mode to Analog In mode")

    result = pdxcobj.SetAnalogInputGain(0, 0.5)
    if result < 0:
        print("set AnalogInputGain to 6 failed", result)
    else:
        print("set AnalogInputGain to 0.5")

    aigain = [0]
    result = pdxcobj.GetAnalogInputGain(0, aigain)
    if result < 0:
        print("get AnalogInputGain failed", result)
    else:
        print("get AnalogInputGain: ", aigain)

    result = pdxcobj.SetAnalogInputOffSet(0, 1.0)
    if result < 0:
        print("set AnalogInputOffSet to 1.0 failed", result)
    else:
        print("set AnalogInputOffSet to 1.0")

    aioffset = [0]
    result = pdxcobj.GetAnalogInputOffSet(0, aioffset)
    if result < 0:
        print("get AnalogInputOffset failed", result)
    else:
        print("get AnalogInputOffset: ", aioffset)

        # Fixed Step size #
    result = pdxcobj.SetCurrentStatusInExternalTrigger(0, "FR[8]")  # FR[8]: set Fixed step size to 8 with Rising
    # edge; FF[8]: set Fixed step size to 8 with Falling edge
    if result < 0:
        print("set trigger mode to Fixed Step size mode failed", result)
    else:
        print("set trigger mode to Fixed Step size mode")

        # Fixed Position #
    result = pdxcobj.SetCurrentStatusInExternalTrigger(0, "PR[-5], PF[5]")  # "PR[-5]: set Fixed Position to -smm
    # with Rising edge; PF[5]: set Fixed Position to 5mm with Falling edge
    if result < 0:
        print("set trigger mode to Fixed Position mode failed", result)
    else:
        print("set trigger mode to Fixed Position mode")


# ------------ Example PDXC SMC Stage -------------- #
def smc_stage(pdxcobj):
    print("*** PDXC SMC stage example")

    result = pdxcobj.SetOpenLoopFrequency(0, 800)  # set/get frequency/Jogsize of open loop for channel 1
    if result < 0:
        print("set OpenLoopFrequency failed", result)
    else:
        print("set OpenLoopFrequency 800Hz ")

    fry = [0]
    result = pdxcobj.GetOpenLoopFrequency(0, fry)
    if result < 0:
        print("get OpenLoopFrequency failed", result)
    else:
        print("get OpenLoopFrequency: ", fry)

    result = pdxcobj.SetOpenLoopJogSize(0, 900)
    if result < 0:
        print("set OpenLoopJogSize failed", result)
    else:
        print("set OpenLoopJogSize 900 ")

    result = pdxcobj.SetOpenLoopFrequency2(0, 1000)  # set/get frequency/Jogsize of open loop for channel 2
    if result < 0:
        print("set OpenLoopFrequency2 failed", result)
    else:
        print("set OpenLoopFrequency2 1000Hz ")

    result = pdxcobj.SetOpenLoopJogSize2(0, 1100)
    if result < 0:
        print("set OpenLoopJogSize2 failed", result)
    else:
        print("set OpenLoopJogSize2 1100 ")

    result = pdxcobj.SetOpenLoopMoveForward(0, 150, 0)  # moveback and move forward in open loop mode of channel 1;
    # SMC[1,65535]; PD2/PD3[1,400000]
    if result < 0:
        print("set OpenLoopMoveForward 150 failed", result)
    else:
        print("set OpenLoopMoveForward 150")
    time.sleep(1)

    result = pdxcobj.SetOpenLoopMoveBack(0, 150, 0)  # SMC[1,65535]; PD2/PD3[1,400000]
    if result < 0:
        print("set OpenLoopMoveBack 150 failed", result)
    else:
        print("set OpenLoopMoveBack 150")
    time.sleep(1)


# ------------ Example PDXC D_Sub-PD2/PD3 Stage -------------- #
def d_sub_pd_stage(pdxcobj):
    print("*** PDXC PD2/PD3 stage example")

    result = pdxcobj.SetOpenLoopFrequency3(0, 800)  # set/get frequency/Jogsize of open loop for PD2
    if result < 0:
        print("set OpenLoopFrequency3 failed", result)
    else:
        print("set OpenLoopFrequency3 800Hz ")

    fry3 = [0]
    result = pdxcobj.GetOpenLoopFrequency3(0, fry3)
    if result < 0:
        print("get OpenLoopFrequency failed", result)
    else:
        print("get OpenLoopFrequency: ", fry3)

    result = pdxcobj.SetOpenLoopJogSize3(0, 900)
    if result < 0:
        print("set OpenLoopJogSize3 failed", result)
    else:
        print("set OpenLoopJogSize3 900 ")

    result = pdxcobj.SetOpenLoopMoveForward(0, 150, 0)  # moveback and move forward in open loop mode of PD2
    # SMC[1,65535]; PD2/PD3[1,400000]
    if result < 0:
        print("set OpenLoopMoveForward 150 failed", result)
    else:
        print("set OpenLoopMoveForward 150")
    time.sleep(1)

    result = pdxcobj.SetOpenLoopMoveBack(0, 150, 0)  # SMC[1,65535]; PD2/PD3[1,400000]
    if result < 0:
        print("set OpenLoopMoveBack 150 failed", result)
    else:
        print("set OpenLoopMoveBack 150")
    time.sleep(1)


def main():
    print("*** pdxc device python example ***")
    pdxcobj = pdxc()
    try:
        devs = pdxc.ListDevices()
        print(devs)
        if len(devs) <= 0:
            print('There is no devices connected')
            exit()
        device_info = devs[0]
        sn = device_info[0]
        print("connect ", sn)
        hdl = pdxcobj.Open(sn, 115200, 3)
        if hdl < 0:
            print("open ", sn, " failed")
            exit()
        if pdxcobj.IsOpen(sn) == 0:
            print("pdxcIsOpen failed")
            pdxcobj.Close()
            exit()

        result = pdxcobj.SetDaisyChain(0)  # 0:Single Mode, 1:Main, 2 -12 : Secondary1 - Secondary11
        if result < 0:
            print("set daisy chain mode failed", result)
        else:
            print("set daisy chain mode: single mode")

        num = [0]
        if pdxcobj.GetJoystickStatus(0, num) < 0:
            print("pdxc Get Joystick Status failed")
        else:
            print("The number of knob on joystick is : ", num)
            if num[0] > 0:
                joy_stick_params(pdxcobj)
            else:
                print("No joystick is connected to this device.")

        ty = [0]
        if pdxcobj.GetSpeedStageType(0, ty) < 0:
            print("pdxcGetSpeedStageType failed")
        else:
            sn2 = [0]
            pdxcobj.GetSN2(0, sn2)
            if ty[0] == 0:
                if 'PDXR' in str(sn2):
                    print("Found PDXR stage")
                elif "PDX1AV" in str(sn2):
                    print("Found PDX1AV stage")
                elif "PDX1A" in str(sn2):
                    print("Found PDX1A stage")
                elif "PDX1" in str(sn2):
                    print("Found PDX1 stage")
                elif "PDX2" in str(sn2):
                    print("Found PDX2 stage")
                elif "PDX3" in str(sn2):
                    print("Found PDX3 stage")
                elif "PDX4" in str(sn2):
                    print("Found PDX4 stage")
                elif "PDX1DV" in str(sn2):
                    print("Found PDX1DV stage")
                elif "PDX1D" in str(sn2):
                    print("Found PDX1D stage")
                elif "PDXG1" in str(sn2):
                    print("Found PDXG1 stage")
                else:
                    print("Found PDXZ1 stage")
                d_sub_pdx_stage(pdxcobj)
            elif ty[0] == 1:
                smc_stage(pdxcobj)
            elif ty[0] == 2:
                if 'PD2' in str(sn2):
                    print('Found PD2 stage')
                else:
                    print('Found PD3 stage')
                d_sub_pd_stage(pdxcobj)
            else:
                print("Unkown stage type!")

        pdxcobj.Close()

    except Exception as e:
        print("Warning:", e)
    print("*** End ***")
    input()


main()
