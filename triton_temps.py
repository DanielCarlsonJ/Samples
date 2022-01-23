import socket
import time
import pandas as pd
from datetime import datetime
import re
import h5py

def gather_temps():
  ##### Time #####
  
  _address = "Triton-Dr.mer.utexas.edu"
  port = 33576
  _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  _socket.connect((_address, port))
  
  cmd = 'READ:SYS:TIME' + '\r\n'
  _socket.sendall(cmd.encode())
  curr_time = _socket.recv(256)
  curr_time = curr_time.decode()
  curr_time = re.sub('STAT:SYS:TIME:', '', curr_time)
  curr_time = curr_time[:-2]
  curr_time = curr_time.replace(':','')
  
  try:
    _socket.shutdown(socket.SHUT_RDWR)
  except Exception as e:
    pass
  _socket.close()
  _socket = None
  
  ##### T1 #####
  
  _address = "Triton-Dr.mer.utexas.edu"
  port = 33576
  _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  _socket.connect((_address, port))
  
  _socket.sendall('READ:DEV:T1:TEMP:SIG:TEMP\r\n'.encode())
  temp1 = _socket.recv(1024)
  temp1 = temp1.decode()
  temp1 = re.sub('STAT:DEV:T1:TEMP:SIG:TEMP:', '', temp1)
  temp1 = temp1[:-2]
  	
  try:
    _socket.shutdown(socket.SHUT_RDWR)
  except Exception as e:
    pass
  _socket.close()
  _socket = None
  
  ##### T2 #####
  
  _address = "Triton-Dr.mer.utexas.edu"
  port = 33576
  _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  _socket.connect((_address, port))
  
  _socket.sendall('READ:DEV:T2:TEMP:SIG:TEMP\r\n'.encode())
  temp2 = _socket.recv(1024)
  temp2 = temp2.decode()
  temp2 = re.sub('STAT:DEV:T2:TEMP:SIG:TEMP:', '', temp2)
  temp2 = temp2[:-2]
  	
  try:
    _socket.shutdown(socket.SHUT_RDWR)
  except Exception as e:
    pass
  _socket.close()
  _socket = None
  
  ##### T3 #####
  
  _address = "Triton-Dr.mer.utexas.edu"
  port = 33576
  _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  _socket.connect((_address, port))
  
  _socket.sendall('READ:DEV:T3:TEMP:SIG:TEMP\r\n'.encode())
  temp3 = _socket.recv(1024)
  temp3 = temp3.decode()
  temp3 = re.sub('STAT:DEV:T3:TEMP:SIG:TEMP:', '', temp3)
  temp3 = temp3[:-2]
  	
  try:
    _socket.shutdown(socket.SHUT_RDWR)
  except Exception as e:
    pass
  _socket.close()
  _socket = None
  
  ##### T4 #####
  
  _address = "Triton-Dr.mer.utexas.edu"
  port = 33576
  _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  _socket.connect((_address, port))
  
  _socket.sendall('READ:DEV:T4:TEMP:SIG:TEMP\r\n'.encode())
  temp4 = _socket.recv(1024)
  temp4 = temp4.decode()
  temp4 = re.sub('STAT:DEV:T4:TEMP:SIG:TEMP:', '', temp4)
  temp4 = temp4[:-2]
  	
  try:
    _socket.shutdown(socket.SHUT_RDWR)
  except Exception as e:
    pass
  _socket.close()
  _socket = None
  
  ##### T5 #####
  
  _address = "Triton-Dr.mer.utexas.edu"
  port = 33576
  _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  _socket.connect((_address, port))
  
  _socket.sendall('READ:DEV:T5:TEMP:SIG:TEMP\r\n'.encode())
  temp5 = _socket.recv(1024)
  temp5 = temp5.decode()
  temp5 = re.sub('STAT:DEV:T5:TEMP:SIG:TEMP:', '', temp5)
  temp5 = temp5[:-2]
  	
  try:
    _socket.shutdown(socket.SHUT_RDWR)
  except Exception as e:
    pass
  _socket.close()
  _socket = None
  
  ##### T6 #####
  
  _address = "Triton-Dr.mer.utexas.edu"
  port = 33576
  _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  _socket.connect((_address, port))
  
  _socket.sendall('READ:DEV:T6:TEMP:SIG:TEMP\r\n'.encode())
  temp6 = _socket.recv(1024)
  temp6 = temp6.decode()
  temp6 = re.sub('STAT:DEV:T6:TEMP:SIG:TEMP:', '', temp6)
  temp6 = temp6[:-2]
  	
  try:
    _socket.shutdown(socket.SHUT_RDWR)
  except Exception as e:
    pass
  _socket.close()
  _socket = None
  
  ##### T7 #####
  
  _address = "Triton-Dr.mer.utexas.edu"
  port = 33576
  _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  _socket.connect((_address, port))
  
  _socket.sendall('READ:DEV:T7:TEMP:SIG:TEMP\r\n'.encode())
  temp7 = _socket.recv(1024)
  temp7 = temp7.decode()
  temp7 = re.sub('STAT:DEV:T7:TEMP:SIG:TEMP:', '', temp7)
  temp7 = temp7[:-2]
  	
  try:
    _socket.shutdown(socket.SHUT_RDWR)
  except Exception as e:
    pass
  _socket.close()
  _socket = None
  
  ##### T8 #####
  
  _address = "Triton-Dr.mer.utexas.edu"
  port = 33576
  _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  _socket.connect((_address, port))
  
  _socket.sendall('READ:DEV:T8:TEMP:SIG:TEMP\r\n'.encode())
  temp8 = _socket.recv(1024)
  temp8 = temp8.decode()
  temp8 = re.sub('STAT:DEV:T8:TEMP:SIG:TEMP:', '', temp8)
  temp8 = temp8[:-2]
  	
  try:
    _socket.shutdown(socket.SHUT_RDWR)
  except Exception as e:
    pass
  _socket.close()
  _socket = None
  
  ##### T9 #####
  
  _address = "Triton-Dr.mer.utexas.edu"
  port = 33576
  _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  _socket.connect((_address, port))
  
  _socket.sendall('READ:DEV:T9:TEMP:SIG:TEMP\r\n'.encode())
  temp9 = _socket.recv(1024)
  temp9 = temp9.decode()
  temp9 = re.sub('STAT:DEV:T9:TEMP:SIG:TEMP:', '', temp9)
  temp9 = temp9[:-2]
  	
  try:
    _socket.shutdown(socket.SHUT_RDWR)
  except Exception as e:
    pass
  _socket.close()
  _socket = None
  
  ##### T10 #####
  
  _address = "Triton-Dr.mer.utexas.edu"
  port = 33576
  _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  _socket.connect((_address, port))
  
  _socket.sendall('READ:DEV:T10:TEMP:SIG:TEMP\r\n'.encode())
  temp10 = _socket.recv(1024)
  temp10 = temp10.decode()
  temp10 = re.sub('STAT:DEV:T10:TEMP:SIG:TEMP:', '', temp10)
  temp10 = temp10[:-2]
  	
  try:
    _socket.shutdown(socket.SHUT_RDWR)
  except Exception as e:
    pass
  _socket.close()
  _socket = None
  
  ##### T11 #####
  
  _address = "Triton-Dr.mer.utexas.edu"
  port = 33576
  _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  _socket.connect((_address, port))
  
  _socket.sendall('READ:DEV:T11:TEMP:SIG:TEMP\r\n'.encode())
  temp11 = _socket.recv(1024)
  temp11 = temp11.decode()
  temp11 = re.sub('STAT:DEV:T11:TEMP:SIG:TEMP:', '', temp11)
  temp11 = temp11[:-2]
  	
  try:
    _socket.shutdown(socket.SHUT_RDWR)
  except Exception as e:
    pass
  _socket.close()
  _socket = None
  
  ##### T12 #####
  
  _address = "Triton-Dr.mer.utexas.edu"
  port = 33576
  _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  _socket.connect((_address, port))
  
  _socket.sendall('READ:DEV:T12:TEMP:SIG:TEMP\r\n'.encode())
  temp12 = _socket.recv(1024)
  temp12 = temp12.decode()
  temp12 = re.sub('STAT:DEV:T12:TEMP:SIG:TEMP:', '', temp12)
  temp12 = temp12[:-2]
  	
  try:
    _socket.shutdown(socket.SHUT_RDWR)
  except Exception as e:
    pass
  _socket.close()
  _socket = None
  
  ##### T13 #####
  
  _address = "Triton-Dr.mer.utexas.edu"
  port = 33576
  _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  _socket.connect((_address, port))
  
  _socket.sendall('READ:DEV:T13:TEMP:SIG:TEMP\r\n'.encode())
  temp13 = _socket.recv(1024)
  temp13 = temp13.decode()
  temp13 = re.sub('STAT:DEV:T13:TEMP:SIG:TEMP:', '', temp13)
  temp13 = temp13[:-2]
  	
  try:
    _socket.shutdown(socket.SHUT_RDWR)
  except Exception as e:
    pass
  _socket.close()
  _socket = None
  
  ##### T14 #####
  
  _address = "Triton-Dr.mer.utexas.edu"
  port = 33576
  _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  _socket.connect((_address, port))
  
  _socket.sendall('READ:DEV:T14:TEMP:SIG:TEMP\r\n'.encode())
  temp14 = _socket.recv(1024)
  temp14 = temp14.decode()
  temp14 = re.sub('STAT:DEV:T14:TEMP:SIG:TEMP:', '', temp14)
  temp14 = temp14[:-2]
  	
  try:
    _socket.shutdown(socket.SHUT_RDWR)
  except Exception as e:
    pass
  _socket.close()
  _socket = None
  
  ##### T15 #####
  
  _address = "Triton-Dr.mer.utexas.edu"
  port = 33576
  _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  _socket.connect((_address, port))
  
  _socket.sendall('READ:DEV:T15:TEMP:SIG:TEMP\r\n'.encode())
  temp15 = _socket.recv(1024)
  temp15 = temp15.decode()
  temp15 = re.sub('STAT:DEV:T15:TEMP:SIG:TEMP:', '', temp15)
  temp15 = temp15[:-2]
  	
  try:
    _socket.shutdown(socket.SHUT_RDWR)
  except Exception as e:
    pass
  _socket.close()
  _socket = None
  
  ##### T16 #####
  
  _address = "Triton-Dr.mer.utexas.edu"
  port = 33576
  _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  _socket.connect((_address, port))
  
  _socket.sendall('READ:DEV:T16:TEMP:SIG:TEMP\r\n'.encode())
  temp16 = _socket.recv(1024)
  temp16 = temp16.decode()
  temp16 = re.sub('STAT:DEV:T16:TEMP:SIG:TEMP:', '', temp16)
  temp16 = temp16[:-2]
  	
  try:
    _socket.shutdown(socket.SHUT_RDWR)
  except Exception as e:
    pass
  _socket.close()
  _socket = None
    
  ##### Data List #####
  data = [curr_time, temp1, temp2, temp3, temp4, temp5, temp6, temp7, temp8, temp9, temp10, temp11, temp12, temp13, temp14, temp15, temp16]
  data = [float(i) for i in data]
  print(data)
  return data
  
##### Write to file #####
def write_hdf5(data):
  curr_date = datetime.today().strftime('%d.%m.%Y')
  curr_month = datetime.today().strftime('%m.%Y')
  
  with h5py.File('TritonTempLog.hdf5', 'a') as f:
    if curr_month+'/'+curr_date in f:
      dset = f[curr_month+'/'+curr_date]
      curr_size = dset.shape[0]
      new_size = curr_size+1
      dset.resize((new_size, 17))
      for i in range(0, 17):
        dset[new_size-1, i] = data[i]
    else:
      month = f.create_group(curr_month)
      dset = month.create_dataset(curr_date, (1, 17), maxshape=(1500, 17), dtype='f')
      for i in range(0, 17):
        dset[0, i] = data[i]
        
while True:
  print('tick')
  data = gather_temps()
  write_hdf5(data)
  time.sleep(5 - time.time() % 5)