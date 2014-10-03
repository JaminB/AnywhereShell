#!/usr/bin/python
import os
import socket
import thread
import logging
logging.basicConfig(filename='knock-server.log',level=logging.DEBUG, format='%(asctime)s %(message)s')
def main():
	import optparse
	parser = optparse.OptionParser()
	parser.add_option('-p', '--management-port', action='store', dest='listening_port', default='9001', type='int', help='The port that your management server runs on')
	options, args = parser.parse_args()
	Server(options.listening_port).start()

class Knock:
	def __init__(self, knock=None):
		self.knock_folder = "knocks/"
		self.knock = knock.replace(' ', '').strip()
		self.SUCCESS = 0
		self.FAILURE = -1

	def create(self, clientIP):
		try:
			f = open(self.knock_folder + self.knock, 'w')	
			f.write(clientIP.strip() + '\n' + 'wait')
			f.close()
			logging.info("Successfully created new knock: " + self.knock + "linked to " + clientIP)
			return self.SUCCESS
		except:
			logging.warning("Failed to create knock: " + self.knock)
			return self.FAILURE
	
	def update(self, status):
		try:
			original = open(self.knock_folder + self.knock, 'r')
			ip = original.readline().strip()	
			original.close()
			new = open(self.knock_folder + self.knock, 'w')
			new.write(ip + '\n' + status)
			new.close()
			logging.info("Successfully updated status of knock: " + self.knock + " to " + status) 
			return self.SUCCESS
		except:
			logging.warning("Could not locate knock: " + self.knock)
			print "No Knock of that name"
			return self.FAILURE
	
	def select(self):
		try:
			knockFile = open(self.knock_folder + self.knock, 'r').read().split('\n')
			ip = knockFile[0]
			status = knockFile[1]
			logging.info("Successfully read knock: " + self.knock)
			return '> ip: ' + ip + ' | ' + 'status: ' + status + ' <'
		except:
			return self.FAILURE
			logging.warning("Could not locate knock: " + self.knock)
			print "No Knock of that name."

	def delete(self):
		try:
			os.remove(self.knock_folder + self.knock)
			logging.info("Successfully removed knock: " + self.knock)
			return self.SUCCESS
		except:
			print "No Knock of that name."
			logging.warning("Could not locate knock: " + self.knock)
			return self.FAILURE

class Interpreter:
	def __init__(self, command, ip=''):
		self.SUCCESS = 0
		self.FAILURE = -1
		self.commandString = command
		self.command = command.strip().split(' ')
		self.ip = ip
	
	def set_ip(self, ip):
		self.ip = ip
	
	def get_ip(self):
		return self.ip

	def start(self):
		commandString = self.commandString
		command = self.command
		for i in range(1, len(commandString) -2):
			if not commandString[i].isalnum():
				if commandString[i] != ':' and commandString[i] != ' ' and commandString[i] != '=':
					#print "Invalid character in knock."
					logging.warning("Request-Failure: Invalid character in request = " + commandString[i]) 
					return (self.FAILURE, "> Invalid character in knock. <")
		if command[0] != '>':
			#print "No start header."
			logging.warning("Request-Failure: No start header")
			return (self.FAILURE, "> No start header. <")
		
		elif command[-1] != '<':
			#print "No end header."
			logging.warning("Request-Failure: No end header")
			return (self.FAILURE, "> No, end header. <")
		
		
		elif len(commandString) < 8:
			#print "Invalid length"
			return (self.FAILURE, "> Invalid length <")
		
		
		elif command[1] == "create:":
			knockName = ''
			for i in range(2,len(command) - 1):
				knockName+=command[i]
			knock = Knock(knockName.replace(' ',''))
			if knock.create(self.ip) == 0:
				#print "Created new knock for " + self.ip
				return (self.SUCCESS, "> Created new knock for " + self.ip + ' <')	
			else:
				return (self.FAILURE, "> Could not create new knock for " + self.ip + ' <')
		
		elif command[1] == "select:":
			knockname = ''
			for i in range(2,len(command) - 1):
				knockname+=command[i]
			knock = Knock(knockname.replace(' ', ''))
			result = knock.select()
			if result != -1:
				#print "Selected ip for knock: " + knockName
				return (self.SUCCESS, result)
			else:
				#print "Knock not found."
				return (self.FAILURE, "> Knock not found <")

		elif command[1] == "update:":
			knockname = ''
			for i in range(2,len(command) - 1):
				if command[i] == '=': break
				knockname+=command[i]
			knock = Knock(knockname.replace(' ', ''))
			try:
				if '=' not in self.commandString:
					return (self.FAILURE, '> Expected "=" <')
				try:
					status = self.commandString.split('=')[1].split(' ')[1]
				except:
					return (self.FAILURE, "> Invalid parameter after status. <")
				if status == "wait" or status == "connect":
					knock.update(status)
					return (self.SUCCESS, "> Updated status for agent on " + self.ip + ' <')
				else:
					return (self.FAILURE, "> Invalid parameter after status. <")
			except:
				return (self.FAILURE, "> Knock not found. <")

	
class Server:
	def __init__(self, port):
		logging.info("Starting server...")
		self.port = port
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.bind(('0.0.0.0', self.port))
		self.socket.listen(2)

	def _parse_client_ip(self, addr):
		return str(addr).split("'")[1].strip()

	def handler(self, conn, addr):
		data = conn.recv(1024)
		if data:
			result = Interpreter(data, self._parse_client_ip(addr))
			resultMessage = result.start()
			print 'Received request from Agent: (' + result.get_ip() +'(: ' + 'Message = ' + data + ')'
			print 'Sending response to Agent (' + result.get_ip() + '): ' + 'Message  = ' + resultMessage[1]
			conn.sendall(str(resultMessage))
		conn.close()

	def start(self):
		import sys
		while 1:
			try:
				conn, addr = self.socket.accept()
				thread.start_new_thread(self.handler,(conn,addr))
			except KeyboardInterrupt:
				logging.info("Killing server...")
				print "\nKilling Server..."
				self.socket.shutdown(socket.SHUT_RDWR)
				self.socket.close()
				sys.exit(0)
		
		
if __name__ == "__main__":
	main()
