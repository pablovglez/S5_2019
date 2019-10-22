 * Download last version (9.1.0) of code composer studio [here](http://software-dl.ti.com/ccs/esd/documents/ccs_downloads.html#code-composer-studio-version-9-downloads)
 * Extract it in a tmp directory
 * Install required packages (for me: `sudo apt install libncurses5 libtinfo5`)
 * Go to the extracted directory and run the installation binary (`sudo apt install libncurses5 libtinfo5`)
   * Select appropriate target (`C26xx`)
 * install the driver
   * `cd ~/ti/ccs910/ccs/install_scripts`
   * `sudo ./install_drivers.sh`

* Install the CC2640R2 SDK
 * Download the SDK at: https://www.ti.com/tool/download/SIMPLELINK-CC2640R2-SDK
 * Run the donwloaded installer:
   * `chmod +x  ./simplelink_cc2640r2_sdk_3_20_00_21.run`
   * `./simplelink_cc2640r2_sdk_3_20_00_21.run` 

* A popup says that updates are avalable do what it asks...
 
  
* Don''t forget to allow local user to access tty: `sudo usermod -a -G dialout $USER`


* Yes, but transfer fails :-(
  * OK, for some reasons, it is needed to decrease the JTAG operating frequency
  * See [here](https://e2e.ti.com/support/tools/ccs/f/81/t/831761?tisearch=e2e-sitesearch&keymatch=CC2640R2%20linux%20can%27t%20flash) and [here](https://e2e.ti.com/support/tools/ccs/f/81/t/831675) and documentation [here](http://software-dl.ti.com/ccs/esd/documents/users_guide/ccs_debug-main.html#advanced-target-configuration-options)
  * in short:
    * from the file explorer, open the .ccxml file (eg. `targetConfigs/CC2640R2F`)
    * go to advanced tab (bottom left)
    * on the top item (XDS110 USB Debug Probe), adjust the JTAG TCLK frequency (worked for me with 2.5MHz ('Fixed with user specified value'))
  
 
 
* In which order shoul I follow the tutos??? 
 * start with [Project Zero](http://dev.ti.com/tirex/explore/node?node=AJ7jWuST9RweXKhWHqlyWg__FUz-xrs__LATEST)
 * Then [RTLS Introduction](http://dev.ti.com/tirex/explore/content/simplelink_academy_cc2640r2sdk_3_20_03_00/modules/rtls_toolbox_ble3/rtls_intro/rtls_intro.html)
 * Then [Time of Flight (ToF)](http://dev.ti.com/tirex/explore/content/simplelink_academy_cc2640r2sdk_3_20_03_00/modules/rtls_toolbox_ble3/rtls_tof/rtls_tof.html)
 
 
* Notes about versions:
 * RTLS demo has been proved to work with the folowing version of software:
 * CCS version 9.1.0.00010
 * simplelink cc2640r2 sdk 3.20.00.21
 * RTLS Monitor (online supervision Tool for ToF/AoA demo) version 0.9.4 [here](https://dev.ti.com/gallery/view/LPRF/RTLS_Monitor/ver/0.9.4/)
