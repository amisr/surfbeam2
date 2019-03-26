#!/usr/bin/env python
################################################################################
#
#    Title: get_modem_status.py
#
#    Author: asreimer
#
#    Description: This script uses the PollSurfBeam2 class to poll the status
#                 pages of a ViaSat SurfBeam 2 Satellite Modem.
#
################################################################################


import os
import sys
from argparse import ArgumentParser
from surfbeam2 import PollSurfBeam2

def main():
    # Set up some argparse stuff
    parser = ArgumentParser(description='Poll a ViaSat SurfBeam2 Satellite Modem for status.')
    parser.add_argument("address", help="The IP address of the modem.", default='192.168.100.1')
    parser.add_argument("-t", "--timeout", help="Poll timeout. Time to wait for response to request.", type=float, default=5.,required=False)
    parser.add_argument("-r", "--retrytime", help="Retry timeout. Time to wait between retries.", type=float, default=1.,required=False)
    # Get arguments. Convert argparser Namespace class to dictionary
    args = vars(parser.parse_args())
    
    address = args['address']
    timeout = args['timeout']
    retrytime = args['retrytime']

    psb = PollSurfBeam2(address, timeout=timeout, retrytime=retrytime)
    psb.poll()
    print(psb.status)

if __name__ == '__main__':
    main()