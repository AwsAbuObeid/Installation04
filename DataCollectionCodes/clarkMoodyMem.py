from websocket import create_connection

ws = create_connection("wss://bitcoin.clarkmoody.com/dashboard/ws")
ws.send("""{"op":"c","ch":"","pl":{"c":"4de43be4236035c5","s":"9f6e08f07c263998"}}""")
ws.send("""{"op":"sub","ch":"mod"}""")
ws.send("""{"op":"sub","ch":"sta"}""")
ws.send("""{"op":"sub","ch":"sys"}""")
ws.send("""{"op":"sub","ch":"upd"}""")

ws.recv()
ws.recv()
ws.recv()
ws.recv()
x = json.loads(ws.recv())

mem = x["pl"]["mt"]