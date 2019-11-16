################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Each subdirectory must supply rules for building sources it contributes
ICallBLE/ble_user_config.obj: /home/vinicio/ti/simplelink_cc2640r2_sdk_3_30_00_20/source/ti/blestack/icall/app/ble_user_config.c $(GEN_OPTS) | $(GEN_FILES) $(GEN_MISC_FILES)
	@echo 'Building file: "$<"'
	@echo 'Invoking: ARM Compiler'
	"/home/vinicio/ti/ccs910/ccs/tools/compiler/ti-cgt-arm_18.12.2.LTS/bin/armcl" --cmd_file="/home/vinicio/ti/simplelink_cc2640r2_sdk_3_30_00_20/source/ti/blestack/config/build_components.opt" --cmd_file="/home/vinicio/ti/simplelink_cc2640r2_sdk_3_30_00_20/source/ti/blestack/config/factory_config.opt" --cmd_file="/home/vinicio/Documents/S5/S5_2019/CCS/host_test_cc2640r2lp_stack_library/TOOLS/build_config.opt"  -mv7M3 --code_state=16 -me -O4 --opt_for_speed=0 --include_path="/home/vinicio/Documents/S5/S5_2019/CCS/host_test_cc2640r2lp_app" --include_path="/home/vinicio/ti/simplelink_cc2640r2_sdk_3_30_00_20/source/ti/blestack/controller/cc26xx_r2/inc" --include_path="/home/vinicio/ti/simplelink_cc2640r2_sdk_3_30_00_20/source/ti/blestack/inc" --include_path="/home/vinicio/ti/simplelink_cc2640r2_sdk_3_30_00_20/source/ti/blestack/rom" --include_path="/home/vinicio/Documents/S5/S5_2019/CCS/host_test_cc2640r2lp_app/Application" --include_path="/home/vinicio/Documents/S5/S5_2019/CCS/host_test_cc2640r2lp_app/Startup" --include_path="/home/vinicio/Documents/S5/S5_2019/CCS/host_test_cc2640r2lp_app/PROFILES" --include_path="/home/vinicio/Documents/S5/S5_2019/CCS/host_test_cc2640r2lp_app/Include" --include_path="/home/vinicio/ti/simplelink_cc2640r2_sdk_3_30_00_20/source/ti/blestack/common/cc26xx" --include_path="/home/vinicio/ti/simplelink_cc2640r2_sdk_3_30_00_20/source/ti/blestack/icall/inc" --include_path="/home/vinicio/ti/simplelink_cc2640r2_sdk_3_30_00_20/source/ti/blestack/profiles/dev_info" --include_path="/home/vinicio/ti/simplelink_cc2640r2_sdk_3_30_00_20/source/ti/blestack/profiles/roles/cc26xx" --include_path="/home/vinicio/ti/simplelink_cc2640r2_sdk_3_30_00_20/source/ti/blestack/profiles/roles" --include_path="/home/vinicio/ti/simplelink_cc2640r2_sdk_3_30_00_20/source/ti/blestack/profiles/simple_profile/cc26xx" --include_path="/home/vinicio/ti/simplelink_cc2640r2_sdk_3_30_00_20/source/ti/blestack/profiles/simple_profile" --include_path="/home/vinicio/ti/simplelink_cc2640r2_sdk_3_30_00_20/source/ti/blestack/target" --include_path="/home/vinicio/ti/simplelink_cc2640r2_sdk_3_30_00_20/source/ti/blestack/hal/src/target/_common" --include_path="/home/vinicio/ti/simplelink_cc2640r2_sdk_3_30_00_20/source/ti/blestack/hal/src/target/_common/cc26xx" --include_path="/home/vinicio/ti/simplelink_cc2640r2_sdk_3_30_00_20/source/ti/blestack/hal/src/inc" --include_path="/home/vinicio/ti/simplelink_cc2640r2_sdk_3_30_00_20/source/ti/blestack/heapmgr" --include_path="/home/vinicio/ti/simplelink_cc2640r2_sdk_3_30_00_20/source/ti/blestack/icall/src/inc" --include_path="/home/vinicio/ti/simplelink_cc2640r2_sdk_3_30_00_20/source/ti/blestack/npi/src" --include_path="/home/vinicio/ti/simplelink_cc2640r2_sdk_3_30_00_20/source/ti/blestack/osal/src/inc" --include_path="/home/vinicio/ti/simplelink_cc2640r2_sdk_3_30_00_20/source/ti/blestack/services/src/saddr" --include_path="/home/vinicio/ti/simplelink_cc2640r2_sdk_3_30_00_20/source/ti/blestack/services/src/sdata" --include_path="/home/vinicio/ti/simplelink_cc2640r2_sdk_3_30_00_20/source/ti/devices/cc26x0r2" --include_path="/home/vinicio/ti/ccs910/ccs/tools/compiler/ti-cgt-arm_18.12.2.LTS/include" --define=DeviceFamily_CC26X0R2 --define=Display_DISABLE_ALL --define=CC2640R2_LAUNCHXL --define=CC26XX --define=CC26XX_R2 --define=ICALL_EVENTS --define=ICALL_JT --define=ICALL_LITE --define=ICALL_MAX_NUM_ENTITIES=6 --define=ICALL_MAX_NUM_TASKS=3 --define=ICALL_STACK0_ADDR --define=MAX_NUM_BLE_CONNS=1 --define=MAX_PDU_SIZE=255 --define=NPI_USE_UART --define=xNPI_USE_SPI --define=NPI_SPI_CONFIG=Board_SPI0 --define=xPOWER_SAVING --define=STACK_LIBRARY --define=USE_ICALL --define=xdc_runtime_Assert_DISABLE_ALL --define=xdc_runtime_Log_DISABLE_ALL -g --c99 --gcc --diag_warning=225 --diag_wrap=off --display_error_number --gen_func_subsections=on --abi=eabi --preproc_with_compile --preproc_dependency="ICallBLE/$(basename $(<F)).d_raw" --obj_directory="ICallBLE" $(GEN_OPTS__FLAG) "$(shell echo $<)"
	@echo 'Finished building: "$<"'
	@echo ' '

ICallBLE/icall_api_lite.obj: /home/vinicio/ti/simplelink_cc2640r2_sdk_3_30_00_20/source/ti/blestack/icall/app/icall_api_lite.c $(GEN_OPTS) | $(GEN_FILES) $(GEN_MISC_FILES)
	@echo 'Building file: "$<"'
	@echo 'Invoking: ARM Compiler'
	"/home/vinicio/ti/ccs910/ccs/tools/compiler/ti-cgt-arm_18.12.2.LTS/bin/armcl" --cmd_file="/home/vinicio/ti/simplelink_cc2640r2_sdk_3_30_00_20/source/ti/blestack/config/build_components.opt" --cmd_file="/home/vinicio/ti/simplelink_cc2640r2_sdk_3_30_00_20/source/ti/blestack/config/factory_config.opt" --cmd_file="/home/vinicio/Documents/S5/S5_2019/CCS/host_test_cc2640r2lp_stack_library/TOOLS/build_config.opt"  -mv7M3 --code_state=16 -me -O4 --opt_for_speed=0 --include_path="/home/vinicio/Documents/S5/S5_2019/CCS/host_test_cc2640r2lp_app" --include_path="/home/vinicio/ti/simplelink_cc2640r2_sdk_3_30_00_20/source/ti/blestack/controller/cc26xx_r2/inc" --include_path="/home/vinicio/ti/simplelink_cc2640r2_sdk_3_30_00_20/source/ti/blestack/inc" --include_path="/home/vinicio/ti/simplelink_cc2640r2_sdk_3_30_00_20/source/ti/blestack/rom" --include_path="/home/vinicio/Documents/S5/S5_2019/CCS/host_test_cc2640r2lp_app/Application" --include_path="/home/vinicio/Documents/S5/S5_2019/CCS/host_test_cc2640r2lp_app/Startup" --include_path="/home/vinicio/Documents/S5/S5_2019/CCS/host_test_cc2640r2lp_app/PROFILES" --include_path="/home/vinicio/Documents/S5/S5_2019/CCS/host_test_cc2640r2lp_app/Include" --include_path="/home/vinicio/ti/simplelink_cc2640r2_sdk_3_30_00_20/source/ti/blestack/common/cc26xx" --include_path="/home/vinicio/ti/simplelink_cc2640r2_sdk_3_30_00_20/source/ti/blestack/icall/inc" --include_path="/home/vinicio/ti/simplelink_cc2640r2_sdk_3_30_00_20/source/ti/blestack/profiles/dev_info" --include_path="/home/vinicio/ti/simplelink_cc2640r2_sdk_3_30_00_20/source/ti/blestack/profiles/roles/cc26xx" --include_path="/home/vinicio/ti/simplelink_cc2640r2_sdk_3_30_00_20/source/ti/blestack/profiles/roles" --include_path="/home/vinicio/ti/simplelink_cc2640r2_sdk_3_30_00_20/source/ti/blestack/profiles/simple_profile/cc26xx" --include_path="/home/vinicio/ti/simplelink_cc2640r2_sdk_3_30_00_20/source/ti/blestack/profiles/simple_profile" --include_path="/home/vinicio/ti/simplelink_cc2640r2_sdk_3_30_00_20/source/ti/blestack/target" --include_path="/home/vinicio/ti/simplelink_cc2640r2_sdk_3_30_00_20/source/ti/blestack/hal/src/target/_common" --include_path="/home/vinicio/ti/simplelink_cc2640r2_sdk_3_30_00_20/source/ti/blestack/hal/src/target/_common/cc26xx" --include_path="/home/vinicio/ti/simplelink_cc2640r2_sdk_3_30_00_20/source/ti/blestack/hal/src/inc" --include_path="/home/vinicio/ti/simplelink_cc2640r2_sdk_3_30_00_20/source/ti/blestack/heapmgr" --include_path="/home/vinicio/ti/simplelink_cc2640r2_sdk_3_30_00_20/source/ti/blestack/icall/src/inc" --include_path="/home/vinicio/ti/simplelink_cc2640r2_sdk_3_30_00_20/source/ti/blestack/npi/src" --include_path="/home/vinicio/ti/simplelink_cc2640r2_sdk_3_30_00_20/source/ti/blestack/osal/src/inc" --include_path="/home/vinicio/ti/simplelink_cc2640r2_sdk_3_30_00_20/source/ti/blestack/services/src/saddr" --include_path="/home/vinicio/ti/simplelink_cc2640r2_sdk_3_30_00_20/source/ti/blestack/services/src/sdata" --include_path="/home/vinicio/ti/simplelink_cc2640r2_sdk_3_30_00_20/source/ti/devices/cc26x0r2" --include_path="/home/vinicio/ti/ccs910/ccs/tools/compiler/ti-cgt-arm_18.12.2.LTS/include" --define=DeviceFamily_CC26X0R2 --define=Display_DISABLE_ALL --define=CC2640R2_LAUNCHXL --define=CC26XX --define=CC26XX_R2 --define=ICALL_EVENTS --define=ICALL_JT --define=ICALL_LITE --define=ICALL_MAX_NUM_ENTITIES=6 --define=ICALL_MAX_NUM_TASKS=3 --define=ICALL_STACK0_ADDR --define=MAX_NUM_BLE_CONNS=1 --define=MAX_PDU_SIZE=255 --define=NPI_USE_UART --define=xNPI_USE_SPI --define=NPI_SPI_CONFIG=Board_SPI0 --define=xPOWER_SAVING --define=STACK_LIBRARY --define=USE_ICALL --define=xdc_runtime_Assert_DISABLE_ALL --define=xdc_runtime_Log_DISABLE_ALL -g --c99 --gcc --diag_warning=225 --diag_wrap=off --display_error_number --gen_func_subsections=on --abi=eabi --preproc_with_compile --preproc_dependency="ICallBLE/$(basename $(<F)).d_raw" --obj_directory="ICallBLE" $(GEN_OPTS__FLAG) "$(shell echo $<)"
	@echo 'Finished building: "$<"'
	@echo ' '

ICallBLE/icall_hci_tl.obj: /home/vinicio/ti/simplelink_cc2640r2_sdk_3_30_00_20/source/ti/blestack/icall/app/icall_hci_tl.c $(GEN_OPTS) | $(GEN_FILES) $(GEN_MISC_FILES)
	@echo 'Building file: "$<"'
	@echo 'Invoking: ARM Compiler'
	"/home/vinicio/ti/ccs910/ccs/tools/compiler/ti-cgt-arm_18.12.2.LTS/bin/armcl" --cmd_file="/home/vinicio/ti/simplelink_cc2640r2_sdk_3_30_00_20/source/ti/blestack/config/build_components.opt" --cmd_file="/home/vinicio/ti/simplelink_cc2640r2_sdk_3_30_00_20/source/ti/blestack/config/factory_config.opt" --cmd_file="/home/vinicio/Documents/S5/S5_2019/CCS/host_test_cc2640r2lp_stack_library/TOOLS/build_config.opt"  -mv7M3 --code_state=16 -me -O4 --opt_for_speed=0 --include_path="/home/vinicio/Documents/S5/S5_2019/CCS/host_test_cc2640r2lp_app" --include_path="/home/vinicio/ti/simplelink_cc2640r2_sdk_3_30_00_20/source/ti/blestack/controller/cc26xx_r2/inc" --include_path="/home/vinicio/ti/simplelink_cc2640r2_sdk_3_30_00_20/source/ti/blestack/inc" --include_path="/home/vinicio/ti/simplelink_cc2640r2_sdk_3_30_00_20/source/ti/blestack/rom" --include_path="/home/vinicio/Documents/S5/S5_2019/CCS/host_test_cc2640r2lp_app/Application" --include_path="/home/vinicio/Documents/S5/S5_2019/CCS/host_test_cc2640r2lp_app/Startup" --include_path="/home/vinicio/Documents/S5/S5_2019/CCS/host_test_cc2640r2lp_app/PROFILES" --include_path="/home/vinicio/Documents/S5/S5_2019/CCS/host_test_cc2640r2lp_app/Include" --include_path="/home/vinicio/ti/simplelink_cc2640r2_sdk_3_30_00_20/source/ti/blestack/common/cc26xx" --include_path="/home/vinicio/ti/simplelink_cc2640r2_sdk_3_30_00_20/source/ti/blestack/icall/inc" --include_path="/home/vinicio/ti/simplelink_cc2640r2_sdk_3_30_00_20/source/ti/blestack/profiles/dev_info" --include_path="/home/vinicio/ti/simplelink_cc2640r2_sdk_3_30_00_20/source/ti/blestack/profiles/roles/cc26xx" --include_path="/home/vinicio/ti/simplelink_cc2640r2_sdk_3_30_00_20/source/ti/blestack/profiles/roles" --include_path="/home/vinicio/ti/simplelink_cc2640r2_sdk_3_30_00_20/source/ti/blestack/profiles/simple_profile/cc26xx" --include_path="/home/vinicio/ti/simplelink_cc2640r2_sdk_3_30_00_20/source/ti/blestack/profiles/simple_profile" --include_path="/home/vinicio/ti/simplelink_cc2640r2_sdk_3_30_00_20/source/ti/blestack/target" --include_path="/home/vinicio/ti/simplelink_cc2640r2_sdk_3_30_00_20/source/ti/blestack/hal/src/target/_common" --include_path="/home/vinicio/ti/simplelink_cc2640r2_sdk_3_30_00_20/source/ti/blestack/hal/src/target/_common/cc26xx" --include_path="/home/vinicio/ti/simplelink_cc2640r2_sdk_3_30_00_20/source/ti/blestack/hal/src/inc" --include_path="/home/vinicio/ti/simplelink_cc2640r2_sdk_3_30_00_20/source/ti/blestack/heapmgr" --include_path="/home/vinicio/ti/simplelink_cc2640r2_sdk_3_30_00_20/source/ti/blestack/icall/src/inc" --include_path="/home/vinicio/ti/simplelink_cc2640r2_sdk_3_30_00_20/source/ti/blestack/npi/src" --include_path="/home/vinicio/ti/simplelink_cc2640r2_sdk_3_30_00_20/source/ti/blestack/osal/src/inc" --include_path="/home/vinicio/ti/simplelink_cc2640r2_sdk_3_30_00_20/source/ti/blestack/services/src/saddr" --include_path="/home/vinicio/ti/simplelink_cc2640r2_sdk_3_30_00_20/source/ti/blestack/services/src/sdata" --include_path="/home/vinicio/ti/simplelink_cc2640r2_sdk_3_30_00_20/source/ti/devices/cc26x0r2" --include_path="/home/vinicio/ti/ccs910/ccs/tools/compiler/ti-cgt-arm_18.12.2.LTS/include" --define=DeviceFamily_CC26X0R2 --define=Display_DISABLE_ALL --define=CC2640R2_LAUNCHXL --define=CC26XX --define=CC26XX_R2 --define=ICALL_EVENTS --define=ICALL_JT --define=ICALL_LITE --define=ICALL_MAX_NUM_ENTITIES=6 --define=ICALL_MAX_NUM_TASKS=3 --define=ICALL_STACK0_ADDR --define=MAX_NUM_BLE_CONNS=1 --define=MAX_PDU_SIZE=255 --define=NPI_USE_UART --define=xNPI_USE_SPI --define=NPI_SPI_CONFIG=Board_SPI0 --define=xPOWER_SAVING --define=STACK_LIBRARY --define=USE_ICALL --define=xdc_runtime_Assert_DISABLE_ALL --define=xdc_runtime_Log_DISABLE_ALL -g --c99 --gcc --diag_warning=225 --diag_wrap=off --display_error_number --gen_func_subsections=on --abi=eabi --preproc_with_compile --preproc_dependency="ICallBLE/$(basename $(<F)).d_raw" --obj_directory="ICallBLE" $(GEN_OPTS__FLAG) "$(shell echo $<)"
	@echo 'Finished building: "$<"'
	@echo ' '


