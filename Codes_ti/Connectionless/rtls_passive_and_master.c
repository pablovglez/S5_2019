/******************************************************************************

 @file  rtls_passive_and_master.c

 @brief This file contains the RTLS Passive sample application for use
         with the CC2650 Bluetooth Low Energy Protocol Stack.

  Group: WCS, BTS
  Target Device: cc2640r2

  ******************************************************************************

#include "rtls_passive.h"

#include <string.h>
#include <stdlib.h>

#include <ti/sysbios/BIOS.h>
#include <ti/sysbios/knl/Task.h>
#include <ti/sysbios/knl/Clock.h>
#include <ti/sysbios/knl/Event.h>
#include <ti/sysbios/knl/Queue.h>
#include <ti/sysbios/hal/Hwi.h>

#include "bcomdef.h"
#include "micro_ble_cm.h"

#include <icall.h>
#include "util.h"
/* This Header file contains all BLE API and icall structure definition */
#include "icall_ble_api.h"
#include "board.h"

#include "central.h"
#include "simple_gatt_profile.h"

// DriverLib
#include <driverlib/aon_batmon.h>
#include "rtls/rtls_ctrl_api.h"
#include "uble.h"
#include "ugap.h"
#include "urfc.h"

#include "board_key.h"
#include "board.h"
#include "util.h"
#include "gap.h"

#include "rtls_master.h"

#include "rtls/rtls_ctrl_api.h"
// RTLS
#include "rtls/rtls_ble.h"

/*********************************************************************
 * MACROS
 */

/*********************************************************************
 * CONSTANTS
 */

#define RTLS_MASTER_STATE_CHANGE_EVT                  0x0001
#define RTLS_MASTER_KEY_CHANGE_EVT                    0x0002
#define RTLS_MASTER_PAIRING_STATE_EVT                 0x0004
#define RTLS_MASTER_PASSCODE_NEEDED_EVT               0x0008
#define RTLS_MASTER_RTLS_MSG_EVT                      0x0010
// Stack Task configuration
#define UBT_TASK_PRIORITY                     3

// Simple Central Task Events
#define RTLS_MASTER_ICALL_EVT                         ICALL_MSG_EVENT_ID // Event_Id_31
#define RTLS_MASTER_QUEUE_EVT                         UTIL_QUEUE_EVENT_ID // Event_Id_30
#ifndef UBT_TASK_STACK_SIZE
#define UBT_TASK_STACK_SIZE                   800
#endif

#define RTLS_MASTER_ALL_EVENTS                        (RTLS_MASTER_ICALL_EVT           | \
                                                       RTLS_MASTER_QUEUE_EVT)
// App Task configuration
#define UCA_TASK_PRIORITY                     2

// Maximum number of scan responses
#define DEFAULT_MAX_SCAN_RES                  8

// Scan duration in ms
#define DEFAULT_SCAN_DURATION                 2000

// Discovery mode (limited, general, all)
#define DEFAULT_DISCOVERY_MODE                DEVDISC_MODE_ALL

// TRUE to use active scan
#define DEFAULT_DISCOVERY_ACTIVE_SCAN         TRUE

// Set desired policy to use during discovery (use values from GAP_Disc_Filter_Policies)
#define DEFAULT_DISCOVERY_WHITE_LIST          GAP_DISC_FILTER_POLICY_ALL

// TRUE to use high scan duty cycle when creating link
#define DEFAULT_LINK_HIGH_DUTY_CYCLE          FALSE

// TRUE to use white list when creating link
#define DEFAULT_LINK_WHITE_LIST               FALSE

// After the connection is formed, the central will accept connection parameter
// update requests from the peripheral
#define DEFAULT_ENABLE_UPDATE_REQUEST         GAPCENTRALROLE_PARAM_UPDATE_REQ_AUTO_ACCEPT

// Minimum connection interval (units of 1.25ms) if automatic parameter update
// request is enabled
#define DEFAULT_UPDATE_MIN_CONN_INTERVAL      400

// Maximum connection interval (units of 1.25ms) if automatic parameter update
// request is enabled
#define DEFAULT_UPDATE_MAX_CONN_INTERVAL      800

// Slave latency to use if automatic parameter update request is enabled
#define DEFAULT_UPDATE_SLAVE_LATENCY          0

// Supervision timeout value (units of 10ms) if automatic parameter update
// request is enabled
#define DEFAULT_UPDATE_CONN_TIMEOUT           600

// Default GAP pairing mode
#define DEFAULT_PAIRING_MODE                  GAPBOND_PAIRING_MODE_INITIATE

// Default MITM mode (TRUE to require passcode or OOB when pairing)
#define DEFAULT_MITM_MODE                     TRUE

// Default bonding mode, TRUE to bond
#define DEFAULT_BONDING_MODE                  TRUE

// Default GAP bonding I/O capabilities
#define DEFAULT_IO_CAPABILITIES               GAPBOND_IO_CAP_KEYBOARD_ONLY

// Default service discovery timer delay in ms
#define DEFAULT_SVC_DISCOVERY_DELAY           1000

// Length of bd addr as a string
#define B_ADDR_STR_LEN                        15

// Task configuration
#define RTLS_MASTER_TASK_PRIORITY             1

#ifndef RTLS_MASTER_TASK_STACK_SIZE
#define RTLS_MASTER_TASK_STACK_SIZE           752
#endif
#ifndef UCA_TASK_STACK_SIZE
#define UCA_TASK_STACK_SIZE                   800
#endif

// Application states
enum
{
  BLE_STATE_IDLE,
  BLE_STATE_CONNECTING,
  BLE_STATE_CONNECTED,
  BLE_STATE_DISCONNECTING
};

// Discovery states
enum
{
  BLE_DISC_STATE_IDLE,                // Idle
  BLE_DISC_STATE_MTU,                 // Exchange ATT MTU size
  BLE_DISC_STATE_SVC,                 // Service discovery
  BLE_DISC_STATE_CHAR                 // Characteristic discovery
};

// Key states for connections
typedef enum
{
  GATT_RW,                 // Perform GATT Read/Write
  RSSI,                    // Toggle RSSI updates
  CONN_UPDATE,             // Send Connection Parameter Update
  GET_CONN_INFO,           // Display Current Connection Information
  DISCONNECT               // Disconnect
} keyPressConnOpt_t;

// Connection event registration
typedef enum
{
  NOT_REGISTERED     = 0x0,
  FOR_ATT_RSP        = 0x2,
  FOR_TOF            = 0x4,
} connectionEventRegisterCause_u;

// Set the register cause to the registration bit-mask
#define CONNECTION_EVENT_REGISTER_BIT_SET(RegisterCause) (connEventRegCauseBitmap |= RegisterCause)
// Remove the register cause from the registration bit-mask
#define CONNECTION_EVENT_REGISTER_BIT_REMOVE(RegisterCause) (connEventRegCauseBitmap &= (~RegisterCause))
// Gets whether the current App is registered to the receive connection events
#define CONNECTION_EVENT_IS_REGISTERED (connEventRegCauseBitmap > 0)
// Gets whether the RegisterCause was registered to receive connection event
#define CONNECTION_EVENT_REGISTRATION_CAUSE(RegisterCause) (connEventRegCauseBitmap & RegisterCause)

// Hard coded PSM for passing data between central and peripheral
#define RTLS_PSM 			0x0080
#define RTLS_PDU_SIZE MAX_PDU_SIZE
/*********************************************************************
 * TYPEDEFS
 */

// RTLS Master event
typedef struct
{
  appEvtHdr_t hdr; // event header
  uint8_t *pData;  // event data
} rtlsMasterEvt_t;

// RSSI read data structure
typedef struct
{
  uint16_t period;      // how often to read RSSI
  uint16_t connHandle;  // connection handle
  Clock_Struct *pClock; // pointer to clock struct
} readRssi_t;
/*********************************************************************
 * GLOBAL VARIABLES
 */

/*********************************************************************
 * EXTERNAL VARIABLES
 */

/*********************************************************************
 * EXTERNAL FUNCTIONS
 */

/*********************************************************************
 * LOCAL VARIABLES
 */
// Event globally used to post local events and pend on local events.
Event_Handle syncAppEvent;

// Entity ID globally used to check for source and/or destination of messages
static ICall_EntityID selfEntity;

// Event globally used to post local events and pend on local events.
static Event_Handle syncStackEvent;

// Event globally used to post local events and pend on system and
// local events.
static ICall_SyncHandle syncEvent;

Task_Struct ubtTask;
uint8 ubtTaskStack[UBT_TASK_STACK_SIZE];

Task_Struct ucaTask;
uint8 ucaTaskStack[UCA_TASK_STACK_SIZE];

// Clock object used to signal timeout
static Clock_Struct startDiscClock;

static Queue_Struct stackMsg;
static Queue_Handle stackMsgQueue;

// Task configuration
Task_Struct rtlsMasterTask;
Char rtlsMasterTaskStack[RTLS_MASTER_TASK_STACK_SIZE];

// Queue object used for app messages
Queue_Struct appMsg;
Queue_Handle appMsgQueue;

// GAP GATT Attributes
static const uint8_t attDeviceName[GAP_DEVICE_NAME_LEN] = "RTLS Master";

// Flag to indicate whether we are reporting to RTLS Control or not
uint8_t gRtlsSyncEnabled = RTLS_FALSE;

// Number of scan results and scan result index
static uint8_t scanRes = 0;

// CM Session for RTLS Passive
uint8_t gCmSessionId = CM_INVALID_SESSION_ID;

// Scan result list
static gapDevRec_t devList[DEFAULT_MAX_SCAN_RES];

// CM is tracking
uint8_t gMonitorTracking = RTLS_FALSE;

// Scanning state
static bool scanningStarted = FALSE;

// Connection handle of current connection
static uint16_t connHandle = GAP_CONNHANDLE_INIT;

// Application state
static uint8_t state = BLE_STATE_IDLE;

// Unique CoC CID
uint16_t cocCID;

// Handle the registration and un-registration for the connection event
uint32_t connEventRegCauseBitmap = NOT_REGISTERED;

/*********************************************************************
 * LOCAL FUNCTIONS
 */
static void RTLSMaster_init(void);
static void RTLSMaster_taskFxn(UArg a0, UArg a1);

static void RTLSMaster_processGATTMsg(gattMsgEvent_t *pMsg);
static void RTLSMaster_processStackMsg(ICall_Hdr *pMsg);
static void RTLSMaster_processAppMsg(rtlsMasterEvt_t *pMsg);
static void RTLSMaster_processRoleEvent(gapCentralRoleEvent_t *pEvent);
static void RTLSMaster_addDeviceInfo(gapDeviceInfoEvent_t *pEvent);
static void RTLSMaster_processPairState(uint8_t state, uint8_t status);
static void RTLSMaster_processPasscode(uint16_t connectionHandle, uint8_t uiOutputs);
static void RTLSMaster_processCmdCompleteEvt(hciEvt_CmdComplete_t *pMsg);
static uint8_t RTLSMaster_eventCB(gapCentralRoleEvent_t *pEvent);
static void RTLSMaster_passcodeCB(uint8_t *deviceAddr, uint16_t connHandle,
                                  uint8_t uiInputs, uint8_t uiOutputs,
                                  uint32_t numComparison);
static void RTLSMaster_pairStateCB(uint16_t connHandle, uint8_t state, uint8_t status);
static uint8_t RTLSMaster_enqueueMsg(uint8_t event, uint8_t status, uint8_t *pData);

static void RTLSPassive_taskFxn(UArg a0, UArg a1);

// RTLS specific functions
static bStatus_t RTLSMaster_sendRTLSData(uint8_t *pMsg);
static void RTLSMaster_processRTLSScanReq(void);
static void RTLSMaster_processRTLSScanRes(gapDeviceInfoEvent_t *deviceInfo);
static void RTLSMaster_processRTLSConnReq(uint8_t *connReq);
static void RTLSMaster_processRTLSConnInfo(void);
static void RTLSMaster_enableRtlsSync(uint8_t enable);
static void RTLSMaster_connEvtCB(Gap_ConnEventRpt_t *pReport);
static void RTLSMaster_processRtlsMsg(uint8_t *pMsg);
static void RTLSMaster_terminateLinkReq(void);

//ubStack High Priority Task
static void ubStack_taskFxn(UArg a0, UArg a1);

// L2CAP COC Handling
static bStatus_t RTLSMaster_openL2CAPChanCoc(void);
static void RTLSMaster_processL2CAPSignalEvent(l2capSignalEvent_t *pMsg);
static void RTLSMaster_processL2CAPDataEvent(l2capDataEvent_t *pMsg);

static void uBLEStack_eventProxy(void);
static bStatus_t RTLSPassive_enqueueStackMsg(uint16 event, uint8 data);

// General message handling
static void RTLSPassive_processRtlsPassiveMsg(uint8_t *pMsg);

// Handling CM events
static void RTLSPassive_processCmMsg(uint8_t *pMsg);
static void RTLSPassive_monitorIndicationEvt(uint8_t *pData);
static void RTLSPassive_monitorCompleteEvt(uint8_t *pData);
static void RTLSPassive_monitorStateChangeEvt(ugapMonitorState_t newState);

// Handling RTLS Control events
static void RTLSPassive_processRtlsCtrlMsg(uint8_t *pMsg);
static void RTLSPassive_cmStartReq(uint8_t *pConnInfo);
static void RTLSPassive_enableRtlsSync(uint8_t enable);
static void RTLSPassive_terminateLinkReq(void);

/*********************************************************************
 * @fn      RTLSMaster_Init
 *
 * @brief   Initialization function for the Simple Central App Task.
 *          This is called during initialization and should contain
 *          any application specific initialization (ie. hardware
 *          initialization/setup, table initialization, power up
 *          notification).
 *
 * @param   none
 *
 * @return  none
 */
static void RTLSMaster_init(void)
{
  // ******************************************************************
  // N0 STACK API CALLS CAN OCCUR BEFORE THIS CALL TO ICall_registerApp
  // ******************************************************************
  // Register the current thread as an ICall dispatcher application
  // so that the application can send and receive messages.
  ICall_registerApp(&selfEntity, &syncEvent);

  // Create an RTOS queue for message from profile to be sent to app.
  appMsgQueue = Util_constructQueue(&appMsg);

  // Setup the Central GAPRole Profile. For more information see the GAP section
  // in the User's Guide:
  // http://software-dl.ti.com/lprf/sdg-latest/html/
  {
    uint8_t scanRes = DEFAULT_MAX_SCAN_RES;

    GAPCentralRole_SetParameter(GAPCENTRALROLE_MAX_SCAN_RES, sizeof(uint8_t),
                                &scanRes);
  }

  // Set GAP Parameters to set the discovery duration
  // For more information, see the GAP section of the User's Guide:
  // http://software-dl.ti.com/lprf/sdg-latest/html/
  GAP_SetParamValue(TGAP_GEN_DISC_SCAN, DEFAULT_SCAN_DURATION);
  GAP_SetParamValue(TGAP_LIM_DISC_SCAN, DEFAULT_SCAN_DURATION);
  GGS_SetParameter(GGS_DEVICE_NAME_ATT, GAP_DEVICE_NAME_LEN,
                   (void *)attDeviceName);

  // Setup the GAP Bond Manager. For more information see the GAP Bond Manager
  // section in the User's Guide:
  // http://software-dl.ti.com/lprf/sdg-latest/html/
  {
    // Don't send a pairing request after connecting; the device waits for the
    // application to start pairing
    uint8_t pairMode = DEFAULT_PAIRING_MODE;
    // Do not use authenticated pairing
    uint8_t mitm = DEFAULT_MITM_MODE;
    // This is a display only device
    uint8_t ioCap = DEFAULT_IO_CAPABILITIES;
    // Create a bond during the pairing process
    uint8_t bonding = DEFAULT_BONDING_MODE;
    // Whether to replace the least recently used entry when bond list is full,
    // and a new device is bonded.
    // Alternative is pairing succeeds but bonding fails, unless application has
    // manually erased at least one bond.
    uint8_t replaceBonds = TRUE;

    GAPBondMgr_SetParameter(GAPBOND_PAIRING_MODE, sizeof(uint8_t), &pairMode);
    GAPBondMgr_SetParameter(GAPBOND_MITM_PROTECTION, sizeof(uint8_t), &mitm);
    GAPBondMgr_SetParameter(GAPBOND_IO_CAPABILITIES, sizeof(uint8_t), &ioCap);
    GAPBondMgr_SetParameter(GAPBOND_BONDING_ENABLED, sizeof(uint8_t), &bonding);
    GAPBondMgr_SetParameter(GAPBOND_LRU_BOND_REPLACEMENT, sizeof(uint8_t), &replaceBonds);
  }

  // Initialize GATT Client
  VOID GATT_InitClient();

  // Register to receive incoming ATT Indications/Notifications
  GATT_RegisterForInd(selfEntity);

  // Initialize GATT attributes
  GGS_AddService(GATT_ALL_SERVICES);         // GAP
  GATTServApp_AddService(GATT_ALL_SERVICES); // GATT attributes

  // Start the Device
  VOID GAPCentralRole_StartDevice(&RTLSMaster_roleCB);

  // Register with bond manager after starting device
  GAPBondMgr_Register(&RTLSMaster_bondCB);

  // Register with GAP for HCI/Host messages (for RSSI)
  GAP_RegisterForMsgs(selfEntity);

  // Register for GATT local events and ATT Responses pending for transmission
  GATT_RegisterForMsgs(selfEntity);

  //Set default values for Data Length Extension
  {
    //Set initial values to maximum, RX is set to max. by default(251 octets, 2120us)
    #define APP_SUGGESTED_PDU_SIZE 251 //default is 27 octets(TX)
    #define APP_SUGGESTED_TX_TIME 2120 //default is 328us(TX)

    //This API is documented in hci.h
    //See the LE Data Length Extension section in the BLE-Stack User's Guide for information on using this command:
    //http://software-dl.ti.com/lprf/sdg-latest/html/cc2640/index.html
    //HCI_LE_WriteSuggestedDefaultDataLenCmd(APP_SUGGESTED_PDU_SIZE, APP_SUGGESTED_TX_TIME);
  }
}

/*********************************************************************
 * @fn      RTLSMaster_taskFxn
 *
 * @brief   Application task entry point for the Simple Central.
 *
 * @param   none
 *
 * @return  events not processed
 */
static void RTLSMaster_taskFxn(UArg a0, UArg a1)
{
  // Initialize application
  RTLSMaster_init();

  // Application main loop
  for (;;)
  {
    uint32_t events;

    events = Event_pend(syncEvent, Event_Id_NONE, RTLS_MASTER_ALL_EVENTS,
                        ICALL_TIMEOUT_FOREVER);

    if (events)
    {
      ICall_EntityID dest;
      ICall_ServiceEnum src;
      ICall_HciExtEvt *pMsg = NULL;

      if (ICall_fetchServiceMsg(&src, &dest,
                                (void **)&pMsg) == ICALL_ERRNO_SUCCESS)
      {
        if ((src == ICALL_SERVICE_CLASS_BLE) && (dest == selfEntity))
        {
          // Process inter-task message
          RTLSMaster_processStackMsg((ICall_Hdr *)pMsg);
        }

        if (pMsg)
        {
          ICall_freeMsg(pMsg);
        }
      }

      // If RTOS queue is not empty, process app message
      if (events & RTLS_MASTER_QUEUE_EVT)
      {
        while (!Queue_empty(appMsgQueue))
        {
          rtlsMasterEvt_t *pMsg = (rtlsMasterEvt_t *)Util_dequeueMsg(appMsgQueue);
          if (pMsg)
          {
            // Process message
            RTLSMaster_processAppMsg(pMsg);

            // Free the space from the message
            ICall_free(pMsg);
          }
        }
      }
    }
  }
}

/*********************************************************************
 * @fn      RTLSMaster_processStackMsg
 *
 * @brief   Process an incoming task message.
 *
 * @param   pMsg - message to process
 *
 * @return  none
 */
static void RTLSMaster_processStackMsg(ICall_Hdr *pMsg)
{
  switch (pMsg->event)
  {
    case GAP_MSG_EVENT:
    {
      RTLSMaster_processRoleEvent((gapCentralRoleEvent_t *)pMsg);
    }
    break;

    case GATT_MSG_EVENT:
    {
      RTLSMaster_processGATTMsg((gattMsgEvent_t *)pMsg);
    }
    break;

    case L2CAP_SIGNAL_EVENT:
    {
      RTLSMaster_processL2CAPSignalEvent((l2capSignalEvent_t *)pMsg);
    }
    break;

    case L2CAP_DATA_EVENT:
    {
      RTLSMaster_processL2CAPDataEvent((l2capDataEvent_t *)pMsg);
    }
    break;

    case HCI_GAP_EVENT_EVENT:
    {
      switch(pMsg->status)
      {
        case HCI_COMMAND_COMPLETE_EVENT_CODE:
        {
          RTLSMaster_processCmdCompleteEvt((hciEvt_CmdComplete_t *)pMsg);
        }
        break;

        case HCI_BLE_HARDWARE_ERROR_EVENT_CODE:
        {
          AssertHandler(HAL_ASSERT_CAUSE_HARDWARE_ERROR,0);
        }
        break;

        default:
          break;
      }
    }
    break;

    default:
      break;
  }
}

/*********************************************************************
 * @fn      RTLSMaster_processAppMsg
 *
 * @brief   Central application event processing function.
 *
 * @param   pMsg - pointer to event structure
 *
 * @return  none
 */
static void RTLSMaster_processAppMsg(rtlsMasterEvt_t *pMsg)
{
  switch (pMsg->hdr.event)
  {
    case RTLS_MASTER_STATE_CHANGE_EVT:
    {
      RTLSMaster_processStackMsg((ICall_Hdr *)pMsg->pData);

      // Free the stack message
      ICall_freeMsg(pMsg->pData);
    }
    break;

    // Pairing event
    case RTLS_MASTER_PAIRING_STATE_EVT:
    {
      RTLSMaster_processPairState(pMsg->hdr.state, *pMsg->pData);

      ICall_free(pMsg->pData);
    }
    break;

    // Passcode event
    case RTLS_MASTER_PASSCODE_NEEDED_EVT:
    {
      RTLSMaster_processPasscode(connHandle, *pMsg->pData);

      ICall_free(pMsg->pData);
    }
    break;

    case RTLS_MASTER_RTLS_MSG_EVT:
    {
      RTLSMaster_processRtlsMsg((uint8_t *)pMsg->pData);

      ICall_free(pMsg->pData);
    }
    break;

    default:
      break;
  }
}

/*********************************************************************
 * @fn      RTLSMaster_processRoleEvent
 *
 * @brief   Central role event processing function.
 *
 * @param   pEvent - pointer to event structure
 *
 * @return  none
 */
static void RTLSMaster_processRoleEvent(gapCentralRoleEvent_t *pEvent)
{
  switch (pEvent->gap.opcode)
  {
    case GAP_DEVICE_INIT_DONE_EVENT:
    {
      if (pEvent->gap.hdr.status != SUCCESS)
      {
        // If we failed to initialize GAP, assert
        AssertHandler(HAL_ASSERT_CAUSE_INTERNAL_ERROR, 0);
      }
    }
    break;

    case GAP_DEVICE_INFO_EVENT:
    {
      char slaveScanRsp[] = {'R','T','L','S','S','l','a','v','e'};

      // Filter results by the slave's scanRsp array
      if (memcmp(&pEvent->deviceInfo.pEvtData[2], slaveScanRsp, sizeof(slaveScanRsp)))
      {
        return;
      }

      RTLSMaster_addDeviceInfo(&pEvent->deviceInfo);
    }
    break;

    case GAP_DEVICE_DISCOVERY_EVENT:
    {
      if (pEvent->gap.hdr.status == SUCCESS)
      {
        // Scan Complete
        scanningStarted = FALSE;

        // Copy results
        scanRes = pEvent->discCmpl.numDevs;

        if (scanRes)
        {
          memcpy(devList, pEvent->discCmpl.pDevList, (sizeof(gapDevRec_t) * scanRes));
        }

        // Scan stopped (no more results)
        RTLSCtrl_scanResultEvt(RTLS_SUCCESS, NULL, NULL);
      }
      else
      {
        // Scan stopped (failed due to wrong parameters)
        RTLSCtrl_scanResultEvt(RTLS_FAIL, NULL, NULL);
      }
    }
    break;

    case GAP_LINK_ESTABLISHED_EVENT:
    {
      if (pEvent->gap.hdr.status == SUCCESS)
      {
        state = BLE_STATE_CONNECTED;
        connHandle = pEvent->linkCmpl.connectionHandle;

        HCI_LE_ReadRemoteUsedFeaturesCmd(connHandle);

        // We send out the connection information at this point
        // Note: we are not yet connected (will be after pairing)
        RTLSMaster_processRTLSConnInfo();
      }
      else
      {
        state = BLE_STATE_IDLE;
        connHandle = GAP_CONNHANDLE_INIT;

        // Link failed to establish
        RTLSCtrl_connResultEvt(RTLS_LINK_ESTAB_FAIL);
      }
    }
    break;

    case GAP_LINK_TERMINATED_EVENT:
    {
      state = BLE_STATE_IDLE;
      connHandle = GAP_CONNHANDLE_INIT;

      // Link terminated
      RTLSCtrl_connResultEvt(RTLS_LINK_TERMINATED);
    }
    break;

    case GAP_LINK_PARAM_UPDATE_EVENT:
    {
      // Upon param update, resend connection information
      RTLSMaster_processRTLSConnInfo();
    }
    break;

    default:
      break;
  }
}


/*********************************************************************
 * @fn      RTLSMaster_processGATTMsg
 *
 * @brief   Process GATT messages and events.
 *
 * @return  none
 */
static void RTLSMaster_processGATTMsg(gattMsgEvent_t *pMsg)
{
  // This example does not deal with GATT messages, just free the message
  GATT_bm_free(&pMsg->msg, pMsg->method);
}

/*********************************************************************
 * @fn      RTLSMaster_processCmdCompleteEvt
 *
 * @brief   Process an incoming OSAL HCI Command Complete Event.
 *
 * @param   pMsg - message to process
 *
 * @return  none
 */
static void RTLSMaster_processCmdCompleteEvt(hciEvt_CmdComplete_t *pMsg)
{
  switch (pMsg->cmdOpcode)
  {
    default:
      break;
  }
}

/*********************************************************************
 * @fn      RTLSMaster_processPairState
 *
 * @brief   Process the new paring state.
 *
 * @return  none
 */
static void RTLSMaster_processPairState(uint8_t state, uint8_t status)
{
  // Once Master and Slave are paired , we can open a COC channel
  if ((state == GAPBOND_PAIRING_STATE_COMPLETE) || (state == GAPBOND_PAIRING_STATE_BONDED))
  {
    if (status == SUCCESS)
    {
      // We are paired, open a L2CAP channel to pass data
      if (RTLSMaster_openL2CAPChanCoc() != SUCCESS)
      {
        RTLSCtrl_connResultEvt(RTLS_LINK_ESTAB_FAIL);
      }
    }
    else
    {
      // We could not establish a link with RTLS Slave
      RTLSCtrl_connResultEvt(RTLS_LINK_ESTAB_FAIL);
    }
  }
}

/*********************************************************************
 * @fn      RTLSMaster_processPasscode
 *
 * @brief   Process the Passcode request.
 *
 * @return  none
 */
static void RTLSMaster_processPasscode(uint16_t connectionHandle,
                                             uint8_t uiOutputs)
{
  // This app uses a default passcode. A real-life scenario would handle all
  // pairing scenarios and likely generate this randomly.
  uint32_t passcode = B_APP_DEFAULT_PASSCODE;

  // Send passcode response
  GAPBondMgr_PasscodeRsp(connectionHandle, SUCCESS, passcode);
}

/*********************************************************************
 * @fn      RTLSMaster_addDeviceInfo
 *
 * @brief   Add a device to the device discovery result list
 *
 * @return  none
 */
static void RTLSMaster_addDeviceInfo(gapDeviceInfoEvent_t *deviceInfo)
{
  uint8_t i;

  // If result count not at max
  if (scanRes < DEFAULT_MAX_SCAN_RES)
  {
    // Check if device is already in scan results
    for (i = 0; i < scanRes; i++)
    {
      if (memcmp(deviceInfo->addr, devList[i].addr , B_ADDR_LEN) == 0)
      {
        return;
      }
    }

    // Send the device info to RTLS Control
    RTLSMaster_processRTLSScanRes(deviceInfo);

    // Add addr to scan result list
    memcpy(devList[scanRes].addr, deviceInfo->addr, B_ADDR_LEN);
    devList[scanRes].addrType = deviceInfo->addrType;

    // Increment scan result count
    scanRes++;
  }
}

/*********************************************************************
 * @fn      RTLSMaster_eventCB
 *
 * @brief   Central event callback function.
 *
 * @param   pEvent - pointer to event structure
 *
 * @return  TRUE if safe to deallocate event message, FALSE otherwise.
 */
static uint8_t RTLSMaster_eventCB(gapCentralRoleEvent_t *pEvent)
{
  // Forward the role event to the application
  if (RTLSMaster_enqueueMsg(RTLS_MASTER_STATE_CHANGE_EVT,
                                  SUCCESS, (uint8_t *)pEvent))
  {
    // App will process and free the event
    return FALSE;
  }

  // Caller should free the event
  return TRUE;
}

/*********************************************************************
 * @fn      RTLSMaster_pairStateCB
 *
 * @brief   Pairing state callback.
 *
 * @return  none
 */
static void RTLSMaster_pairStateCB(uint16_t connHandle, uint8_t state, uint8_t status)
{
  uint8_t *pData = NULL;

  // Allocate space for the event data.
  if (pData = ICall_malloc(sizeof(uint8_t)))
  {
    *pData = status;

    // Queue the event.
    if (RTLSMaster_enqueueMsg(RTLS_MASTER_PAIRING_STATE_EVT, state, pData) == FALSE)
    {
      ICall_free(pData);
    }
  }
}

/*********************************************************************
 * @fn      RTLSMaster_passcodeCB
 *
 * @brief   Passcode callback.
 *
 * @return  none
 */
static void RTLSMaster_passcodeCB(uint8_t *deviceAddr, uint16_t connHandle,
                                  uint8_t uiInputs, uint8_t uiOutputs,
                                  uint32_t numComparison)
{
  uint8_t *pData = NULL;

  // Allocate space for the passcode event.
  if (pData = ICall_malloc(sizeof(uint8_t)))
  {
    *pData = uiOutputs;

    // Enqueue the event.
    if (RTLSMaster_enqueueMsg(RTLS_MASTER_PASSCODE_NEEDED_EVT, 0, pData) == FALSE)
    {
      ICall_free(pData);
    }
  }
}

/*********************************************************************
 * @fn      RTLSMaster_enqueueMsg
 *
 * @brief   Creates a message and puts the message in RTOS queue.
 *
 * @param   event - message event.
 * @param   state - message state.
 * @param   pData - message data pointer.
 *
 * @return  TRUE or FALSE
 */
static uint8_t RTLSMaster_enqueueMsg(uint8_t event, uint8_t state, uint8_t *pData)
{
  rtlsMasterEvt_t *pMsg = ICall_malloc(sizeof(rtlsMasterEvt_t));

  // Create dynamic pointer to message.
  if (pMsg)
  {
    pMsg->hdr.event = event;
    pMsg->hdr.state = state;
    pMsg->pData = pData;

    // Enqueue the message.
    return Util_enqueueMsg(appMsgQueue, syncEvent, (uint8_t *)pMsg);
  }

  return FALSE;
}

/*********************************************************************
 * @fn      RTLSMaster_connEvtCB
 *
 * @brief   Connection event callback.
 *
 * @param   pReport - pointer to connection event report
 *
 * @return  none
 */
static void RTLSMaster_connEvtCB(Gap_ConnEventRpt_t *pReport)
{
  // Sanity check
  if (!pReport)
  {
    return;
  }

  if (CONNECTION_EVENT_REGISTRATION_CAUSE(FOR_TOF))
  {
    rtlsStatus_e status;

    // Convert BLE specific status to RTLS Status
    if (pReport->status != GAP_CONN_EVT_STAT_MISSED)
    {
      status = RTLS_SUCCESS;
    }
    else
    {
      status = RTLS_FAIL;
    }

    RTLSCtrl_syncEventNotify(status, pReport->nextTaskTime, pReport->lastRssi, pReport->channel);
  }

  if (pReport != NULL)
  {
    // Free the report once we are done using it
    ICall_free(pReport);
  }
}

/*********************************************************************
 * @fn      RTLSMaster_sendRTLSData
 *
 * @brief   Send RTLS data to the peer
 *
 * @param   pMsg - pointer to the message to send
 *
 * @return  none
 */
static bStatus_t RTLSMaster_sendRTLSData(uint8_t *pMsg)
{
  l2capPacket_t pkt;
  rtlsPacket_t *req;
  bStatus_t status = SUCCESS;

  // Sanity check
  if (!pMsg)
  {
    return FAILURE;
  }

  // Cast to appropriate struct
  req = (rtlsPacket_t *)pMsg;

  // Tell L2CAP the desired Channel ID
  pkt.CID = cocCID;

  // Allocate space for payload
  pkt.pPayload = L2CAP_bm_alloc(req->payloadLen);

  if (pkt.pPayload != NULL)
  {
    // The request is the payload for the L2CAP SDU
    memcpy(pkt.pPayload, req, req->payloadLen);
    pkt.len = req->payloadLen;
    status = L2CAP_SendSDU(&pkt);

    // Check that the packet was sent
    if (SUCCESS != status)
    {
      // If SDU wasn't sent, free
      BM_free(pkt.pPayload);
    }
  }
  else
  {
    status = bleMemAllocError;
  }

  return (status);
}

/*********************************************************************
 * @fn      RTLSMaster_processRTLSScanRes
 *
 * @brief   Process a scan response and forward to RTLS Control
 *
 * @param   deviceInfo - a single scan response
 *
 * @return  none
 */
static void RTLSMaster_processRTLSScanRes(gapDeviceInfoEvent_t *deviceInfo)
{
  gapDeviceInfoEvent_t *devInfo;
  size_t resSize;
  bleScanInfo_t *scanResult;

  // Sanity check
  if (!deviceInfo)
  {
    return;
  }

  devInfo = deviceInfo;

  // Assign and allocate space
  resSize = sizeof(bleScanInfo_t) + devInfo->dataLen;
  scanResult = (bleScanInfo_t *)ICall_malloc(resSize);

  // We could not allocate memory, report to host and exit
  if (!scanResult)
  {
    RTLSCtrl_scanResultEvt(RTLS_OUT_OF_MEMORY, NULL, 0);
    return;
  }

  memcpy(scanResult->addr, devInfo->addr, B_ADDR_LEN);
  scanResult->addrType = devInfo->addrType;
  scanResult->eventType = devInfo->eventType;
  scanResult->dataLen = devInfo->dataLen;
  scanResult->rssi = devInfo->rssi;
  memcpy(scanResult->pEvtData, devInfo->pEvtData, devInfo->dataLen);

  RTLSCtrl_scanResultEvt(RTLS_SUCCESS, (uint8_t*)scanResult, resSize);

  ICall_free(scanResult);
}

/*********************************************************************
 * @fn      RTLSMaster_processRTLSScanReq
 *
 * @brief   Process a scan request
 *
 * @param   none
 *
 * @return  none
 */
static void RTLSMaster_processRTLSScanReq(void)
{
  // Start discovery
  if ((state != BLE_STATE_CONNECTED) && (!scanningStarted))
  {
    scanningStarted = TRUE;
    scanRes = 0;

    GAPCentralRole_StartDiscovery(DEFAULT_DISCOVERY_MODE,
                                  DEFAULT_DISCOVERY_ACTIVE_SCAN,
                                  DEFAULT_DISCOVERY_WHITE_LIST);
  }
}

/*********************************************************************
 * @fn      RTLSMaster_processRTLSConnReq
 *
 * @brief   Start the connection process with another device
 *
 * @param   connReq - pointer from RTLS control containing connection params
 *
 * @return  none
 */
static void RTLSMaster_processRTLSConnReq(uint8_t *connReq)
{
  bleConnReq_t *bleConnReq;

  // Sanity check
  if (!connReq)
  {
   return;
  }

  // Cast to appropriate struct
  bleConnReq = (bleConnReq_t *)connReq;

  if (state == BLE_STATE_IDLE)
  {
    state = BLE_STATE_CONNECTING;

    // configure both Min/Max connection interval with same value
    GAP_SetParamValue(TGAP_CONN_EST_INT_MIN, bleConnReq->connInterval);
    GAP_SetParamValue(TGAP_CONN_EST_INT_MAX, bleConnReq->connInterval);

    GAPCentralRole_EstablishLink(DEFAULT_LINK_HIGH_DUTY_CYCLE,
                                 DEFAULT_LINK_WHITE_LIST,
                                 bleConnReq->addrType, bleConnReq->addr);
  }
}

/*********************************************************************
 * @fn      RTLSMaster_processRTLSConnRes
 *
 * @brief   Process a connection established event - send conn info to RTLS Control
 *
 * @param   status - Establishing a connection succeeded/failed
 *          If this fails then the error code should correspond to rtlsErrorCodes_e
 *
 * @return  none
 */
static void RTLSMaster_processRTLSConnInfo(void)
{
  hciActiveConnInfo_t connInfo;
  bleConnInfo_t rtlsConnInfo = {0};

  // Send connection information to RTLS Control
  HCI_EXT_GetActiveConnInfoCmd(0, &connInfo);

  rtlsConnInfo.accessAddr = connInfo.accessAddr;
  rtlsConnInfo.connInterval = connInfo.connInterval;
  rtlsConnInfo.currChan = connInfo.nextChan;
  rtlsConnInfo.hopValue = connInfo.hopValue;
  rtlsConnInfo.mSCA = connInfo.mSCA;
  rtlsConnInfo.crcInit = BUILD_UINT32(connInfo.crcInit[0], connInfo.crcInit[1], connInfo.crcInit[2], 0);

  memcpy(rtlsConnInfo.chanMap, connInfo.chanMap, LL_NUM_BYTES_FOR_CHAN_MAP);

  RTLSCtrl_connInfoEvt((uint8_t*)&rtlsConnInfo, sizeof(bleConnInfo_t));
}

/*********************************************************************
 * @fn      RTLSMaster_openL2CAPChanCoc
 *
 * @brief   Opens a communication channel between RTLS Master/Slave
 *
 * @param   pairState - Verify that devices are paired
 *
 * @return  status - 0 = success, 1 = failed
 */
static bStatus_t RTLSMaster_openL2CAPChanCoc(void)
{
  bStatus_t ret;
  l2capPsm_t psm;
  l2capPsmInfo_t psmInfo;

  if (L2CAP_PsmInfo(RTLS_PSM, &psmInfo) == INVALIDPARAMETER)
  {
    // Prepare the PSM parameters
    psm.initPeerCredits = 0xFFFF;
    psm.maxNumChannels = 1;
    psm.mtu = RTLS_PDU_SIZE;
    psm.peerCreditThreshold = 0;
    psm.pfnVerifySecCB = NULL;
    psm.psm = RTLS_PSM;
    psm.taskId = ICall_getLocalMsgEntityId(ICALL_SERVICE_CLASS_BLE_MSG, selfEntity);

    // Register PSM with L2CAP task
    ret = L2CAP_RegisterPsm(&psm);

    if (ret == SUCCESS)
    {
      // Send the connection request to RTLS slave
      ret = L2CAP_ConnectReq(connHandle, RTLS_PSM, RTLS_PSM);
    }
  }
  else
  {
    // Send the connection request to RTLS slave
    ret = L2CAP_ConnectReq(connHandle, RTLS_PSM, RTLS_PSM);
  }
  return ret;
}

/*********************************************************************
 * @fn      RTLSMaster_processL2CAPSignalEvent
 *
 * @brief   Handle L2CAP signal events
 *
 * @param   pMsg - pointer to the signal that was received
 *
 * @return  none
 */
static void RTLSMaster_processL2CAPSignalEvent(l2capSignalEvent_t *pMsg)
{
  // Sanity check
  if (!pMsg)
  {
    return;
  }

  switch (pMsg->opcode)
  {
    case L2CAP_CHANNEL_ESTABLISHED_EVT:
    {
      l2capChannelEstEvt_t *pEstEvt = &(pMsg->cmd.channelEstEvt);

      // Connection established, save the CID
      cocCID = pEstEvt->CID;

      // Give max credits to the other side
      L2CAP_FlowCtrlCredit(pEstEvt->CID, 0xFFFF);

      // L2CAP establishing a COC channel means that both Master and Slave are ready
      // Tell RTLS Control that we are ready for more commands
      RTLSCtrl_connResultEvt(RTLS_SUCCESS);
    }
    break;

    case L2CAP_SEND_SDU_DONE_EVT:
    {
      if (pMsg->hdr.status == SUCCESS)
      {
        RTLSCtrl_processDataSent(RTLS_SUCCESS);
      }
      else
      {
        RTLSCtrl_processDataSent(RTLS_FAIL);
      }
    }
    break;

    case L2CAP_CHANNEL_TERMINATED_EVT:
    {
      if (connHandle != GAP_CONNHANDLE_INIT)
      {
        GAPCentralRole_TerminateLink(connHandle);
        connHandle = GAP_CONNHANDLE_INIT;
      }
    }
    break;
  }
}

/*********************************************************************
 * @fn      RTLSMaster_processL2CAPDataEvent
 *
 * @brief   Handles incoming L2CAP data
 *
 * @param   pMsg - pointer to the signal that was received
 *
 * @return  none
 */
static void RTLSMaster_processL2CAPDataEvent(l2capDataEvent_t *pMsg)
{
  rtlsPacket_t *pRtlsPkt;

  // Sanity check
  if (!pMsg)
  {
    return;
  }

  // This application doesn't care about other L2CAP data events other than RTLS
  // It is possible to expand this function to support multiple COC CID's
  if (pMsg->pkt.CID == cocCID)
  {
    pRtlsPkt = (rtlsPacket_t *)ICall_malloc(pMsg->pkt.len);

    // Check for malloc error
    if (!pRtlsPkt)
    {
      // Free the payload (must use BM_free here according to L2CAP documentation)
      BM_free(pMsg->pkt.pPayload);
      return;
    }

    // Copy the payload
    memcpy(pRtlsPkt, pMsg->pkt.pPayload, pMsg->pkt.len);

    // Free the payload (must use BM_free here according to L2CAP documentation)
    BM_free(pMsg->pkt.pPayload);

    // RTLS Control will handle the information in the packet
    RTLSCtrl_processRtlsPacket((uint8_t *)pRtlsPkt);
  }
}

/*********************************************************************
 * @fn      RTLSMaster_enableRtlsSync
 *
 * @brief   This function is used by RTLS Control to notify the RTLS application
 *          to start sending synchronization events (for BLE this is a connection event)
 *
 * @param   enable - start/stop synchronization
 *
 * @return  none
 */
static void RTLSMaster_enableRtlsSync(uint8_t enable)
{
  bStatus_t status;

  if (enable == RTLS_TRUE)
  {
    if (!CONNECTION_EVENT_IS_REGISTERED)
    {
      status = GAP_RegisterConnEventCb(RTLSMaster_connEvtCB, GAP_CB_REGISTER, LINKDB_CONNHANDLE_ALL);
    }

    if (status == SUCCESS)
    {
      CONNECTION_EVENT_REGISTER_BIT_SET(FOR_TOF);
    }
  }
  else if (enable == RTLS_FALSE)
  {
    CONNECTION_EVENT_REGISTER_BIT_REMOVE(FOR_TOF);

    // If there is nothing registered to the connection event, request to unregister
    if (!CONNECTION_EVENT_IS_REGISTERED)
    {
      GAP_RegisterConnEventCb(RTLSMaster_connEvtCB, GAP_CB_UNREGISTER, LINKDB_CONNHANDLE_ALL);
    }
  }
}

/*********************************************************************
 * @fn      RTLSMaster_terminateLinkReq
 *
 * @brief   Terminate active link
 *
 * @param   none
 *
 * @return  none
 */
static void RTLSMaster_terminateLinkReq(void)
{
  if (connHandle != GAP_CONNHANDLE_INIT  && cocCID != 0)
  {
    L2CAP_DisconnectReq(cocCID);
    cocCID = 0;
  }
  else
  {
    RTLSCtrl_sendDebugEvent("Connection Handle invalid", GAP_CONNHANDLE_INIT);
  }
}

/*********************************************************************
 * @fn      RTLSMaster_processRtlsMsg
 *
 * @brief   Handle processing messages from RTLS Control
 *
 * @param   msg - a pointer to the message
 *
 * @return  none
 */
static void RTLSMaster_processRtlsMsg(uint8_t *pMsg)
{
  rtlsCtrlReq_t *pReq;

  // Sanity check
  if (!pMsg)
  {
    return;
  }

  // Cast to appropriate struct
  pReq = (rtlsCtrlReq_t *)pMsg;

  switch(pReq->reqOp)
  {
    case RTLS_REQ_CONN:
    {
      RTLSMaster_processRTLSConnReq(pReq->pData);
    }
    break;

    case RTLS_REQ_SCAN:
    {
      RTLSMaster_processRTLSScanReq();
    }
    break;

    case RTLS_REQ_ENABLE_SYNC:
    {
      RTLSMaster_enableRtlsSync(*pReq->pData);
    }
    break;

    case RTLS_REQ_SEND_DATA:
    {
      RTLSMaster_sendRTLSData(pReq->pData);
    }
    break;

    case RTLS_REQ_TERMINATE_LINK:
    {
      RTLSMaster_terminateLinkReq();
    }
    break;

    default:
      break;
  }

  // Free the payload
  if (pReq->pData)
  {
    ICall_free(pReq->pData);
  }
}

/*********************************************************************
 * @fn      RTLSMaster_rtlsCtrlMsgCb
 *
 * @brief   Callback given to RTLS Control
 *
 * @param  cmd - the command to be enqueued
 *
 * @return  none
 */
void RTLSMaster_rtlsCtrlMsgCb(uint8_t *cmd)
{
  // Enqueue the message to switch context
  RTLSMaster_enqueueMsg(RTLS_MASTER_RTLS_MSG_EVT, SUCCESS, cmd);
}

/*********************************************************************
*********************************************************************/


/*********************************************************************
 * EXTERN FUNCTIONS
 */
extern void AssertHandler(uint8 assertCause, uint8 assertSubcause);

/*********************************************************************
 * PROFILE CALLBACKS
 */

// Central GAPRole Callbacks
static gapCentralRoleCB_t RTLSMaster_roleCB =
{
  RTLSMaster_eventCB     // GAPRole Event Callback
};

// Bond Manager Callbacks
static gapBondCBs_t RTLSMaster_bondCB =
{
  RTLSMaster_passcodeCB, // Passcode callback
  RTLSMaster_pairStateCB // Pairing / Bonding state Callback
};

/*********************************************************************
 * PUBLIC FUNCTIONS
 */


/*********************************************************************
 * @fn      RTLSMaster_createTask
 *
 * @brief   Task creation function for the Simple Central.
 *
 * @param   none
 *
 * @return  none
 */

void RTLSMaster_createTask(void)
{
  Task_Params taskParams;

  // Configure task
  Task_Params_init(&taskParams);
  taskParams.stack = rtlsMasterTaskStack;
  taskParams.stackSize = RTLS_MASTER_TASK_STACK_SIZE;
  taskParams.priority = RTLS_MASTER_TASK_PRIORITY;

  Task_construct(&rtlsMasterTask, RTLSMaster_taskFxn, &taskParams, NULL);
}

/*********************************************************************
 * @fn      RTLSPassive_processRtlsPassiveMsg
 *
 * @brief   General handling of application events
 *
 * @param   pMsg - a pointer to the message
 *
 * @return  none
 */
static void RTLSPassive_processRtlsPassiveMsg(uint8_t *pMsg)
{
  rtlsPassiveEvt_t *pEvt = (rtlsPassiveEvt_t *)pMsg;
  volatile uint32_t keyHwi;
  
  switch(pEvt->event)
  {
    case RTLS_PASSIVE_RTLS_CTRL_EVT:
    {
      RTLSPassive_processRtlsCtrlMsg((uint8_t *)pEvt->pData);
    }
    break;

    case RTLS_PASSIVE_CM_EVT:
    {
      RTLSPassive_processCmMsg((uint8_t *)pEvt->pData);
    }
    break;

    default:
      break;
  }

  keyHwi = Hwi_disable();
  free(pEvt->pData);
  Hwi_restore(keyHwi);
}

/*********************************************************************
 * @fn      RTLSPassive_processRtlsCtrlMsg
 *
 * @brief   Handle processing messages from RTLS Control
 *
 * @param   pMsg - a pointer to the message
 *
 * @return  none
 */
static void RTLSPassive_processRtlsCtrlMsg(uint8_t *pMsg)
{
  rtlsCtrlReq_t *pReq = (rtlsCtrlReq_t *)pMsg;
  volatile uint32_t keyHwi;

  switch(pReq->reqOp)
  {
    case RTLS_REQ_ENABLE_SYNC:
    {
      RTLSPassive_enableRtlsSync(*pReq->pData);
    }
    break;

    case RTLS_REQ_CONN:
    {
      RTLSPassive_cmStartReq(pReq->pData);
    }
    break;

    case RTLS_REQ_TERMINATE_LINK:
    {
      RTLSPassive_terminateLinkReq();
    }
    break;

    default:
      break;
  }

  keyHwi = Hwi_disable();
  free(pReq->pData);
  Hwi_restore(keyHwi);
}

/*********************************************************************
 * @fn      RTLSPassive_processCmMsg
 *
 * @brief   Handle processing messages from Connection Monitor
 *
 * @param   pMsg - a pointer to the message
 *
 * @return  none
 */
static void RTLSPassive_processCmMsg(uint8_t *pMsg)
{
  cmEvt_t *pEvt = (cmEvt_t *)pMsg;
  volatile uint32_t keyHwi;
  
  switch(pEvt->event)
  {
    case CM_MONITOR_STATE_CHANGED_EVT:
    {
      RTLSPassive_monitorStateChangeEvt(*pEvt->pData);
    }
    break;

    case CM_PACKET_RECEIVED_EVT:
    {
      RTLSPassive_monitorIndicationEvt(pEvt->pData);
    }
    break;

    case CM_CONN_EVT_COMPLETE_EVT:
    {
      RTLSPassive_monitorCompleteEvt(pEvt->pData);
    }
    break;

    default:
      break;
  }

  keyHwi = Hwi_disable();
  free(pEvt->pData);
  Hwi_restore(keyHwi);
}

/*********************************************************************
 * @fn      RTLSPassive_enableRtlsSync
 *
 * @brief   Enable RTLS synchronization
 *
 * @param   enable - enable/disable sync
 *
 * @return  none
 */
static void RTLSPassive_enableRtlsSync(uint8_t enable)
{
  if (enable == RTLS_TRUE)
  {
    gRtlsSyncEnabled = RTLS_TRUE;
  }
  else
  {
    gRtlsSyncEnabled = RTLS_FALSE;
  }
}

/*********************************************************************
 * @fn      RTLSPassive_cmStartReq
 *
 * @brief   Start Monitoring a BLE connection
 *
 * @param   pConnInfo - BLE connection parameters
 *
 * @return  none
 */
static void RTLSPassive_cmStartReq(uint8_t *pConnInfo)
{
  bleConnInfo_t *pBleConnInfo = (bleConnInfo_t *)pConnInfo;

  // We currently support only 1 session
  if (gCmSessionId != CM_INVALID_SESSION_ID)
  {
    ubCM_stop(gCmSessionId);
  }

  // Mark that monitor is not currently tracking
  gMonitorTracking = RTLS_FALSE;

  // Kick CM
  gCmSessionId = ubCM_startExt(pBleConnInfo->accessAddr,
                               pBleConnInfo->connInterval,
                               pBleConnInfo->hopValue,
                               pBleConnInfo->currChan,
                               pBleConnInfo->chanMap,
                               pBleConnInfo->crcInit);
}

/*********************************************************************
 * @fn      RTLSPassive_terminateLinkReq
 *
 * @brief   Stop Monitoring a BLE connection
 *
 * @return  none
 */
static void RTLSPassive_terminateLinkReq(void)
{
  ubCM_stop(gCmSessionId);
  ugap_monitorStop();

  gCmSessionId = CM_INVALID_SESSION_ID;
  gRtlsSyncEnabled = RTLS_FALSE;
  gMonitorTracking = RTLS_FALSE;

  // Link terminated
  RTLSCtrl_connResultEvt(RTLS_LINK_TERMINATED);
}

/*********************************************************************
 * @fn      RTLSPassive_monitorIndicationEvt
 *
 * @brief   This function will be called for each BLE packet received
 *
 * @param   pData - Packet payload
 *
 * @return  none
 */
static void RTLSPassive_monitorIndicationEvt(uint8_t *pData)
{
}

/*********************************************************************
 * @fn      RTLSPassive_monitorCompleteEvt
 *
 * @brief   A single connection event has ended
 *
 * @param   pData - Session Id and Status of the session
 *
 * @return  none
 */
static void RTLSPassive_monitorCompleteEvt(uint8_t *pData)
{
  monitorCompleteEvt_t *pCompleteEvt = (monitorCompleteEvt_t *)pData;
  uint32_t nextStartTime;
  uint32_t currentTime;
  uint32_t nextEventTimeUs;
  int8_t slaveRssi;
  uint8_t channel;
  rtlsStatus_e status;
  port_key_t key;
  port_key_t key_h;

  // Convert CM Status to RTLS Status
  if (pCompleteEvt->status == CM_SUCCESS)
  {
    if (gMonitorTracking == RTLS_FALSE)
    {
      RTLSCtrl_connResultEvt(RTLS_SUCCESS);

      gMonitorTracking = RTLS_TRUE;
    }

    status = RTLS_SUCCESS;
  }
  else
  {
    status = RTLS_FAIL;
  }
  

  // The timing of the next event is critical
  // Enter CS
  key_h = port_enterCS_HW();
  key = port_enterCS_SW();

   // Set up the next monitor session
  (void)ubCM_start(ubCM_findNextPriorityEvt());


  if (gRtlsSyncEnabled == RTLS_TRUE)
  {
    // Get the next start time
    nextStartTime = ubCMConnInfo.ArrayOfConnInfo[pCompleteEvt->sessionId - 1].nextStartTime;

    currentTime = RF_getCurrentTime();
    nextEventTimeUs = RF_convertRatTicksToUs(nextStartTime - currentTime);

    // We are interested in the slave RSSI and channel
    slaveRssi = (int8_t)ubCMConnInfo.ArrayOfConnInfo[pCompleteEvt->sessionId - 1].rssiSlave;
    channel = (uint8_t)ubCMConnInfo.ArrayOfConnInfo[pCompleteEvt->sessionId - 1].currentChan;

    RTLSCtrl_syncEventNotify(status, nextEventTimeUs, slaveRssi, channel);
  }

  // Exit CS
  port_exitCS_SW(key);
  port_exitCS_HW(key_h);
}

/*********************************************************************
 * @fn      RTLSPassive_monitorStateChangeEvt
 *
 * @brief   This function will be called for each BLE CM state change
 *
 * @param   newState - The new state
 *
 * @return  none
 */
static void RTLSPassive_monitorStateChangeEvt(ugapMonitorState_t newState)
{
  switch (newState)
  {
    case UGAP_MONITOR_STATE_INITIALIZED:
    {

    }
    break;

    case UGAP_MONITOR_STATE_IDLE:
    {

    }
    break;

    case UGAP_MONITOR_STATE_MONITORING:
    {

    }
    break;

    default:
      break;
  }
}


/*********************************************************************
 *  @fn      RTLSPassive_init
 *
 *  @brief   Called during initialization and contains application
 *           specific initialization (ie. hardware initialization/setup,
 *           table initialization, power up notification, etc), and
 *           profile initialization/setup.
 *
 *  @param   None
 *
 *  @return  None
 */
void RTLSPassive_init(void)
{
  Task_Params ucaTaskParams;

  // Create an RTOS event used to wake up this application to process events.
  syncAppEvent = Event_create(NULL, NULL);

  // Create an RTOS queue for message from profile to be sent to app.
  appMsgQueue = Util_constructQueue(&appMsg);

  // Configure App task
  Task_Params_init(&ucaTaskParams);
  ucaTaskParams.stack = ucaTaskStack;
  ucaTaskParams.stackSize = UCA_TASK_STACK_SIZE;
  ucaTaskParams.priority = UCA_TASK_PRIORITY;
  Task_construct(&ucaTask, RTLSPassive_taskFxn, &ucaTaskParams, NULL);
}

/*********************************************************************
 * @fn      RTLSPassive_taskFxn
 *
 * @brief   Main CM application RTOS task loop, handles new CM command requests
 *          and continous monitor calls.
 *
 * @param   a0 - Standard TI RTOS taskFxn arguments.
 * @param   a1 -
 *
 * @return  none
 */
static void RTLSPassive_taskFxn(UArg a0, UArg a1)
{
  for(;;)
  {
    volatile uint32 keyHwi;
    uint32_t events = Event_pend(syncAppEvent, Event_Id_NONE, UCA_ALL_EVENTS, BIOS_WAIT_FOREVER);

    // If RTOS queue is not empty, process app message.
    while (!Queue_empty(appMsgQueue))
    {
      keyHwi = Hwi_disable();
      rtlsPassiveEvt_t *pMsg = (rtlsPassiveEvt_t *)Util_dequeueMsg(appMsgQueue);
      Hwi_restore(keyHwi);

      if (pMsg)
      {
        // Process message.
        RTLSPassive_processRtlsPassiveMsg((uint8_t *)pMsg);

        keyHwi = Hwi_disable();
        free(pMsg);
        Hwi_restore(keyHwi);
      }
    }
  }
}

/*********************************************************************
 * @fn      RTLSPassive_rtlsCtrlMsgCb
 *
 * @brief   Callback given to RTLS Control
 *
 * @param  cmd - the command to be enqueued
 *
 * @return  none
 */
void RTLSPassive_rtlsCtrlMsgCb(uint8_t *pCmd)
{
  // Enqueue the message to switch context
  RTLSPassive_enqueueAppMsg(RTLS_PASSIVE_RTLS_CTRL_EVT, (uint8_t *)pCmd);
}

/*********************************************************************
 * @fn      RTLSPassive_cmCb
 *
 * @brief   Callback given to Connection Monitor
 *
 * @param   pCmd - the command to be enqueued
 *
 * @return  none
 */
void RTLSPassive_cmCb(uint8_t *pCmd)
{
  // Enqueue the message to switch context
  RTLSPassive_enqueueAppMsg(RTLS_PASSIVE_CM_EVT, (uint8_t *)pCmd);
}

/*********************************************************************
 * @fn      RTLSPassive_enqueueMsg
 *
 * @design /ref 159098678
 *
 * @brief   Enqueue a message to RTLS Passive task function
 *
 * @param   pMsg - pointer to a message
 * @param   eventId - needed to send message to correct handler
 *
 * @return  none
 */
void RTLSPassive_enqueueAppMsg(uint16_t eventId, uint8_t *pMsg)
{
  rtlsPassiveEvt_t *qMsg;
  volatile uint32 keyHwi;

  keyHwi = Hwi_disable();
  if((qMsg = (rtlsPassiveEvt_t *)malloc(sizeof(rtlsPassiveEvt_t))))
  {
    qMsg->event = eventId;
    qMsg->pData = pMsg;

    Util_enqueueMsg(appMsgQueue, syncAppEvent, (uint8_t *)qMsg);
  }
  else
  {
    // Free pMsg if we failed to enqueue
    if (pMsg)
    {
      free(pMsg);
    }
  }
  Hwi_restore(keyHwi);
}

/*********************************************************************
 Setup and Run Required High Priority RTOS Task for ubStack functionality
 *********************************************************************/

/*********************************************************************
 * @fn      RTLSPassive_stack_init
 *
 * @brief   Initialize ubtTask.
 *
 * @param   none
 *
 * @return  none
 */
void RTLSPassive_stack_init(void)
{
  Task_Params stackTaskParams;

  // Configure Stack task
  Task_Params_init(&stackTaskParams);
  stackTaskParams.stack = ubtTaskStack;
  stackTaskParams.stackSize = UBT_TASK_STACK_SIZE;
  stackTaskParams.priority = UBT_TASK_PRIORITY;
  Task_construct(&ubtTask, ubStack_taskFxn, &stackTaskParams, NULL);
}

/*********************************************************************
 * @fn      ubStack_taskFxn
 *
 * @brief   Stack task entry point for the micro_ble.
 *
 * @param   none
 *
 * @return  none
 */
static void ubStack_taskFxn(UArg a0, UArg a1)
{
  volatile uint32 keyHwi;

  // Create an RTOS event used to wake up this application to process events.
  syncStackEvent = Event_create(NULL, NULL);

  // Create an RTOS queue for message from profile to be sent to app.
  stackMsgQueue = Util_constructQueue(&stackMsg);

  uble_stackInit(UBLE_ADDRTYPE_PUBLIC, NULL, uBLEStack_eventProxy,
                 RF_TIME_CRITICAL);

  ubCm_init(RTLSPassive_cmCb);

  for (;;)
  {
    // Waits for an event to be posted associated with the calling thread.
    // Note that an event associated with a thread is posted when a
    // message is queued to the message receive queue of the thread
    Event_pend(syncStackEvent, Event_Id_NONE, UBT_QUEUE_EVT, BIOS_WAIT_FOREVER);

    // If RTOS queue is not empty, process app message.
    while (!Queue_empty(stackMsgQueue))
    {
      ubtEvt_t *pMsg;

      // malloc() is not thread safe. Must disable HWI.
      keyHwi = Hwi_disable();
      pMsg = (ubtEvt_t *) Util_dequeueMsg(stackMsgQueue);
      Hwi_restore(keyHwi);

      if (pMsg)
      {
        // Only expects UBT_EVT_MICROBLESTACK from ubStack.
        if (pMsg->event == RTLS_PASSIVE_USTACK_EVT)
        {
          uble_processMsg();
        }

        // free() is not thread safe. Must disable HWI.
        keyHwi = Hwi_disable();

        // Free the space from the message.
        free(pMsg);
        Hwi_restore(keyHwi);
      }
    }
  }
}

/*********************************************************************
 * @fn      uBLEStack_eventProxy
 *
 * @brief   Required event_post for ubStack operation.
 *
 */
void uBLEStack_eventProxy(void)
{
  if (RTLSPassive_enqueueStackMsg(RTLS_PASSIVE_USTACK_EVT, 0) == FALSE)
  {
    // post event anyway when heap is out to avoid malloc error
    Event_post(syncStackEvent, UTIL_QUEUE_EVENT_ID);
  }
}

/*********************************************************************
 * @fn      RTLSPassive_enqueueMsg
 *
 * @brief   Creates a message and puts the message in RTOS queue.
 *
 * @param   event - message event.
 * @param   data - message data.
 *
 * @return  TRUE or FALSE
 */
static bStatus_t RTLSPassive_enqueueStackMsg(uint16 event, uint8 data)
{
  volatile uint32 keyHwi;
  ubtEvt_t *pMsg;
  uint8_t status = FALSE;

  // malloc() is not thread safe. Must disable HWI.
  keyHwi = Hwi_disable();

  // Create dynamic pointer to message.
  pMsg = (ubtEvt_t*) malloc(sizeof(ubtEvt_t));
  if (pMsg != NULL)
  {
    pMsg->event = event;
    pMsg->data = data;

    // Enqueue the message.
    status = Util_enqueueMsg(stackMsgQueue, syncStackEvent, (uint8*) pMsg);
  }
  Hwi_restore(keyHwi);
  return status;
}

/*********************************************************************
 *********************************************************************/
