#!/usr/bin/env python3

import os,sys,argparse,re

from cmd import Cmd
from contextlib import redirect_stdout

class bootlegShell(Cmd):


	def pipeMethod(self):
		pid = os.getpid()
		global pipeCommand
		os.write(1, ("About to fork (pid:%d)\n" % pid).encode())
		rc = os.fork()

		if rc < 0:
		    os.write(2, ("fork failed, returning %d\n" % rc).encode())
		    sys.exit(1)

		elif rc == 0:                   # child
		    #os.write(1, ("Child: My pid==%d.  Parent's pid=%d\n" % 
		    #             (os.getpid(), pid)).encode())
			args = [pipeCommand]
			for dir in re.split(":", os.environ['PATH']): # try each directory in the path
				program = "%s/%s" % (dir, args[0])
		        #os.write(1, ("Child:  ...trying to exec %s\n" % program).encode())
				try:
					normalIn = sys.stdin
					sys.stdin = open("pipe1.txt", "r")
					os.dup2(sys.stdin.fileno(), 0)
					os.execve(program, args, os.environ) # try to exec program
					sys.stdin = normalIn
				except FileNotFoundError:             # ...expected
					pass                              # ...fail quietly
			os.write(2, ("Child:    Could not exec %s\n" % args[0]).encode())
			sys.exit(1)                 # terminate with error

		else:                           # parent (forked ok)
		    #os.write(1, ("Parent: My pid=%d.  Child's pid=%d\n" % 
		    #             (pid, rc)).encode())
		    childPidCode = os.wait()
		    os.write(1, ("Parent: Child %d terminated with exit code %d\n" % 
		                 childPidCode).encode())                          # ...fail quietly

	def do_CDR(self, args):
		"""The shell itself, follow the prompts on screen. Output file must be created beforehand."""
		pid = os.getpid()
		print("Input command...")
		commandName = input()
		commands = commandName.split()
		command = commands[0]
		fileName=""
		pipe=False
		outFile=""
		global pipeCommand
		global program
		for x in range(len(commands)):
			if(commands[x]=='<'):
				fileName=commands[x+1]
			if(commands[x]=='>'):
				outFile=commands[x+1]
			if(commands[x]=='|'):
				outFile="pipe1.txt"
				pipe=True
				pipeCommand=commands[x+1]
		os.write(1, ("About to fork (pid:%d)\n" % pid).encode())
		rc = os.fork()

		if rc < 0:
		    os.write(2, ("fork failed, returning %d\n" % rc).encode())
		    sys.exit(1)

		elif rc == 0:                   # child
		    #os.write(1, ("Child: My pid==%d.  Parent's pid=%d\n" % 
		    #             (os.getpid(), pid)).encode())
			args = [command]
			for dir in re.split(":", os.environ['PATH']): # try each directory in the path
				program = "%s/%s" % (dir, args[0])
		        #os.write(1, ("Child:  ...trying to exec %s\n" % program).encode())
				try:
					normalIn = sys.stdin
					normalOut = sys.stdout
					if(fileName!=""):
						sys.stdin = open(fileName,"r")
					if(outFile!=""):
						sys.stdout = open(outFile,"w")
					if(pipe):
						sys.stdout = open("pipe1.txt", "w")
					os.dup2(sys.stdin.fileno(), 0)
					os.dup2(sys.stdout.fileno(), 1)
					os.execve(program, args, os.environ) # try to exec program
					sys.stdin = normalIn
					sys.stdout = normalOut
				except FileNotFoundError:             # ...expected
					pass                              # ...fail quietly
			os.write(2, ("Child:    Could not exec %s\n" % args[0]).encode())
			sys.exit(1)                 # terminate with error

		else:                           # parent (forked ok)
		    #os.write(1, ("Parent: My pid=%d.  Child's pid=%d\n" % 
		    #             (pid, rc)).encode())
		    childPidCode = os.wait()
		    os.write(1, ("Parent: Child %d terminated with exit code %d\n" % 
		                 childPidCode).encode())
		if(pipe==True):
			shell.pipeMethod()


	def do_hello(self, args):
		"""Says hello"""
		print("Greetings, Stranger!")

	def do_quit(self, args):
		"""Quits the terminal"""
		print("Goodbye, Stranger!")
		raise SystemExit


if __name__ == '__main__':
    shell = bootlegShell()
    shell.shell = '> '
    shell.cmdloop('Starting prompt...')