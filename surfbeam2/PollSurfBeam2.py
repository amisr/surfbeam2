#!/usr/bin/env python
################################################################################
#
#    Title: PollSurfBeam.py
#
#    Author: asreimer
#
#    Description: This class was built to poll the status pages of a ViaSat
#                 SurfBeam 2 Satellite Modem. The modem is accessed via an IP
#                 address of 192.168.100.1. This script gets both the TRIA and
#                 modem status.
#
#                 This script assumes modem software version: UT_2.2.4.11.0
#
################################################################################

import time
import requests

class PollSurfBeam2():

    MODEM_URL = 'http://%s/index.cgi?page=modemStatusData'
    TRIA_URL = 'http://%s/index.cgi?page=triaStatusData'

    def __init__(self,address,timeout=5,retrytime=1):
        # need to make a call to the SurfBeam2 CGI API
        self.query_modem_url = self.MODEM_URL % (address)
        self.query_tria_url = self.TRIA_URL % (address)

        # initialize some output params
        self.modem_status_raw = None
        self.tria_status_raw = None
        self.status = dict()
        self.status['modem'] = dict()
        self.status['tria'] = dict()
        self.timeout = timeout
        self.retrytime = retrytime


    # poll the modem for modem and tria status then parse the raw response
    def poll(self):
        # poll modem status
        num_tries = 0
        status = 0
        while num_tries < 3:
            try:
                r = requests.get(self.query_modem_url, timeout=self.timeout)
                status = r.status_code
            except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
                status = 0
            if status == 200:
                break
            num_tries += 1
            time.sleep(self.retrytime)
        if status == 200:
            self.modem_status_raw = r.text
        else:
            self.modem_status_raw = None

        # poll tria status
        num_tries = 0
        status = 0
        while num_tries < 3:
            try:
                r = requests.get(self.query_tria_url, timeout=self.timeout)
                status = r.status_code
            except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
                status = 0
            if status == 200:
                break
            num_tries += 1
            time.sleep(self.retrytime)
        if status == 200:
            self.tria_status_raw = r.text
        else:
            self.tria_status_raw = None
        
        self.parse_modem_status()
        self.parse_tria_status()


    def parse_modem_status(self):
        # replicates some of the functionality in "scripts.js" in the
        # "decodeAndUpdateModemStatus()" function.
        if self.modem_status_raw is None:
            self.status['modem']['poll_results'] = 'Fail'
            return
        else:
            self.status['modem']['poll_results'] = 'Success'

        temp = self.modem_status_raw.encode('utf-8')
        params = temp.split("##")

        self.status['modem']['ipAddr'] = params[0]
        self.status['modem']['swVer'] = params[2]
        self.status['modem']['utStatus'] = params[4]
        self.status['modem']['txPkts'] = params[5]
        self.status['modem']['txBytes'] = params[6]
        self.status['modem']['rxPkts'] = params[7]
        self.status['modem']['rxBytes'] = params[8]
        self.status['modem']['uptime'] = params[9]
        self.status['modem']['losCount'] = params[10]
        self.status['modem']['esNo'] = params[11]
        self.status['modem']['rxPower'] = params[14]
        self.status['modem']['oduCblr'] = params[16]
        self.status['modem']['oduTelemetry'] = params[18]
        self.status['modem']['oduCbla'] = params[19]
        self.status['modem']['iflType'] = params[21]
        self.status['modem']['partNum'] = params[22]
        self.status['modem']['cspStatus'] = params[26]
        self.status['modem']['cspHealth'] = params[27]
        self.status['modem']['cspFlPacketsLost'] = params[28]
        self.status['modem']['cspRlPacketsLost'] = params[29]
        self.status['modem']['cspPageLoad'] = params[30]
        self.status['modem']['bdtVersion'] = params[40]
        self.status['modem']['sdConnStatus'] = params[44] # AKA Storage Status
        self.status['modem']['sdSize'] = params[45] # AKA Storage Size 


    def parse_tria_status(self):
        # replicates some of the functionality in "scripts.js" in the
        # "decodeAndUpdateTriaStatus()" function.
        if self.tria_status_raw is None:
            self.status['tria']['poll_results'] = 'Fail'
            return
        else:
            self.status['tria']['poll_results'] = 'Success'

        temp = self.tria_status_raw.encode('utf-8')
        params = temp.split("##")

        self.status['tria']['oduThermLvl'] = params[4]
        self.status['tria']['oduPol'] = params[5]
        self.status['tria']['oduHpaType'] = params[6]
        self.status['tria']['oduTxIfPwr'] = params[7]
        self.status['tria']['oduCableType'] = params[9]
        self.status['tria']['oduTemperature'] = params[10]
        self.status['tria']['oduCblr'] = params[14]
        self.status['tria']['oduHours'] = params[15]
        self.status['tria']['oduSn'] = params[16]
        self.status['tria']['oduTxRfPwr'] = params[17]
        self.status['tria']['oduTxBand'] = params[19]
        self.status['tria']['oduRxBand'] = params[21]
        self.status['tria']['oduThermMode'] = params[22]
        self.status['tria']['oduPolSwCnt'] = params[23]
        self.status['tria']['oduFwVer'] = params[24]
        self.status['tria']['oduBrownOut'] = params[27]
        self.status['tria']['oduBlueOut'] = params[28]


def main():
    import sys
    psb = PollSurfBeam2(sys.argv[1])
    psb.poll()
    print(psb.status)


if __name__ == '__main__':
	main()