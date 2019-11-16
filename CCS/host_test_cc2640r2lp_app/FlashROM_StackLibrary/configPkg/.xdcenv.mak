#
_XDCBUILDCOUNT = 
ifneq (,$(findstring path,$(_USEXDCENV_)))
override XDCPATH = /home/vinicio/ti/simplelink_cc2640r2_sdk_3_30_00_20/source;/home/vinicio/ti/simplelink_cc2640r2_sdk_3_30_00_20/kernel/tirtos/packages;/home/vinicio/ti/simplelink_cc2640r2_sdk_3_30_00_20/source/ti/blestack
override XDCROOT = /home/vinicio/ti/xdctools_3_51_03_28_core
override XDCBUILDCFG = ./config.bld
endif
ifneq (,$(findstring args,$(_USEXDCENV_)))
override XDCARGS = 
override XDCTARGETS = 
endif
#
ifeq (0,1)
PKGPATH = /home/vinicio/ti/simplelink_cc2640r2_sdk_3_30_00_20/source;/home/vinicio/ti/simplelink_cc2640r2_sdk_3_30_00_20/kernel/tirtos/packages;/home/vinicio/ti/simplelink_cc2640r2_sdk_3_30_00_20/source/ti/blestack;/home/vinicio/ti/xdctools_3_51_03_28_core/packages;..
HOSTOS = Linux
endif
