import pprint
pp = pprint.PrettyPrinter(indent=5)
from components import *

buf = Buffer(5)
buf.push({"p":0.1, "path":["1","2"]},"3")

pp.pprint(buf.getBuffer())

buf.push({"p":0.2, "path":["1","2"]},"6")
buf.push({"p":0.7, "path":["1","2"]},"9")
buf.push({"p":0.5, "path":["1","2"]},"6")
buf.push({"p":0.3, "path":["1","2"]},"6")
buf.push({"p":0.5, "path":["1","2"]},"6")
buf.push({"p":0.7, "path":["1","2"]},"6")
buf.push({"p":0.2, "path":["1","2"]},"6")
buf.push({"p":0.5, "path":["1","2"]},"6")
buf.push({"p":0.3, "path":["1","2"]},"6")
buf.push({"p":0.5, "path":["1","2"]},"6")
buf.push({"p":0.7, "path":["1","2"]},"6")
buf.push({"p":0.2, "path":["1","2"]},"6")
buf.push({"p":0.5, "path":["1","2"]},"6")
buf.push({"p":0.3, "path":["1","2"]},"6")
buf.push({"p":0.5, "path":["1","2"]},"6")
buf.push({"p":0.7, "path":["1","2"]},"6")
buf.push({"p":0.2, "path":["1","2"]},"6")
buf.push({"p":0.5, "path":["1","2"]},"6")
buf.push({"p":0.3, "path":["1","2"]},"6")
buf.push({"p":0.5, "path":["1","2"]},"6")
buf.push({"p":0.7, "path":["1","2"]},"6")
buf.push({"p":0.2, "path":["1","2"]},"6")



pp.pprint(buf.getBuffer())
pp.pprint(buf.getPath(3))


