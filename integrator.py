import json
from ta5k_api import Adtran_TA5K

# Gets OLT info from config file, this will return a list type object
def loadOLTsfromfile(file):
    # Load file
    f = open (file, "r")
    # Convert json to dictionary
    data = json.loads(f.read())
    return data['TA5Ks']

# Return a type dict containig info of specified OLT
def getOLTbyID(id, list):
    for x in list:
        if x["id"] == id:
            return x
    return None

# To get the IP of an specific OLT, getOLTbyID(2,olts)[address] where 2 is the id of the desired OLT.

# Load OLTs from file
olts = loadOLTsfromfile('config.json')

# Get the Lab one, id=3
OLT_Test = getOLTbyID(3,olts)

# Create olt instance
olt = Adtran_TA5K(OLT_Test["id"], OLT_Test["address"], OLT_Test["port"], OLT_Test["username"], OLT_Test["password"])

# Test command
olt.provADTRANSDX611("ADTN21081694","2@1/3/2.gpon",1000,1000,'ipoe-10','20')
#olt.interactive_provision()
