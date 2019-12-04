#Navigate to the SDK folder (~\tools\blestack\rtls_agent)

#virtualenv -p python3 .venv or python3 -m venv .venv

#. .venv/bin/activate # or source .venv/bin/activate which does exactly the same thing

#Make sure all pre-requisites are fulfilled by typing: pip3 install -r requirements.dev.txt 

#Open the examples/rtls_example.py, go to line 44, and 
#edit the line my_nodes = [RTLSNode('COM17', 115200), RTLSNode('COM12', 115200)] 
#to use the COM ports of the master and passive LaunchPads.

#Note that you can get the port number using "agent/rtls_agent_cli.py
#Then, replace COM17 for MASTER (/dev/ttyACM0) and COM12 for PASSIVE ('/dev/ttyACM4')

#GO TO PATH /home/efisio/ti/simplelink_cc2640r2_sdk_3_20_00_21/tools/blestack/rtls_agent

#RUN rtls_example.py
#python3 -u examples/rtls_example.py

