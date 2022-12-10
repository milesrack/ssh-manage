#!/usr/bin/python
import os
import sys
import socket
import threading
import queue
import ipaddress
import paramiko

BASE_DIR = os.path.dirname(__file__)
NETWORK = "192.168.6.0/24"

class Client:
	def __init__(self, ip, port=22, username="root", password=None, keyfile=os.path.join(BASE_DIR, "id_rsa")):
		self.__ip = ip
		self.__port = port
		self.__username = username
		self.__password = password
		self.__keyfile = keyfile
		self.__key = paramiko.RSAKey.from_private_key_file(self.__keyfile)
		try:
			self.__ssh = paramiko.SSHClient()
			self.__ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			self.__ssh.connect(self.__ip, self.__port, self.__username, pkey=self.__key)
		except:
			self.__ssh = None

	def get_ip(self):
		return self.__ip

	def get_ssh(self):
		return self.__ssh

	def exec(self, cmd):
		if self.__ssh:
			try:
				stdin, stdout, stderr = self.__ssh.exec_command(cmd)
				out = {"host":self.__ip, "stdout":stdout.read().decode(), "stderr":stderr.read().decode()}
				print(f"[+] {out}")
			except Exception as e:
				print(f"[-] {str(e)}")

class C2:
	def __init__(self, cidr):
		self.cidr = cidr
		self.network = [str(ip) for ip in ipaddress.IPv4Network(cidr)]
		self.online = []
		self.scan()
	
	def __scan(self, q):
		while q.not_empty:
			try:
				ip = q.get_nowait()
			except:
				return
			try:
				s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				s.settimeout(3)
				s.connect((ip, 22))
				banner = s.recv(1024)
				if b'SSH-2.0-OpenSSH' in banner:
					print(f"[+] {ip} online")
					client = Client(ip)
					self.online.append(client)
				s.close()
			except Exception as e:
				#print(f"[-] {str(e)}")
				pass
			q.task_done()
	
	def scan(self):
		q = queue.Queue()
		[q.put(ip) for ip in self.network]
		for _ in range(255):
			t = threading.Thread(target=self.__scan, args=(q,))
			t.start()
		q.join()
	
	def __send(self, q, cmd):
		while q.not_empty:
			try:
				c = q.get_nowait()
				c.exec(cmd)
			except:
				return
			q.task_done()
	def send(self, cmd):
		q = queue.Queue()
		[q.put(c) for c in self.online]
		for _ in range(len(self.online)):
			t = threading.Thread(target=self.__send, args=(q, cmd))
			t.start()
		q.join()

print("""\
         _nnnn_                      
        dGGGGMMb     ,\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"'
       @p~qp~~qMb    |  I use Arch Linux  |
       M|@||@) M|   _;....................'
       @,----.JM| -'
      JS^\\__/  qKL
     dZP        qKRb
    dZP          qKKb
   fZP            SMMb
   HZM            MMMM
   FqM            MMMM
 __| ".        |\\dS"qML
 |    `.       | `' \\Zq
_)      \\.___.,|     .'
\\____   )MMMMMM|   .'
     `-'       `--'\
""")
network_input = input(f"Enter the network your client devices are on ({NETWORK}): ")
if len(network_input) > 0:
	NETWORK = network_input
c2 = C2(NETWORK)
while True:
	try:
		cmd = input("[ssh-manage] > ")
		if cmd == "exit":
			sys.exit()
		else:
			c2.send(cmd)
	except KeyboardInterrupt:
		sys.exit()