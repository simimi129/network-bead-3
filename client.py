import sys, struct, socket, random
port = sys.argv[2]
host = sys.argv[1]
serv = (host, port)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(serv)
start = 1
finish = 100
ops = ['>', '<']
packer = struct.Struct('c I')
end = False
while not end:
  if start != end:
    op = random.choice(ops)
    m = (end + start) / 2
  else:
    op = "="
    m = start
  data = packer.pack(op.encode(), m)
  sock.sendall(data)
  message = sock.recv(packer.size)
  res = packer.unpack(message)
  r = res[0].decode()
  if r == 'Y':
    end = True
  elif r == 'K' or r == "V":
    end = True
  elif r == 'I':
    if op == ">":
      start = m + 1 
    else:
      finish = m - 1
  elif r == 'N':
    if op == ">":
      finish = m 
    else:
      start = m
sock.close()
