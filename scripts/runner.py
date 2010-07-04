#!/usr/bin/python2.6

import extractor
import sys
import os
import generator

inputFile = file(sys.argv[1]).read()
outputPath = sys.argv[2]
outputName = sys.argv[1].rsplit("/", 1)[-1].split(".html")[0]
outputHeader = file(outputPath + "/" + outputName + ".hpp", "wb")
outputSource = file(outputPath + "/" + outputName + ".cpp", "wb")

parser = extractor.DocParser(outputName)
parser.parse(inputFile)

absPath = os.path.abspath(sys.argv[1])
relPath = absPath[-len(absPath) + len(os.path.commonprefix([absPath, os.getcwd()])):]
namespaces = [ item for item in relPath.split("/") if len(item.strip()) and item.find(".html") == -1]
generator = generator.Generator(parser, namespaces, sys.argv[1])

try:
   outputHeader.write(generator.get_header(sys.argv[1]).encode("utf8"))
   outputSource.write(generator.get_source().encode("utf8"))
except:
   print "Error processing file: "+sys.argv[1]
   if (os.path.basename(sys.argv[1])[0] == "I"):
     print "It's an interface file. This parser doesn't understand it yet"
     pass
   else:
     raise
   
outputHeader.close()
outputSource.close()
print "Done writing to "+outputPath+"/"+outputName+".{h,c}pp"


#print parser.get_signature()
#print parser.get_inheritance()
#print parser.get_description()
#methods = parser.get_methods()
#descs = parser.get_methods_desc()
#for i in range(0, len(methods)):
  #method = methods[i]
  #desc = descs[i]
  #print "/** " + desc + "*/"
  #print method

