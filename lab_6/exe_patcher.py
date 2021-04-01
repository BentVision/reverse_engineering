#Python 3.6
import os #Interact with system directories & files
import binascii #Convert UTF-8 byte code into HEX format
import re #Parse through hex code and isolate desired character from output
from subprocess import Popen,PIPE,STDOUT #Run and communicate with newly generated executables

#These directory paths are relative to whoever is running the program
#SET FOR DIRECTORY CONTAINING ORIGNINAL EXE FILES
source_dir = "D:\\Code\\python_code\\binaries\\256exes\\"
#SET FOR LOCATION OF NEW FILES
destination_dir = "D:\\Code\\python_code\\binaries\\256exes_modded\\"

#Patching Function
def patcher(src_file, dst_file):

    f = open(src_file, "rb")

    #Store byte data of program into variable in HEX form
    data = b''
    try:
        byte = f.read(1)
        while byte != b"":
            data += byte
            byte = binascii.hexlify(f.read(1))
    finally:
        f.close()

    #Break down the single string of byte data into a list of Hex pairs
    hexes = re.findall('..', str(data[1:]))     #Split the single string into hex digit pairs
    hexes.insert(1, '4d')   #4d is equivilent to the 'M' bytes marker and needs to be readded
    #print(hexes)

    #Replace compare and jump functions with NOPS (90) in the hexes
    new_hexes = []
    marker = 0
    pre_hex = 'xxxxxx'
    for count, line in enumerate(hexes):
        if '3b' in line and ('000000' in pre_hex or 'ffffff' in pre_hex) and ('75' in hexes[count+6]):    
            #3b is the unique identifier in conjunstion with 75 and being preceeded by ffffff or 000000
            marker = count + 8
            #print(line)
        if count < marker:
            new_hexes.append('90') #Insert NOP values
        else:
            new_hexes.append(line)
        pre_hex = pre_hex[2:] + line
        #print(pre_hex)

    #Reconstruct new data into exe format
    new_data = binascii.unhexlify(''.join(new_hexes[1:]))   #Ommit the first b' value since it is added in the reconstruction
    #print(new_data)

    g = open(dst_file, "wb")
    g.write(new_data)
    g.close()

#Iterate though all files in source directory, patch, and generate new executable

for filename in os.listdir(source_dir):
    #Contruct file paths
    src_file = source_dir + filename
    dst_file = destination_dir + filename[:5] + "_modded" + filename[5:]
    patcher(src_file, dst_file)


#Interact with each modded executable to gather all character outputs
def get_character(dst_file):
    current = Popen(dst_file, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
    response = str(current.communicate('1'.encode()))
    #print(response)
    character = re.findall(r'\((.)\)', response)[0]
    #print(character)
    return character

#Iterate though all modded files to construct the full 256 byte message
message = []
for filename in os.listdir(destination_dir):
    dst_file = destination_dir + filename
    #print(dst_file)  #Display path of current file
    message.append(get_character(dst_file))
    
print(''.join(message))

#Means to test out the conditions for different EXEs
#patcher("D:\\Code\\python_code\\binaries\\256exes\\00014.exe", "D:\\Code\\python_code\\binaries\\256exes_modded\\00014_modded.exe")
#get_character("D:\\Code\\python_code\\binaries\\256exes_modded\\00014_modded.exe")