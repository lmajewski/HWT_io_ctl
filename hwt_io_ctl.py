#! /usr/bin/env python
"""
Control GPIO connected via a FTDI FT232R module using pylibftdi

Copyright (c) 2014 Lukasz Majewski <l.majewski@samsung.com>
License: GPLv2+
"""
import argparse
from pylibftdi import BitBangDevice

def flash_forever(rate):
    "toggle bit zero at rate Hz"
    # put an LED with 1Kohm or similar series resistor
    # on D0 pin
    with BitBangDevice() as bb:
	while True:
	    time.sleep(1.0 / (2 * rate))
	    bb.port ^= 0x08


def main():
    if len(sys.argv) > 1:
	rate = float(sys.argv[1])
	flash_forever(rate)
    else:
	flash_forever(1)


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description=
					 'HW test (HWT) PWR control (via FTDI232R)',
					 formatter_class=argparse.RawDescriptionHelpFormatter,
					 epilog='''\
  ----------------------
  FTDI232RL device pins:
  ----------------------
  D0         TXD
  D1         RXD
  D2         RTS#
  D3         CTS#
  D4         DTR#
  D5         DSR#
  D6         DCD#
  D7         RI#''')
	parser.add_argument('-d', '--device', required = True,
			    help='FT232 Device to connect')
	parser.add_argument('-p', '--pin', required = True,
			    help='Pin to control - e.g. CTS')
	parser.add_argument('--state', required = True,
			    help='State - on/off')
	parser.add_argument('--debug',
			    action='store_true',
			    default=False,
			    dest='debug_en',
			    help='Enable printing debug information')

	args = parser.parse_args()

	if args.debug_en:
		print "HWT PWR control (FTDI based) - %s" % \
		    str(datetime.datetime.now())[:19]
