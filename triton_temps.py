# Pulls data every 5 seconds from a dilution fridge through SSH and stores it in an hdf5 dataset.

def gather_temps():
  ##### Time #####
  
  _address = "Triton.utexas.edu" #Fake address
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
