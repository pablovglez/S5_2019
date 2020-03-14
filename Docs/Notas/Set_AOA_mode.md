### ##########   TO ACTIVATE AOA ########## ###

# Reminder
 * For the case of our cards :
 * Passive <L5000IZO>
 * Master  <L5000J02>
 * Slave   <L5000IZP>

### This is a tutorial to activate AOA in Code Composer Studio using LAUNCH CC2640R2 cards ###

In the master and slave : right click on the *_app project and then in properties
 * In <Build/XDCtools> Make sure the XDC TOOL is 3.20.0.21 

In the master and slave : double click on the *.ccxml file <app project/targetConfigs/CC2640R2F.ccxm>
  - Decrease the JTAG operating frequency to 2.5 MHz	DECREASE THE JTAG OPERATING FREQUENCY TO 2.5 MHz

In the master and slave : go to TOOLS folder <app project/TOOLS>
 * Double click on <build_config.opt>
 * Go to the end of the file and uncomment the line defining : <RTLS_LOCATIONING_AOA>
 * Save and flash

In the passive : right click on the *_app project and then in properties
 * In <Build/XDCtools> Make sure the XDC TOOL is 3.20.0.21

Double click on the *.ccxml file <app project/targetConfigs/CC2640R2F.ccxm>
 * Decrease the JTAG operating frequency to 2.5 MHz

Go to project properties (Right click) 
 * <app project/CCS Build/ARM Compiler/Predefined Symbols>
 * Clic add and type <RTLS_LOCATIONING_AOA>
 * Apply and close
 * Save and flash

### AOA Format (RTLS) ###
 * {"originator": "Nwp", "type": "AsyncReq", "subsystem": "RTLS", "command": "RTLS_CMD_AOA_RESULT_ANGLE", "payload": {"angle": -59, "rssi": -47, "antenna": 2, "channel": 22}}

### AOA Format (our codes) ###

 * "payload": {"angle": -19, "rssi": -66, "antenna": 2, "channel": 26, "time": 1581951429.8088975, "distance": "4", "position": "-15"}
