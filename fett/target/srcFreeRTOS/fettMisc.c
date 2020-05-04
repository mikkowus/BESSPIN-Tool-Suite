/*
Functions used for Misc implementation on FreeRTOS
*/

#include "fettFreeRTOS.h"

static uint8_t doEndFett = 0;
MessageBufferHandle_t globalMsgBuffer = NULL;

// Only printf while "ON"
void fettPrintf (const char * textToPrint, ...) {
    if (!doEndFett) {
        va_list args;
        va_start(args, textToPrint);
        vprintf(textToPrint, args);
        va_end(args);
    }
    return;
}

//turn off printing. and print >>>End of Fett<<<
void exitFett (uint8_t exitCode) {
    if (!doEndFett) {
        doEndFett = 1;
        printf ("EXIT: exiting FETT with code <%x>\r\n",exitCode);
        printf ("\r\n>>>End of Fett<<<\r\n");
    }
    return;
}

/*
--- This function is called by FreeRTOS_TCP_IP.c. This is a dirty implementation
 * Callback that provides the inputs necessary to generate a randomized TCP
 * Initial Sequence Number per RFC 6528.  THIS IS ONLY A DUMMY IMPLEMENTATION
 * THAT RETURNS A PSEUDO RANDOM NUMBER SO IS NOT INTENDED FOR USE IN PRODUCTION
 * SYSTEMS.
 */
uint32_t ulApplicationGetNextSequenceNumber(uint32_t ulSourceAddress,
                                            uint16_t usSourcePort,
                                            uint32_t ulDestinationAddress,
                                            uint16_t usDestinationPort)
{
    (void)ulSourceAddress;
    (void)usSourcePort;
    (void)ulDestinationAddress;
    (void)usDestinationPort;

    return uxRand();
}

/* This function sends some data to the message buffer */
uint8_t sendToMsgBuffer (void * xData, size_t xDataSize) {
    if (globalMsgBuffer == NULL) { //it was not created
        size_t msgBufSize = MSGBUF_SIZE;

        globalMsgBuffer = xMessageBufferCreate (msgBufSize);
        if (globalMsgBuffer == NULL) {
            fettPrintf ("(Error)~  sendToMsgBuffer: Create the global message buffer.\r\n");
            return uFALSE;
        }
    } //if it was not created

    size_t xBytesSent = xMessageBufferSend( globalMsgBuffer, xData, xDataSize, 0);
    if (xBytesSent != xDataSize) {
        fettPrintf ("(Error)~  sendToMsgBuffer: Send to the message buffer. [ret=%d]\r\n",xBytesSent);
        return uFALSE;
    }

    return uTRUE;
}

/* This function receives some data from the message buffer */
size_t recvFromMsgBuffer (void * xBuf, size_t xBufSize) {
    if (globalMsgBuffer == NULL) { //it was not created or received
        fettPrintf ("(Error)~  recvFromMsgBuffer: Message buffer to receive from.\r\n");
        return 0;
    }

    return xMessageBufferReceive( globalMsgBuffer, xBuf, xBufSize, 0); //No waiting; not used in flow control to be more generic
}


/*fake function because sometimes, a wolfssl functions calls it despite defining NO_FILESYSTEM.
In such a case, such culprit function should have a wrapper and the functionality implemented here */
void _open (const char * dump1, int dump2, ...) {
    (void) (dump1);
    (void) (dump2);
    fettPrintf ("FATAL ERROR: <_open> should never be called.\r\n");
    prEXIT(1);
}

/* Fake functions because time is needed for certificated expiry and beginning dates.
_gettimeofday appears to be called from time.h; also the XTIME function overrides the calls to time().
   This can be improved by being called to set at time of boot and then adding
   the tickCount (with an interrupt at tickCount overflow).
   Or even better, we can get the time from the network.
   It does not seem worth it to spend the time and do that for fett purposes */
void _gettimeofday (struct timeval *__p, void *__tz) {
    if (__tz != NULL) {
        fettPrintf("Warning: timezone pointer is not NULL in custom <gettimeofday>.\r\n");
    }
    //this is only temporary ---- will be changed!!
    if (__p == NULL) {
        fettPrintf ("<INVALID> No timeval allocated in <gettimeofday>.\r\n");
        prEXIT(1);
    }
    #ifdef FAKETIMEOFDAY
        __p->tv_sec = FAKETIMEOFDAY;
    #else
        fettPrintf ("<INVALID> [gettimeofday]: FAKETIMEOFDAY is not defined!\r\n");
        prEXIT(1);
    #endif
    __p->tv_usec = 0UL;
    return;
}

time_t XTIME(time_t *t) {
    (void) t;
    #ifdef FAKETIMEOFDAY
        return FAKETIMEOFDAY;
    #else
        fettPrintf ("<INVALID> [XTIME]: FAKETIMEOFDAY is not defined!\r\n");
        exitFett(2);
        return 0;
    #endif
}

/* Added as there is no such function in FreeRTOS. */
// type is not type anymore; it is the old size.
void *XREALLOC(void *p, size_t n, void* heap, int type)
{
    // This part is clean
    if (n == 0)
    {
       vPortFree (p);
       return NULL;
    }
    else if (p == NULL)
    {
       return pvPortMalloc (n);
    }

    //This has the dangerous part
    #if __riscv_xlen == 64
        unsigned int isItCustomCall = (heap != NULL) && ((intptr_t) heap == USE_FETT_REALLOC);
    #else
        unsigned int isItCustomCall = (heap != NULL) && ((int) heap == USE_FETT_REALLOC);
    #endif

    if (isItCustomCall == 0) { //super dangerous method
        fettPrintf ("Warning: XREALLOC <dangerously defined> is used.\r\n");
    }

    void *pvReturn = pvPortMalloc (n);
    if (pvReturn == NULL) {
        fettPrintf ("<INVALID> [XREALLOC]: Failed to malloc.");
        exitFett (2); //cannot use prEXIT because this function is non-void
        return NULL;
    }

    if (isItCustomCall == 0) { //super dangerous method
        memcpy (pvReturn, p, n); //This is dangerous because n might be > size(p) and may be in a bad memory region.
    } else { //the custom safe call
        memcpy (pvReturn, p, (size_t) type);
    }

    vPortFree (p);
    return pvReturn;
}

/* Added as no /dev/urandom to give the seed for RNG -- Not for REAL APPLICATIONS
   It is not integrated, so if needed, fett.py should create a header and fill it with seeds
*/
static uint8_t iSeed = 0; //start with the first one
int fett_wc_GenerateSeed(uint8_t* seed, uint8_t sz) {

#if defined (FETT_WC_SEEDS_LEN)
    uint8_t seedsArray [FETT_WC_SEEDS_LEN] = { FETT_WC_SEEDS };
    uint8_t seedOS = seedsArray[iSeed];
    memcpy (seed, &seedOS, sz);
    iSeed++; //next time, use next seed
    if (iSeed >= FETT_WC_SEEDS_LEN) {
        iSeed = 0;
    }
#else
    // Temporary implementation that doesn't depend on fett.py generating
    // FETT_WC_SEEDS_LEN and FETT_WC_SEEDS.  Obviously NOT for production use.
    uint8_t seedsArray [10] = { 4, 7, 234, 65, 23, 12, 78, 44, 98, 234 };
    uint8_t seedOS = seedsArray[iSeed];
    memcpy (seed, &seedOS, sz);
    iSeed++; //next time, use next seed
    if (iSeed >= 10) {
        iSeed = 0;
    }
#endif

    return 0;
}
