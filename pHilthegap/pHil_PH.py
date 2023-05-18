'''
@file pHil_PH.py
Copy of the original DFrobot_PH.py from DFRobot
@author Karl Hallström (karlhal@chalmers.se)
@version  1.0
@date  2023-05-18
@copyright Copyright (c) 2023 pHil The Gap - Chalmers tekniska högskola (philthegap2023.com)
@license Creative Commons Attribution 4.0 International (CC BY 4.0)
This software is released under the Creative Commons Attribution 4.0 International license.
You are free to copy, redistribute and adapt the material for any purpose, even commercially, under the>Attribution — You must give appropriate credit to the original author (DFRobot), provide a link to the >and indicate if changes were made. You may do so in any reasonable manner, but not in any way that sugg>the licensor endorses you or your use. For more details visit:
https://creativecommons.org/licenses/by/4.0/

The original code from which this code is derived is under The MIT License (MIT)
@author [Jiawei Zhang](jiawei.zhang@dfrobot.com)
@copyright Copyright (c) 2010 DFRobot Co.Ltd (http://www.dfrobot.com)
'''

import time
import sys

_temperature      = 25.0
_acidVoltage      = 2032.44
_neutralVoltage   = 1500.0

class pHil_PH():
    def begin(self):
        global _acidVoltage
        global _neutralVoltage
        try:
            with open('phdata.txt','r') as f:
                neutralVoltageLine = f.readline()
                neutralVoltageLine = neutralVoltageLine.strip('neutralVoltage=')
                _neutralVoltage    = float(neutralVoltageLine)
                acidVoltageLine    = f.readline()
                acidVoltageLine    = acidVoltageLine.strip('acidVoltage=')
                _acidVoltage       = float(acidVoltageLine)
        except:
            print("phdata.txt ERROR ! Please run DFRobot_PH_Reset")
            sys.exit(1)

    def read_PH(self, voltage, temperature):
        global _acidVoltage
        global _neutralVoltage
        slope = (7.0 - 4.0) / ((_neutralVoltage - 1500.0) / 3.0 - (_acidVoltage - 1500.0) / 3.0)
        intercept = 7.0 - slope * (_neutralVoltage - 1500.0) / 3.0
        _phValue = slope * (voltage - 1500.0) / 3.0 + intercept
        round(_phValue, 2)
        return _phValue

    def calibration(self, voltage):
        if (voltage > 1322 and voltage < 1678):
            print(">>>Buffer Solution:7.0")
            with open('phdata.txt', 'r+') as f:
                flist = f.readlines()
            flist[0] = 'neutralVoltage=' + str(voltage) + '\n'
            with open('phdata.txt', 'w+') as f:
                f.writelines(flist)
            print(">>>PH:7.0 Calibration completed,Please enter Ctrl+C exit calibration in 5 seconds")
            time.sleep(5.0)
        elif (voltage > 1854 and voltage < 2210):
            print(">>>Buffer Solution:4.0")
            with open('phdata.txt', 'r+') as f:
                flist = f.readlines()
            flist[1] = 'acidVoltage=' + str(voltage) + '\n'
            with open('phdata.txt', 'w+') as f:
                f.writelines(flist)
            print(">>>PH:4.0 Calibration completed,Please enter Ctrl+C exit calibration in 5 seconds")
            time.sleep(5.0)
        else:
            print(">>>Buffer Solution Error Try Again<<<")

    def reset(self):
        global _acidVoltage
        global _neutralVoltage
        _acidVoltage = 2032.44
        _neutralVoltage = 1500.0
        try:
            with open('phdata.txt', 'r+') as f:
                flist = f.readlines()
            flist[0] = 'neutralVoltage=' + str(_neutralVoltage) + '\n'
            flist[1] = 'acidVoltage=' + str(_acidVoltage) + '\n'
            with open('phdata.txt', 'w+') as f:
                f.writelines(flist)
            print(">>>Reset to default parameters<<<")
        except:
            with open('phdata.txt', 'w') as f:
                flist = 'neutralVoltage=' + str(_neutralVoltage) + '\n'
                flist += 'acidVoltage=' + str(_acidVoltage) + '\n'
                # f=open('data.txt','w+')
                f.writelines(flist)
                f.close()
                print(">>>Reset to default parameters<<<")
 
