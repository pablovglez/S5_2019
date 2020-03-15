### ########## THIS TUTORIAL EXPLAINS HOW TO INSTALL SIMPLELINK-CC2640R2-SDK/3.20.00.21 ON UBUNTU 18.04 AND ABOVE ########## ###

* Go to <http://www.ti.com/tool/download/SIMPLELINK-CC2640R2-SDK/3.20.00.21>
* Download Linux Installer

* Go to download folder in terminal and type:

* Give permissions to file typing in terminal 
  - chmod +x simplelink_cc2640r2_sdk_3_20_00_21.run

* Run in terminal 
  - simplelink_cc2640r2_sdk_3_20_00_21.run

* Look for the rtls_monitor tool located in [ti --> simplelink_cc2640r2_sdk_3_20_00_21 --> tools --> blestack --> rtls_agent]

* Give permissions to file typing in terminal 
  - chmod +x requirements.txt
  
* Install the requirements in the *.txt file
  - pip3 install -r requirements.txt
   - If error with windows-curses [windows-curses is not necessary on Python 3.7] comment such line

* Install virtualenv typing 
  * sudo pip3 install virtualenv 

* Execute virtualenv typing
  - virtualenv -p python3 .venv 
   - or python3 -m venv .venv

* Activate virtualenv typing 
  - . .venv/bin/activate 
   - or source .venv/bin/activate   which does exactly the same thing

* Give permissions to file typing in terminal 
  - chmod +x rtls_agent_cli


* Now you can run the RTLS Agent
  - python3 agent/rtls_agent_cli.py


### ########## TO RUN AGAIN THE VIRTUAL ENVIRONMENT ########## ###
### FOR THE FOLLOWING USES ###

* Execute virtualenv typing
  - virtualenv -p python3 .venv 
   - or python3 -m venv .venv

* Activate virtualenv typing 
  - . .venv/bin/activate 
   - or source .venv/bin/activate   which does exactly the same thing

* Go to </ti/simplelink_cc2640r2_sdk_3_20_00_21/tools/blestack/rtls_agent> directory 
  - cd /home/efisio/ti/simplelink_cc2640r2_sdk_3_20_00_21/tools/blestack/rtls_agent
  - cd /home/vinicio/ti/simplelink_cc2640r2_sdk_3_20_00_21/tools/blestack/rtls_agent

* To get the ports where the cards are connected
* Run typing
  - python3 agent/rtls_agent_cli.py



### TO RUN THE AOA CLIENT ###

* Go to /ti/simplelink_cc2640r2_sdk_3_20_00_21/tools/blestack/rtls_agent directory 
 - /home/efisio/ti/simplelink_cc2640r2_sdk_3_20_00_21/tools/blestack/rtls_agent/examples
 - /home/vinicio/ti/simplelink_cc2640r2_sdk_3_20_00_21/tools/blestack/rtls_agent/examples

### ########## TO INSTALL SDK 3.40.00.10 ########## ###
### ATTENTION : Installing SDK 3.40 will make impossible to use the code rtls_AoA developped for SDK 3.20 ###

* Go to <http://www.ti.com/tool/download/SIMPLELINK-CC2640R2-SDK/3.40.00.10>
* Download Linux Installer

* Go to download folder in terminal and type:

* Give permissions to file typing in terminal 
  - chmod +x simplelink_cc2640r2_sdk_3_40_00_10.run

* Run in terminal 
  - Type in terminal 
   - ./simplelink_cc2640r2_sdk_3_40_00_10.run

* Go to </ti/simplelink_cc2640r2_sdk_3_40_00_21/tools/blestack/rtls_agent> directory 

* Give permissions to file typing in terminal 
  - chmod +x package.sh

* File package.sh has been created as a script for Windows env and then ported over to run on a Unix environment so we need to type:
  - sed -i -e 's/\r$//' package.sh 

* Run de package file
  - ./package.sh -c -b -u -i 

* Go to <ti/simplelink_cc2640r2_sdk_3_40_00_10/tools/blestack/rtls_agent/rtls_ui> directory
  - cd ti/simplelink_cc2640r2_sdk_3_40_00_10/tools/blestack/rtls_agent/rtls_ui

* Give permissions to file typing in terminal 
  - chmod +x rtls_ui

* Run the RTLS Graphic Interface
  - ./rtls_ui
