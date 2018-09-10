#! /usr/bin/env python3

import os,sys,argparse,re

from cmd import Cmd
from contextlib import redirect_stdout

class bootlegShell(Cmd):



	def do_test(self, args):
		#The shell itself, follow the prompts on screen. Output file must be created beforehand.
		pid = os.getpid()
		print("Input file name...or press enter")
		fileName = input()
		print("Input command...")
		commandName = input()
		print("Input output file name... or press enter")
		outFile = input()
		os.write(1, ("About to fork (pid:%d)\n" % pid).encode())
		rc = os.fork()

		if rc < 0:
		    os.write(2, ("fork failed, returning %d\n" % rc).encode())
		    sys.exit(1)

		elif rc == 0:                   # child
		    #os.write(1, ("Child: My pid==%d.  Parent's pid=%d\n" % 
		    #             (os.getpid(), pid)).encode())
			args = [commandName]
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
