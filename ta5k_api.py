from netmiko import ConnectHandler

class Adtran_TA5K():
    id = ""
    address = ""
    port = ""
    username = ""
    password = ""

    SN = ""
    location = ""

    def __init__(self, id, address, port, username, password):
        self.id = id
        self.address = address
        self.port = port
        self.username = username
        self.password = password

        self.net_connect = ConnectHandler(
            device_type="adtran_os",
            host = self.address,
            username = self.username,
            password = self.password,
        )
        self.net_connect.enable()

    # Basic functions

    # Opens a connection, sends a command, closes the conection ad return the output.
    def sendSimpleCommand(self, command):
        net_connect = ConnectHandler(
            device_type="adtran_os",
            host = self.address,
            username = self.username,
            password = self.password,
        )
        net_connect.enable()
        out = self.net_connect.send_command(command)
        net_connect.disconnect()
        return out

    # Allows sending multiple command, uses the built in object, user must remember to close the connection.
    def sendCommandInteractive(self, command):
        return self.net_connect.send_command(command)

    # Closes the connection
    def closeConnection(self):
        self.net_connect.disconnect()
        return 0

    # Config related functions

    def getAllConfig(self):
        cmd = "show running-config"
        return self.sendCommandInteractive(cmd)

    def getAllConfigVerbose(self):
        cmd = "show running-config verbose"
        return self.sendCommandInteractive(cmd)

    # System related functions

    def getUptime(self):
        cmd = "show version 1/S | include Uptime"
        return self.sendCommandInteractive(cmd)

    # Provision related functions

    # Returns the RAW output for "show table remote-devices inactive"
    def getRDInactive(self):
        cmd = "show table remote-devices inactive"
        return self.sendCommandInteractive(cmd)

    # Returns the RAW output for "show table remote-devices ont"
    def getRDONT(self):
        cmd = "show table remote-devices ont"
        return self.sendCommandInteractive(cmd)

    # Returns the RAW output for "show table remote-devices ont @1/3/1.gpon "
    def getRDONTSpecific(self, remote_index):
        cmd = "show table remote-devices ont @"+remote_index+".gpon"
        return self.sendCommandInteractive(cmd)

    """
    Returns a list of dicts contaiing GPONL2 devices ex: 
    [{
        'remote_index': '1/3/2',
        'serial_number': 'ADTN2108158b' 
    }]
    """
    def getRDInactivePretty(self):
        out = self.getRDInactive()
        out = ''.join(out.splitlines(keepends=True)[2:])
        out_lines = out.splitlines()
        
        count = 0
        devices = []
        for line in out_lines:
            lsplitted = line.split()
            devices.append({
                "remote_index":lsplitted[0],
                "serial_number":lsplitted[1]
                })
            count += 1

        return devices

    """
    Returns a list of dicts contaiing GPONL2 devices ex:
    [{
        'remote_index': '2@1/3/1.gpon', 
        'admin_state': 'IS', 
        'oper_state': 'up', 
        'serial_number': 'ADTN2111699b', 
        'fiber_dist': '46', 
        'ont_power': '-18.1|4.0', 
        'bip_error': '0|0', 
        'rdi': '0', 
        'aes': 'Dis'
    }]
    """
    def getRDONTPretty(self):
        out = self.getRDONT()
        out = ''.join(out.splitlines(keepends=True)[4:])
        out_lines = out.splitlines()

        count = 0
        devices = []
        for line in out_lines:
            lsplitted = line.split()
            devices.append({
                "remote_index":lsplitted[0],
                "admin_state":lsplitted[1],
                "oper_state":lsplitted[2],
                "serial_number":lsplitted[3],
                "fiber_dist":lsplitted[4],
                "ont_power":lsplitted[5],
                "bip_error":lsplitted[6],
                "rdi":lsplitted[7],
                "aes":lsplitted[8]
                })
            count += 1

        return devices

    def getRDONTSpecificPretty(self, remote_index):
        out = self.getRDONTSpecific(remote_index)
        out = ''.join(out.splitlines(keepends=True)[4:])
        out_lines = out.splitlines()

        count = 0
        devices = []
        for line in out_lines:
            lsplitted = line.split()
            devices.append({
                "remote_index":lsplitted[0],
                "admin_state":lsplitted[1],
                "oper_state":lsplitted[2],
                "serial_number":lsplitted[3],
                "fiber_dist":lsplitted[4],
                "ont_power":lsplitted[5],
                "bip_error":lsplitted[6],
                "rdi":lsplitted[7],
                "aes":lsplitted[8]
                })
            count += 1

        return devices

    def findNextRemoteIndex(self, remote_index):
        remote_devices = self.getRDONTSpecificPretty(remote_index)
        indexes = []

        # Generate the index list
        for device in remote_devices:
            index = device["remote_index"].split("@")
            indexes.append(int(index[0]))
        
        # Find the available index
        for i in range(len(indexes)):
            if (i+1) !=  indexes[i]:
                # Hueco en la serie
                return i+1
        # The next index is the last +1
        next_index = (len(indexes) +1 )
        # Check that the index is correct
        if (next_index != 0) and (next_index < 128):
            return next_index

    def interactive_provision(self):
        print("\nWelcome to integrated provision, here is the list of available remote devices:\n")
        remote_devices = self.getRDInactivePretty()
        for i in range(len(remote_devices)):
            print("   ->  "+str(i)+"  -  "+remote_devices[i]["remote_index"]+"  -  "+remote_devices[i]["serial_number"]+"\n")
        id = int(input("Please input the id of the selected device: "))
        print("\nYou selected: "+remote_devices[i]["serial_number"])
        print("\nSelecting new remote index...")
        new_index = self.findNextRemoteIndex(remote_devices[i]["remote_index"])
        print("\nNew remote index = "+str(new_index))
        
        return 0
