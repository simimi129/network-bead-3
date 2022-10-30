import sys, struct, socket, select, random
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setblocking(0)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
port = sys.argv[2]
host = sys.argv[1]
serv = (host, port)
server.bind(serv)
server.listen(1)
end = False
inp = [server]
numToGuess = random.randint(1, 100)
packer = struct.Struct('c I')
while inp:
  timeout = 1
  r, w, ex = select.select(inp, inp, inp, timeout)
  if not (r or w or ex):
    continue
  for rec in r:
    try:
      if rec is server:
        client, client_address = rec.accept()
        client.setblocking(0)
        inp.append(client)
      else:
        data = rec.recv(200)
        if data:
          guessedNum = packer.unpack(data)
          num = guessedNum[1]
          op = guessedNum[0]
          res  = packer.pack(b'V', 0)
          if end:
            res = packer.pack(b'V', 0)
          else:
            operator = op.decode()
            term = False
            res = ""
            if operator == '=':
              if num == numToGuess:
                c = 'K'
              else:
                c = 'Y'
                term = True
                res = packer.pack(c.encode(), 0)
            elif operator == '<':
              if num < numToGuess:
                c = 'N'
              else:
                c = 'I'
                res = packer.pack(c.encode(), 0)
            elif operator == '>':
              if num > numToGuess:
                c = 'N'
              else:
                c = 'I'
                res = packer.pack(c.encode(), 0)
                switch = res
                if term:
                  end = True
              rec.sendall(res)
            else:
              inp.remove(rec)
              if rec in w:
                w.remove(rec)
                rec.close()
    except socket.error:
      inp.remove(rec)
      if rec in w:
        w.remove(rec)
        rec.close()





