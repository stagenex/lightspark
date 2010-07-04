#!/usr/bin/python2.6

import extractor
import sys

def stripDown(x):
  return x.strip() + "\n"

class Generator():
  def __init__(self, parser, namespaces, inputFileName):
    self.parser = parser
    self.className = parser.className
    self.namespaces = namespaces
    self.methods = parser.get_methods()
    self.descs = parser.get_methods_desc()
    self.events = parser.get_events()
    self.eventsDesc = parser.get_events_desc()
    if len(self.methods) != len(self.descs) and len(self.descs) > len(self.methods):
	sys.stderr.write("[ERROR]: Mismatch in description/method number in "+inputFileName+"\n") 
	sys.stderr.write("       -- Dump of the extracted methods --\n")
	for i in range(0, len(self.methods)):
	  sys.stderr.write(str(i)+" : "+ self.methods[i].encode("utf8") + "\n")
	sys.stderr.write("\n       -- Dump of the extracted descriptions --\n")
	for i in range(0, len(self.descs)):
	  sys.stderr.write(str(i)+" : "+ self.descs[i].encode("utf8") + "\n")
    if len(self.methods) != len(self.descs) and len(self.descs) == 0:
	sys.stderr.write("[WARNING]: No description extracted for "+inputFileName+"\n") 
    if len(self.methods) != len(self.descs) and len(self.descs) < len(self.methods):
	sys.stderr.write("[ERROR]: Missing some description for "+inputFileName+", please check the file manually\n") 
    
  def out_desc(self, indent, desc, start = "/**"):
    s = indent + start + " " + (indent + "    ").join(map(stripDown, desc.split("\n"))) + "\n" + indent + "*/\n"
    # Remove empty lines
    return "\n".join([ line for line in s.split("\n") if len(line.strip())])+"\n"
    
  def filter_class(self, className):
    if className.find("public") == -1:
      return "#error Please fix this file manually (from: "+className+")\n"
    return "class DLL_PUBLIC " + className.split(" ")[-1]
    
  def filter_hierarchy(self, className):
    if len(className.strip()) == 0 or className.strip() == "Object":
      return "public ASObject"
    else: 
      return "public "+ className.strip()
      
  def out_class(self, indent):
    s = ""
    s+= self.out_desc(indent, self.parser.get_description())
    s+= indent + self.filter_class(self.parser.get_signature()) + "\n"
    s+= indent + "    : " + self.filter_hierarchy(self.parser.get_inheritance()) + "\n"
    s+= indent + "{\n"
    s+= indent + "    CLASSBUIDABLE(" + self.className + ");\n"
    return s;

  def out_member(self, indent, desc, method):
    s = self.out_desc(indent, desc)
    s += indent + "// "+ self.out_param(method)  + ";\n"
    s += indent + "ASMEMBER("+ self.out_param(method).split(" ")[0] + ", " + self.out_param(method).split(" ")[1]  + ");\n"
    return s
    
  def out_method(self, indent, desc, method):
    s = self.out_desc(indent, desc)
    name = method.split("(")[0].split(" ")[-1]
    isStatic = ""
    if method.find("static") != -1:
      isStatic = "static "
    returnType = method.split(":")[-1]

    params = method.split("(")[-1].split(")")[0]
    args = []
    for param in params.split(","):
      args.append(self.out_param(param))
    
    s += indent + "// " + isStatic + returnType.strip() + " " 
    s += name.strip() + "(" + ", ".join(args) + ");\n"

    s += indent + "const AS3OBJ_TYPE "+ name.strip()+ "_Types[];\n"
    s += indent + "ASFUNCTION_EX("+ name.strip() + ");\n"
    return s

  def out_param(self, method):
    type = method.split(":")[-1].strip()
    name = method.split(":")[0].split(" ")[-1]
    return type.split(" ")[0].strip() + " " + name.strip() + " ".join(type.split(" ")[1:])



  def out_const(self, indent, desc, method):
    s = self.out_desc(indent, desc)
    name = method.split("(")[0].split(" ")[-1]
    params = method.split("(")[-1].split(")")[0]
    args = []
    for param in params.split(","):
      args.append(self.out_param(param))
    s += indent + name.strip() + "(" + ", ".join(args) + "); \n"
    s += indent + "const AS3OBJ_TYPE "+ name.strip()+ "_Types[];\n"
    s += indent + "ASFUNCTION_EX(_constructor); \n"
    
    return s

  def out_param_body(self, method):
    type = method.split(":")[-1].strip()
    name = method.split(":")[0].split(" ")[-1]
    return type.split(" ")[0].strip()

  def out_const_body(self, indent, desc, method):
    s = self.out_desc(indent, desc, "/*")
    name = method.split("(")[0].split(" ")[-1]
    params = method.split("(")[-1].split(")")[0]
    args = []
    argsStr = []
    for param in params.split(","):
      args.append(self.out_param_body(param))
      argsStr.append("REG_"+self.out_param_body(param).upper())
      
    s += indent + "AS3OBJ_TYPE "+self.className+"::"+name+"_Types[] = {" + ", ".join(argsStr) + "}; \n"
    s += indent + "ASFUNCTION_EXBODY("+self.className+ ", _constructor) \n"
    s += indent + "{\n"
    for i in range(0,len(args)):
      s += indent + "    CHECK_ARG(args["+str(i)+"], "+args[i]+");\n"
    s += "\n" + indent + "    // Your code here\n"
    s += indent + "}\n\n"
    return s

  def out_method_body(self, indent, desc, method):
    s = self.out_desc(indent, desc, "/*")
    name = method.split("(")[0].split(" ")[-1].strip()
    params = method.split("(")[-1].split(")")[0]
    args = []
    argsStr = []
    for param in params.split(","):
      args.append(self.out_param_body(param))
      argsStr.append(self.out_param_body(param))
      

    s += indent + "AS3OBJ_TYPE "+self.className+"::"+name+"_Types[] = {" + ", ".join(argsStr) + "}; \n"
    s += indent + "ASFUNCTION_EXBODY("+self.className+ ", "+ name +") \n"
    s += indent + "{\n"
    for i in range(0,len(args)):
      s += indent + "    CHECK_ARG(args["+str(i)+"], "+args[i]+");\n"
    s += "\n" + indent + "    // Your code here\n"
    s += indent + "}\n\n"
    return s
    

  def get_header(self, inputFileName):
    s = "#ifndef hpp_CPP_" + self.className + "_CPP_hpp\n"
    s += "#define hpp_CPP_" + self.className + "_CPP_hpp\n"
    s += "\n"
    s += "// Automatically generated from file: " + inputFileName + "\n\n"  
    indentLevel = 0
    for namespace in self.namespaces:
      s+= "".ljust(indentLevel*4) + "namespace " + namespace + "\n"
      s+= "".ljust(indentLevel*4) + "{\n"
      indentLevel += 1
      
    # Then add the class description
    indent = "".ljust(indentLevel * 4)
    s+= self.out_class(indent)
    methods = self.methods
    descs = self.descs
    inMember = False
    isConstructor = False
    inIndent = "".ljust(indentLevel * 4 + 4)
    for i in range(0, len(methods)):
      method = methods[i]
      try:
	desc = descs[i]
      except:
	desc = ""
	pass
      if method.find("function") == -1:
	if inMember != True:
	  s+= "\n"+ indent + "// Members\n" + indent + "private:\n"
	  inMember = True
      else: 
        if method.find(self.className+"(") != -1:
          s+= "\n"+ indent + "// Construction\n" + indent + "public:\n"
          isConstructor = True
        else:
	  if inMember:
	    s+= "\n"+ indent + "// Interface\n" + indent + "public:\n"
          inMember = False
          isConstructor = False
      
      if isConstructor:
	s+= self.out_const(inIndent, desc, method)
      elif inMember:
        s+= self.out_member(inIndent, desc, method)
      else:
	s+= self.out_method(inIndent, desc, method)
    
    writtenSeparation = False
    for i in range(0, len(self.events)):
      event = self.events[i]
      desc = self.eventsDesc[i]
      if writtenSeparation == False:
	 s+= "\n"+ indent + "// Events\n" + indent + "public:\n" + inIndent + "ASEVENT_START\n"
	 writtenSeparation = True
      s+= self.out_desc(inIndent, desc);
      s+= inIndent + "ASEVENT(" + event.split('.')[-1].strip() + ");\n"
    if writtenSeparation:
      s+= inIndent + "ASEVENT_END\n"
      
    
    s+= indent + "};\n"
    for namespace in self.namespaces:
      s+= "".ljust(indentLevel * 4 - 4) + "}\n"
      indentLevel -= 1
    s += "static const AS3OBJ_TYPE DLL_PUBLIC REG_"+self.className.upper()+";\n"
    s+= "\n#endif\n"
    return s
  
  def get_source(self):
    s = "// We need our declaration\n#include \"" + self.className + "\"\n"
    s += "\n"
    
    s += "const AS3OBJ_TYPE DLL_PUBLIC REG_"+self.className.upper()+" = " + "globalIDIdentifier++;\n"
    
    indentLevel = 0
    for namespace in self.namespaces:
      s+= "".ljust(indentLevel*4) + "namespace " + namespace + "\n"
      s+= "".ljust(indentLevel*4) + "{\n"
      indentLevel += 1
      
    # Then add the class description
    indent = "".ljust(indentLevel * 4)
    inIndent = "".ljust(indentLevel * 4 + 4)
    methods = self.methods
    descs = self.descs
    for i in range(0, len(methods)):
      method = methods[i]
      try:
	desc = descs[i]
      except:
	desc = ""
	pass
      if method.find("function") == -1:
          continue    
      if method.find(self.className+"(") != -1:
	  s += self.out_const_body(indent, desc, method)
      else:
	  s += self.out_method_body(indent, desc, method)

    writtenSeparation = False
    for i in range(0, len(self.events)):
      event = self.events[i]
      desc = self.eventsDesc[i]
      if writtenSeparation == False:
	 s+= indent + "ASEVENT_START_BODY(" + self.className + ")\n"
	 writtenSeparation = True
      s+= self.out_desc(indent, desc, "/*");
      s+= indent + "ASEVENT_BODY(" + self.className + ", " + event.split('.')[-1].strip() + ");\n"
    if writtenSeparation:
      s+= indent + "ASEVENT_END_BODY\n"

    
    for namespace in self.namespaces:
      s+= "".ljust(indentLevel * 4 - 4) + "}\n"
      indentLevel -= 1
    return s