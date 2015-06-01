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

def hwtIOOffAll(dev):
	with BitBangDevice(dev) as bbdev:
		bbdev.port = 0xFF

def hwtIOOnAll(dev):
	with BitBangDevice(dev) as bbdev:
		bbdev.port = 0x00

def hwtIOSetPinState(dev, pin, state, debug_en=False):
	""" Execution routine """

	dev = dev.upper()
	pin = pin.upper()
	state = state.upper()

	if pin not in pins:
		print 'HWT PWR - there is no "%s" pin available!' % pin
		return

	if state not in ["ON", "OFF"]:
		print 'HWT PWR - state "%s" not supported!' % state
		return

	if debug_en:
		print "PIN: %s [%s]" % (pin, state)

	with BitBangDevice(dev) as bbdev:
		tmp = bbdev.port
		if debug_en:
			sys.stdout.write("Current: 0x%x" % tmp)

		idx = pins.index(pin)
		if state == "OFF":
			tmp |= (1 << idx)
		else:
			tmp &= ~(1 << idx)

		if debug_en:
			print " New: 0x%x" % tmp

		bbdev.port = tmp

def hwtIOInitDevice(deviceSerial):
	""" Initialization routine """

	# idVendor=0x0403, idProduct=0x6001
	# are for FTDI USB <-> Serial converter
	# they shouldn't change -> compare iSerialNumber

	dev = usb.core.find(find_all=True, idVendor=0x0403, idProduct=0x6001)
	if dev is None:
		print 'HWT PWR device is not connected!'
		sys.exit()

	for dev_instance in dev:
		iSerialNumber = usb.util.get_string(dev_instance,
						    dev_instance.iSerialNumber)
		if iSerialNumber == deviceSerial:
			return

	print "Device with serial: %s not found!" % deviceSerial
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

	hwtIOInitDevice(args.device)
	if args.pin.upper() == "ALL":
		if args.state.upper() == "ON":
			hwtIOOnAll(args.device)
		else:
			hwtIOOffAll(args.device)
		sys.exit()

	if args.debug_en:
		print "HWT PWR control (FTDI232RL based) - %s" % \
		    str(datetime.datetime.now())[:19]
		displayHelp()

	hwtIOSetPinState(args.device, args.pin, args.state, args.debug_en)
