#!/usr/bin/env python
################################################################################
#
#    Title: test.py
#
#    Author: asreimer
#
#    Description: This tests the PollSurfBeam class
#
################################################################################

import time
import requests
import unittest
try:
    from unittest import mock
except ImportError:
    import mock
from PollSurfBeam2 import PollSurfBeam2


# we need to mock the requests.get call in PollSurfBeam
def mocked_requests_get(*args,**kwargs):
    MODEM_URL = 'http://192.168.100.1/index.cgi?page=modemStatusData'
    TRIA_URL = 'http://192.168.100.1/index.cgi?page=triaStatusData'
    MOCK_MODEM_RESPONSE = """0.0.0.0##00:00:00:00:00:00##UT_2.2.4.11.0##UT_7 P3_V1##Online##203,745##36,265,784##195,576##24,234,623##000:04:30:25##15##2.6##20%##283714481586##-54.8##30%##0.5##0%##Active##23.0##100%##Single##1113450014##images/Modem_Status_005_Online.png##/images/Satellite_Status_Purple.png##0##<p style="color:green">Connected</p>##<p style="color:green">Good</p>##0.00%##0.00%##0.00s##0%##625000################4####0%##0##<p style="color:red">Disconnected</p>##0.0 GB##Xplor##FIXED##0########################################"""
    MOCK_TRIA_RESPONSE = """images/green_check_small_002.png##images/green_check_small_002.png##images/green_check_small_002.png##images/green_check_small_002.png##Reduced power##Right##WIN##-12.7##images/green_check_small_002.png##SINGLE##-10##images/green_check_small_002.png##images/green_check_small_002.png##images/green_check_small_002.png##0.5##16116##1020149622##34.3##images/green_check_small_002.png##20##images/green_check_small_002.png##19##9##18##18.33##89%##77%##No##No##/images/Satellite_Status_Purple.png########################################################################################################"""

    class MockResponse():
        def __init__(self, text, status_code):
            self.text = text
            self.status_code = status_code

    if args[0] == MODEM_URL:
        return MockResponse(MOCK_MODEM_RESPONSE, 200)
    elif args[0] == TRIA_URL:
        return MockResponse(MOCK_TRIA_RESPONSE, 200)

    return MockResponse(None, 404)


# run the PollSurfBeam unit test
class TestPollSurfBeam2(unittest.TestCase):

    # We patch 'requests.get' with our own method. The mock object is passed in to our test case method.
    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_modem_status(self, mock_get):
        expected = {'modem': {'oduCblr': '0.5', 'bdtVersion': '4', 'oduCbla': '23.0', 'rxBytes': '24,234,623', 'utStatus': 'Online', 'cspFlPacketsLost': '0.00%', 'uptime': '000:04:30:25', 'cspPageLoad': '0.00s', 'esNo': '2.6', 'cspStatus': '<p style="color:green">Connected</p>', 'cspHealth': '<p style="color:green">Good</p>', 'sdConnStatus': '<p style="color:red">Disconnected</p>', 'rxPower': '-54.8', 'cspRlPacketsLost': '0.00%', 'ipAddr': '0.0.0.0', 'txPkts': '203,745', 'poll_results': 'Success', 'txBytes': '36,265,784', 'partNum': '1113450014', 'oduTelemetry': 'Active', 'swVer': 'UT_2.2.4.11.0', 'losCount': '15', 'rxPkts': '195,576', 'iflType': 'Single', 'sdSize': '0.0 GB'}, 'tria': {'oduCblr': '0.5', 'oduHpaType': 'WIN', 'oduFwVer': '18.33', 'oduBlueOut': 'No', 'oduRxBand': '19', 'oduThermMode': '9', 'oduPol': 'Right', 'oduSn': '1020149622', 'oduThermLvl': 'Reduced power', 'oduTemperature': '-10', 'poll_results': 'Success', 'oduHours': '16116', 'oduTxIfPwr': '-12.7', 'oduBrownOut': 'No', 'oduTxBand': '20', 'oduCableType': 'SINGLE', 'oduPolSwCnt': '18', 'oduTxRfPwr': '34.3'}}

        psb = PollSurfBeam2('192.168.100.1')
        psb.poll()
        self.assertEqual(psb.status,expected)


if __name__ == '__main__':
    unittest.main()