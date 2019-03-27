#!/usr/bin/env python
################################################################################
#
#    Title: modemview.py
#
#    Author: asreimer
#
#    Description: This script displays the results of a PollSurfBeam2 class 
#                 poll in a curses display.
#
################################################################################


import re
import os
import sys
import curses
import curses.ascii
from argparse import ArgumentParser

from surfbeam2 import PollSurfBeam2


# helper function to remove html tags from some of the poll results
def remove_tags(text):
    TAG_RE = re.compile(r'<[^>]+>')
    return TAG_RE.sub('', text)


# class for curses display
class modemview():
    def __init__(self,stdscr,address,timeout,retrytime):
        psb = PollSurfBeam2(address, timeout=timeout, retrytime=retrytime)

        self.psb = psb
        self.stdscr = stdscr


    def run(self):
        self.stdscr.timeout(2000)
        self.update()

        while True:
            c = self.stdscr.getch()
            if c==-1:
                self.update()
            elif c==curses.ascii.ESC:
                break

        self.stdscr.erase()


    def update(self):
        self.stdscr.addstr(1,1,'*')
        self.stdscr.move(curses.LINES-2,curses.COLS-2)
        self.stdscr.refresh()

        try:
            self.psb.poll()
            status = self.psb.status
        except: 
            status = None 
        
        self.stdscr.addstr(1,1,' ')
        self.stdscr.move(curses.LINES-2,curses.COLS-2)
        self.stdscr.refresh()

        self.stdscr.erase()
        self.stdscr.border()


        self.stdscr.addstr(1,2,'ViaSat SurfBeam2 Modem Status: %s' % (self.psb.address))
        # modem status
        if status['modem']['poll_results'] == 'Success':
            modem = status['modem']
        else:
            modem = {'utStatus': 'err', 'uptime':'err', 'esNo':'err',
                     'rxPower':'err', 'oduTelemetry':'err', 'oduCbla':'err',
                     'oduCblr':'err', 'ipAddr':'err', 'macAddr':'err',
                     'swVer':'err', 'hwVer':'err', 'utSerialNum':'err',
                     'partNum':'err', 'iflType':'err', 'txPkts':'err',
                     'txBytes':'err', 'rxPkts':'err', 'rxBytes':'err',
                     'losCount':'err', 'cspStatus':'err', 'cspHealth':'err',
                     'cspFlPacketsLost':'err', 'cspRlPacketsLost':'err',
                     'cspPageLoad':'err'}

        col1 = 4
        col2 = 50
        self.stdscr.addstr( 3, col1-2,'MODEM')
        self.stdscr.addstr( 5, col1-1,'GENERAL')
        self.stdscr.addstr( 6, col1,'Status:               %s' % (modem['utStatus']))
        self.stdscr.addstr( 6, col2,'Online Time:       %s' % (modem['uptime']))
        self.stdscr.addstr( 7, col1,'Rx Power:             %s dBm' % (modem['rxPower']))
        self.stdscr.addstr( 7, col2,'Rx SNR:            %s dB' % (modem['esNo']))
        self.stdscr.addstr( 8, col1,'Cable Resistance:     %s Ohm' % (modem['oduCblr']))
        self.stdscr.addstr( 8, col2,'Cable Attenuation: %s dB' % (modem['oduCbla']))
        self.stdscr.addstr( 9, col1,'ODU Telemetry Status: %s' % (modem['oduTelemetry']))

        self.stdscr.addstr(11, col1-1,'IDENTIFICATION')
        self.stdscr.addstr(12, col1,'IP Address:       %s' % (modem['ipAddr']))
        self.stdscr.addstr(12, col2,'MAC Address:      %s' % (modem['macAddr']))
        self.stdscr.addstr(13, col1,'Software Version: %s' % (modem['swVer']))
        self.stdscr.addstr(13, col2,'Hardware Version: %s' % (modem['hwVer']))
        self.stdscr.addstr(14, col1,'Serial Number:    %s' % (modem['utSerialNum']))
        self.stdscr.addstr(14, col2,'Part Number:      %s' % (modem['partNum']))
        self.stdscr.addstr(15, col1,'IFL Type:         %s' % (modem['iflType']))
        #self.stdscr.addstr(15, col2,'BDT Version: %s' % (modem['']))

        self.stdscr.addstr(17, col1-1,'ETHERNET INTERFACE STATISTICS')
        self.stdscr.addstr(18, col1,'Transmitted Packets: %s' % (modem['txPkts']))
        self.stdscr.addstr(18, col2,'Transmitted Bytes: %s' % (modem['txBytes']))
        self.stdscr.addstr(19, col1,'Received Packets:    %s' % (modem['rxPkts']))
        self.stdscr.addstr(19, col2,'Received Bytes:    %s' % (modem['rxBytes']))
        self.stdscr.addstr(20, col1,'Loss of Sync Count:  %s' % (modem['losCount']))

        self.stdscr.addstr(22, col1-1,'CLIENT-SIDE PROXY STATISTICS')
        self.stdscr.addstr(23, col1,'Status:                     %s' % (remove_tags(modem['cspStatus'])))
        self.stdscr.addstr(23, col2,'Health:                     %s' % (remove_tags(modem['cspHealth'])))
        self.stdscr.addstr(24, col1,'FL Packets Lost Percentage: %s' % (modem['cspFlPacketsLost']))
        self.stdscr.addstr(24, col2,'RL Packets Lost Percentage: %s' % (modem['cspRlPacketsLost']))
        self.stdscr.addstr(25, col1,'Last Page Load Duration:    %s' % (modem['cspPageLoad']))


        # tria status
        if status['tria']['poll_results'] == 'Success':
            tria = status['tria']
        else:
            tria = {'oduFwVer': 'err', 'oduBlueOut': 'err', 'oduSn': 'err',
                    'oduTemperature': 'err', 'oduTxIfPwr': 'err', 'oduBrownOut': 'err',
                    'oduTxBand': 'err', 'oduTxRfPwr': 'err'}

        self.stdscr.addstr(28, col1-2,'TRIA')
        self.stdscr.addstr(30, col1-1,'GENERAL')
        self.stdscr.addstr(31, col1,'Tx IF Power: %s dBm' % (tria['oduTxIfPwr']))
        self.stdscr.addstr(31, col2,'Tx RF Power: %s dBm' % (tria['oduTxRfPwr']))
        self.stdscr.addstr(32, col1,'Temperature: %s C' % (tria['oduTemperature']))

        self.stdscr.addstr(34, col1-1,'DIAGNOSTICS')
        self.stdscr.addstr(35, col1,'Brownout Mode Enabled: %s' % (tria['oduBrownOut']))
        self.stdscr.addstr(35, col2,'Blueout Mode Enabled: %s' % (tria['oduBlueOut']))
        self.stdscr.addstr(36, col1,'TRIA Serial Number:    %s' % (tria['oduSn']))
        self.stdscr.addstr(36, col2,'TRIA Firmware Number: %s' % (tria['oduFwVer']))

        # NOT Currently supported.
        # self.stdscr.addstr(37, col1-1,'MODULE STATUS')
        # self.stdscr.addstr(38, col1,'Bullfrog VG: %s' % (tria['txPkts']))
        # self.stdscr.addstr(38, col2,'Transmitted Bytes: %s' % (tria['txBytes']))
        # self.stdscr.addstr(39, col1,'Received Packets:    %s' % (tria['rxPkts']))
        # self.stdscr.addstr(39, col2,'Received Bytes:    %s' % (tria['rxBytes']))
        # self.stdscr.addstr(40, col1,'Received Packets:    %s' % (tria['rxPkts']))
        # self.stdscr.addstr(40, col2,'Received Bytes:    %s' % (tria['rxBytes']))
        # self.stdscr.addstr(41, col1,'Loss of Sync Count:  %s' % (tria['losCount']))

        self.stdscr.move(curses.LINES-2,curses.COLS-2)
        self.stdscr.refresh()

        return


# provides command line interface
def main():
    # Set up some argparse stuff
    parser = ArgumentParser(description='Poll a ViaSat SurfBeam2 Satellite Modem for status.')
    parser.add_argument("address", help="The IP address of the modem.", default='192.168.100.1')
    parser.add_argument("-t", "--timeout", help="Poll timeout. Time to wait for response to request.", type=float, default=1.,required=False)
    parser.add_argument("-r", "--retrytime", help="Retry timeout. Time to wait between retries.", type=float, default=1.,required=False)
    # Get arguments. Convert argparser Namespace class to dictionary
    args = vars(parser.parse_args())
    
    address = args['address']
    timeout = args['timeout']
    retrytime = args['retrytime']

    curses.wrapper(start_curses,address,timeout,retrytime)


# helper function for starting curses
def start_curses(stdscr,address,timeout,retrytime):
    modemview(stdscr,address,timeout,retrytime).run()


if __name__ == '__main__':
    main()