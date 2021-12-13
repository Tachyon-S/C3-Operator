import os
import struct
from mathutils import Vector

class C3OP_Helping_File_Reader:
    def __init__(self, path, pointer=0):
        self.path = path
        self.pointer = pointer
        self.file = open(path, 'rb')
        self.length = 0
    
    def load(self):
        self.file.seek(0)
        self.data = self.file.read()
        self.length = len(self.data)

    def readInt(self, pointer=-1):
        if pointer == -1 :
            pointer = self.pointer
        integer = struct.unpack('<i', self.data[pointer:pointer+4])[0]
        self.pointer = self.pointer + 4
        return integer
    def readByte(self, pointer=-1):
        if pointer == -1 :
            pointer = self.pointer
        byte = struct.unpack('<b', self.data[pointer:pointer+1])[0]
        self.pointer = self.pointer + 1
        return byte
    def readShort(self, pointer=-1):
        if pointer == -1 :
            pointer = self.pointer
        #print(pointer)
        s = struct.unpack('<H', self.data[pointer:pointer+2])[0]
        
        self.pointer = self.pointer + 2
        return s
    def readFloat(self, pointer=-1):
        if pointer == -1 :
            pointer = self.pointer
        f = struct.unpack('<f', self.data[pointer:pointer+4])[0]
        self.pointer = self.pointer + 4
        return f
    def readString(self, length, pointer=-1):
        if pointer == -1 :
            pointer = self.pointer
        text = self.data[pointer:pointer+length].decode()
        self.pointer = self.pointer + length
        return text
    def setPointer(self, value):
        self.pointer = value
        return self.pointer
    def getPointer(self):
        return self.pointer
    def __len__(self):
        return self.length



class C3OP_Helping_File_Writer:
    def __init__(self, path):
        self.path = path
        self.pointer = 0
        self.file = open(path, 'wb')
        self.length = 0
    
    def load(self):
        self.file.seek(0)
        self.data = self.file.read()
        self.length = len(self.data)

    def writeInt(self, i, pointer=-1):
        if pointer == -1 :
            pointer = self.pointer
        self.file.write(struct.pack('<i', i))
        self.pointer = self.pointer + 4
        #return integer
    def writeByte(self, b, pointer=-1):
        if pointer == -1 :
            pointer = self.pointer
        self.file.write(struct.pack('<b', b))
        self.pointer = self.pointer + 1
        #return byte
    def writeShort(self, s, pointer=-1):
        if pointer == -1 :
            pointer = self.pointer
        #print(pointer)
        self.file.write(struct.pack('<H', s))
        
        self.pointer = self.pointer + 2
        #return s
    def writeFloat(self, f, pointer=-1):
        if pointer == -1 :
            pointer = self.pointer
        self.file.write(struct.pack('<f', f))
        self.pointer = self.pointer + 4
        #return f
    def writeString(self, s, pointer=-1):
        if pointer == -1 :
            pointer = self.pointer
        self.file.write(s.encode())
        self.pointer = self.pointer + len(s)
        #return text
    def writeBinaryString(self, s, pointer=-1):
        if pointer == -1 :
            pointer = self.pointer
        self.file.write(s)
        self.pointer = self.pointer + len(s)
        #return text
    #def setPointer(self, value):
        #self.pointer = value
        #return self.pointer
    def fillZeros(self, amount):
        self.file.write(b"\x00"*amount)
    def getPointer(self):
        return self.pointer
    #def __len__(self):
        #return self.length
    def close(self):
        self.file.close()

