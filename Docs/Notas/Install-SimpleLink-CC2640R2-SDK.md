#Go to http://www.ti.com/tool/download/SIMPLELINK-CC2640R2-SDK/3.20.00.21

#Download Linux Installer

# Go to download folder in terminal and type:

#Give permissions to file typing in terminal 
chmod +x simplelink_cc2640r2_sdk_3_20_00_21.run

#Type in terminal 
-/simplelink_cc2640r2_sdk_3_20_00_21.run

#Look for the rtls_monitor tool located in [ti --> simplelink_cc2640r2_sdk_3_20_00_21 --> tools --> blestack --> rtls_agent]

#Give permissions to file typing in terminal 
chmod +x requirements.txt

#Install virtualenv typing 
sudo pip3 install virtualenv 

virtualenv -p python3 .venv 
#or python3 -m venv .venv

. .venv/bin/activate 
# or source .venv/bin/activate which does exactly the same thing

#Give permissions to file typing in terminal 
chmod +x rtls_agent_cli

#Make sure all pre-requisites are fulfilled by typing: 
#Tkinker must be included on the list
pip3 install -r requirements.txt 

#If error with windows-curses [windows-curses is not necessary on Python 3.7] comment such line

#### NOW YOU CAN RUN THE RTLS AGENT

python3 agent/rtls_agent_cli.py

########## TO RUN AGAIN THE VIRTUAL ENVIRONMENT ####


### FOR THE FOLLOWING USES, START FROM  LINE 17 ###

virtualenv -p python3 .venv
#or python3 -m venv .venv

. .venv/bin/activate 
# or source .venv/bin/activate which does exactly the same thing

cd /home/efisio/ti/simplelink_cc2640r2_sdk_3_20_00_21/tools/blestack/rtls_agent

cd /home/vinicio/ti/simplelink_cc2640r2_sdk_3_20_00_21/tools/blestack/rtls_agent

chmod +x rtls_agent_cli

pip3 install -r requirements.txt

python3 agent/rtls_agent_cli.py

### TO RUN THE AOA CLIENT ###

cd /home/efisio/ti/simplelink_cc2640r2_sdk_3_20_00_21/tools/blestack/rtls_agent/examples

cd /home/vinicio/ti/simplelink_cc2640r2_sdk_3_20_00_21/tools/blestack/rtls_agent/examples

python3 tst_efisio.py


####
###### TO INSTALL SDK 3.40.00.10
####

#Go to http://www.ti.com/tool/download/SIMPLELINK-CC2640R2-SDK/3.40.00.10

# Go to download folder in terminal and type:

#Give permissions to file typing in terminal 
chmod +x simplelink_cc2640r2_sdk_3_40_00_10.run

#Type in terminal 
./simplelink_cc2640r2_sdk_3_40_00_10.run

# Installing Python3.7
#Setup external packages in case you network is behind a proxy use [--proxy]

#Go to <rtls_agent folder>
cd ti/simplelink_cc2640r2_sdk_3_40_00_10/tools/blestack/rtls_agent

#Give permissions to file typing in terminal 
chmod +x package.sh

#Package has been created as a script for Windows env and then ported over to run on a Unix environment so we need to type:

sed -i -e 's/\r$//' package.sh 

#Run de package file
histoy./package.sh -c -b -u -i 

#Go to <rtls_ui folder>

cd ti/simplelink_cc2640r2_sdk_3_40_00_10/tools/blestack/rtls_agent/rtls_ui

chmod +x rtls_ui
./rtls_ui
