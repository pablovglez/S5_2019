### ##########   TO ACTIVATE AOA ########## ###

#This is a tutorial to activate AOA in Code Composer Studio using LAUNCH CC2640R2 cards

In the master and slave : right click on the *_app project and then in properties
  * In <Build/XDCtools> Make sure the XDC TOOL is 3.20.0.21 

In the master and slave : double click on the *.ccxml file <app project/targetConfigs/CC2640R2F.ccxm>
  - Decrease the JTAG operating frequency to 2.5 MHz	DECREASE THE JTAG OPERATING FREQUENCY TO 2.5 MHz

In the master and slave : go to TOOLS folder <app project/TOOLS>
 * Double click on <build_config.opt>
 * GO TO THE END OF THE FILE AND UNCOMMENT THE LINE DEFINING RTLS_LOCATIONING_AOA
#	SAVE AND FLASH
#	
#	
#	
# 
#	
#	L5000IZP  -  Slave
#	L5000IZO  -  Passive
#	L5000J02  -  Master



# IN THE PASIVE:
#	MAKE SURE THE XDC TOOL IS 3.20.0.21
#	DECREASE THE JTAG OPERATING FREQUENCY TO 2.5 MHz
#	GO TO PROJECT PROPERTIES (RIGHT CLICK)
#	SELECT: BUILD ->  ARM COMPILER ->  PREDEFINED SYMBOLS
#	CLICK ADD AND TYPE RTLS_LOCATIONING_AOA
#	APPLY AND CLOSE
#	SAVE AND FLASH
#	
#	

##### AOA FORMAT
#	{"originator": "Nwp", "type": "AsyncReq", "subsystem": "RTLS", "command": "RTLS_CMD_AOA_RESULT_ANGLE", "payload": {"angle": -59, "rssi": -47, "antenna": 2, "channel": 22}}
#	
#	
#	
#	
#	



#A FAIRE: - 15 O 10 GRADOS, BOXPLOT, MOSTRAR SI LA TARJETA NOS DICE DE QUÉ LADO ESTÁ

