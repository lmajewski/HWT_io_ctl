#! /usr/bin/env python
"""
Control GPIO connected via a FTDI FT232R module using pylibftdi

Copyright (c) 2014 Lukasz Majewski <l.majewski@samsung.com>
License: GPLv2+
"""
import usb
import sys
import string
import argparse
import datetime
from pylibftdi import BitBangDevice


pins = ["TXD", "RXD", "RTS", "CTS", "DTR", "DSR", "DCD", "RI"]

def hwtIOOffAll():
	with BitBangDevice() as bbdev:
		bbdev.port = 0xFF

def hwtIOOnAll():
	with BitBangDevice() as bbdev:
		bbdev.port = 0x00

def hwtIOSetPinState(pin, state):
	""" Execution routine """

	if args.pin.upper() not in pins:
		print 'HWT PWR - there is no "%s" pin available!' % args.pin
		return

	if state not in ["ON", "OFF"]:
		print 'HWT PWR - state "%s" not supported!' % state
		return

	if args.debug_en:
		print "PIN: %s [%s]" % (pin, state)

	with BitBangDevice() as bbdev:
		tmp = bbdev.port
		if args.debug_en:
			sys.stdout.write("Current: 0x%x" % tmp)

		idx = pins.index(pin)
		if state == "OFF":
			tmp |= (1 << idx)
		else:
			tmp &= ~(1 << idx)

		if args.debug_en:
			print " New: 0x%x" % tmp

		bbdev.port = tmp

def hwtIOInitDevice(deviceSerial):
	""" Initialization routine """

	# idVendor=0x0403, idProduct=0x6001
	# are for FTDI USB <-> Serial converter
	# they shouldn't change -> conpare iSerialNumber

	dev = usb.core.find(idVendor=0x0403, idProduct=0x6001)
	if dev is None:
		print 'HWT PWR device is not connected!'
		sys.exit()
	else:
		iSerialNumber = usb.util.get_string(dev, dev.iSerialNumber)
		if iSerialNumber != deviceSerial:
			print "iSerialNumber: %s does not match %s" % \
			       (iSerialNumber, deviceSerial)
			sys.exit()

def displayHelp():
	print "\nFTDI232RL pins description:"
	print "---------------------------"
	i = 0
	for pin in pins:
		print "D%d:\t--->\t%s" % (i, pins[i])
		i += 1
	print "---------------------------\n"
	print "One can also specify ALL to\n"
	print "change state of all pins\n"

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description=
					 'HW test (HWT) PWR control \
					 (via FTDI232R)',)

	parser.add_argument('--debug',
			    action='store_true',
			    default=False,
			    dest='debug_en',
			    help='Enable printing debug information')
	parser.add_argument('-d', '--device', required = True,
			    help='FT232 Device to connect')
	parser.add_argument('-p', '--pin', required = True,
			    help='Pin to control - e.g. CTS, ALL')
	parser.add_argument('state', nargs='?', default="OFF",
			    help='State - on/off')

	args = parser.parse_args()

	if args.pin.upper() == "ALL":
		if args.state.upper() == "ON":
			hwtIOOnAll()
		else:
			hwtIOOffAll()
		sys.exit()

	if args.debug_en:
		print "HWT PWR control (FTDI232RL based) - %s" % \
		    str(datetime.datetime.now())[:19]
		displayHelp()

	hwtIOInitDevice(args.device)
	hwtIOSetPinState(args.pin.upper(), args.state.upper())
