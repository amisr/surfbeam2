# SurfBeam2 #
A package for polling and parsing the status of a ViaSat SurfBeam 2 Satellite Modem.

### Installation ###

Clone this repo and install using:

    pip install .

from the root directory of the repository.

### Usage ###

There are 2 ways to use this package,
1) from a python shell, or
2) from the command line.

#### Python Shell ####

    from surfbeam2 import PollSurfBeam2
    address = '192.168.100.1'
    timeout = 5
    retrytime = 1
    psb = PollSurfBeam2(address,timeout=timeout,retrytime=retrytime)
    psb.poll()
    print(psb.status)

#### Command Line ####
Installation results in a `pollsurfbeam2` command line tool. Example usage:

    $ pollsurfbeam2 192.168.100.1

which will poll the modem with IP address `192.168.100.1`. By default, the
program will try to poll the modem 3 times waiting with a timeout of 5
seconds and a retry time of 1 second. Check out the help to see how to
modify the `timeout` and `retrytime`:

    $ pollsurfbeam2 -h
    usage: pollsurfbeam2 [-h] [-t TIMEOUT] [-r RETRYTIME] address
    
    Poll a ViaSat SurfBeam2 Satellite Modem for status.
    
    positional arguments:
      address               The IP address of the modem.
    
    optional arguments:
      -h, --help            show this help message and exit
      -t TIMEOUT, --timeout TIMEOUT
                            Poll timeout. Time to wait for response to request.
      -r RETRYTIME, --retrytime RETRYTIME
                            Retry timeout. Time to wait between retries.

