#!/usr/bin/python

#copyright Philippe Thirion
#github.com/tirfil
#

import sys
import string

class parser:
	def __init__(self,filename):
		self.modules={}
		self.entity=""
		self.architecture="rtl"
		self.clock="MCLK"
		self.clockedge=1
		self.reset="nRST"
		self.resettype=0
		self.read(filename)
		
	def getName(self):
		return self.entity
	
	def read(self,filename):
		with open(filename,'r') as f:
			for line in f:
				#print len(line)
				if len(line) < 3:
					continue
				parameters = string.split(line)
				command = parameters[0]
				command = command.lower()
				if command == "entity":
					self.entity = parameters[1]
					#print "entity is %s" % self.entity
					self.modules[self.entity] = []
				if (command == "clock"):
					self.clock = parameters[1]
					if len(parameters)==3:
						if parameters[2] == "0":
							self.clockedge=0
					command = "in"
					parameters[0] = "in"
				if (command == "reset"):
					self.reset = parameters[1]
					if len(parameters)==3:
						if parameters[2] == "1":
							self.resettype=1
					command = "in"
					parameters[0] = "in"
				if (command == "in") or \
						(command == "out") or \
						(command == "inout"):
					a = self.modules[self.entity]
					a.append(parameters)
				if (command[0:4] == "arch"):
					self.architecture = parameters[1]
				if command == 'end':
					break
					
	def header(self):
		buffer=[]
		buffer.append("--###############################")
		buffer.append("--# Project Name : ")
		buffer.append("--# File         : ")
		buffer.append("--# Author       : ")
		buffer.append("--# Description  : ")
		buffer.append("--# Modification History")
		buffer.append("--#")
		buffer.append("--###############################")
		buffer.append("")		
		buffer.append("library IEEE;")
		buffer.append("use IEEE.std_logic_1164.all;")
		buffer.append("")
		return buffer
		
	def port(self,iolist,tab=0):
		last=len(iolist)
		index=1
		buffer=[]
		pre="\t"*tab
		for io in iolist:
			if len(io) == 3: # is a bus ?
				high = int(io[2])-1 # bus msb
				line=pre + "\t\t%s\t\t: %s\tstd_logic_vector(%d downto 0)" % (io[1],io[0],high)
			else:
				line=pre + "\t\t%s\t\t: %s\tstd_logic" % (io[1],io[0])
			if index != last:
				buffer.append(line + ";")
				index += 1
			else:
				buffer.append(line)
		return buffer
					
	def write_entity(self,name):
		if not self.modules.has_key(name):
			return ""
		buffer=[]
		iolist=self.modules[name]
		buffer.append("entity %s is" % name)
		buffer.append("\tport(")
		buffer += self.port(iolist)
		buffer.append("\t);")
		buffer.append("end %s;" % name)
		buffer.append("")
		return buffer
		
	def component(self,name,tab=0):
		if not self.modules.has_key(name):
			return ""
		pre="\t"*tab
		buffer=[]
		iolist=self.modules[name]
		buffer.append(pre + "component %s" % name)
		buffer.append(pre +"\tport(")
		buffer += self.port(iolist,tab)
		buffer.append(pre +"\t);")
		buffer.append(pre +"end component;")
		buffer.append("")
		return buffer
		
	def portmap(self,name,digit,tab=0):
		if not self.modules.has_key(name):
			return ""
		buffer=[]
		pre="\t"*tab
		iolist=self.modules[name]
		buffer.append(pre + "I_%s_%d : %s" % (name,digit,name))
		buffer.append(pre + "\tport map (")
		last=len(iolist)
		index=1
		for io in iolist:
			line= pre + "\t\t%s\t\t=> %s" % (io[1],io[1])
			if index != last:
				buffer.append(line +",")
				index += 1
			else:
				buffer.append(line)
		buffer.append(pre + "\t);")
		buffer.append("")
		return buffer
		
	def signals(self,name,tab=0):
		if not self.modules.has_key(name):
			return ""
		buffer=[]
		pre="\t"*tab
		iolist=self.modules[name]
		for io in iolist:
			if len(io) == 3:
				high = int(io[2])-1
				buffer.append(pre + "signal %s\t\t: std_logic_vector(%d downto 0);" % (io[1],high))
			else:
				buffer.append(pre + "signal %s\t\t: std_logic;" % io[1])
		buffer.append("")
		return buffer
		
	def vhdl(self,name):
		buffer=[]
		buffer += self.header()
		buffer += self.write_entity(name)
		buffer.append("architecture %s of %s is" % (self.architecture,name))
		buffer.append("")
		buffer.append("begin")
		buffer.append("")
		buffer.append("\tTODO: process( %s, %s)"% (self.clock,self.reset))
		buffer.append("\tbegin")
		buffer.append("\t\tif ( %s = '%d') then" % (self.reset,self.resettype))
		buffer.append("")
		buffer.append("\t\telsif ( %s'event and %s = '%d') then" % (self.clock,self.clock,self.clockedge))
		buffer.append("")
		buffer.append("\tend process TODO;")
		buffer.append("")		 
		buffer.append("end %s;" % self.architecture)
		buffer.append("");
		return buffer
		
	def testbench(self,name):
		buffer=[]
		buffer += self.header()
		buffer.append("entity tb_%s is" % name)
		buffer.append("end tb_%s;" % name)
		buffer.append("")
		buffer.append("architecture stimulus of tb_%s is" % name)
		buffer.append("")
		buffer.append("-- COMPONENTS --")
		buffer += self.component(name,1)
		buffer.append("--")
		buffer.append("-- SIGNALS --")
		buffer += self.signals(name,1)
		buffer.append("--")
		buffer.append("\tsignal RUNNING	: std_logic := '1';")
		buffer.append("")		
		buffer.append("begin")
		buffer.append("")
		buffer.append("-- PORT MAP --")
		buffer += self.portmap(name,0,1)
		buffer.append("--")
		buffer.append("\tCLOCK: process")
		buffer.append("\tbegin")
		buffer.append("\t\twhile (RUNNING = '1') loop")
		buffer.append("\t\t\t%s <= '1';" % self.clock)
		buffer.append("\t\t\twait for 10 ns;")
		buffer.append("\t\t\t%s <= '0';" % self.clock)
		buffer.append("\t\t\twait for 10 ns;")
		buffer.append("\t\tend loop;")
		buffer.append("\t\twait;")
		buffer.append("\tend process CLOCK;")
		buffer.append("")
		buffer.append("\tGO: process")
		buffer.append("\tbegin")
		val = self.resettype 
		if val == 0:
			invval = 1;
		else:
			invval = 0;
		buffer.append("\t\t%s <= '%d';" % (self.reset,val))
		buffer.append("\t\twait for 1000 ns;")
		buffer.append("\t\t%s <= '%d';" % (self.reset,invval))
		buffer.append("")
		buffer.append("\t\tRUNNING <= '0';")
		buffer.append("\t\twait;")
		buffer.append("\tend process GO;")
		buffer.append("")
		buffer.append("end stimulus;")
		return buffer
	
if __name__ == "__main__":
	if len(sys.argv) != 2:
		print "usage: %s %s" % (sys.argv[0],"file")
		exit(0)		
	filename = sys.argv[1]
	obj = parser(filename)
	name = obj.getName()
	filename = name.lower() + "_empty.vhd"
	with open(filename,"w") as f:
		buffer = obj.vhdl(name)
		for line in buffer:
			f.write(line + '\n')
	filename = "tb_" + name.lower() + "_empty.vhd"
	with open(filename,"w") as f:
		buffer = obj.testbench(name)
		for line in buffer:
			f.write(line+ '\n')
"""
	buffer = obj.entity(name)
	for line in buffer:
		print line
	buffer = obj.component(name)
	for line in buffer:
		print line
	buffer = obj.portmap(name,0)
	for line in buffer:
		print line
	buffer = obj.signals(name)
	for line in buffer:
		print line	
	buffer = obj.header()
	for line in buffer:
		print line		
"""	

		
		
		


	
	



	


			

		
