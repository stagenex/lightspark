#!/usr/bin/python2.6

from lxml import etree
from StringIO import StringIO


      
class DocParser():
  def __init__(self, className):
    "Parse a xml document"
    self.parser = etree.HTMLParser()
    self.className = className
    self.events = []
    self.eventsDesc = []
    
  def parse(self, doc):
    self.doc = etree.parse(StringIO(doc), self.parser)
    # Throw the examples here, as it pollutes the parsing
    for element in self.doc.xpath("//div[@class='exampleHeader']/following::*"):
      element.getparent().remove(element)
    for element in self.doc.xpath("//div[@class='seeAlso']/following-sibling::*"):
      element.getparent().remove(element)
    for element in self.doc.xpath("//div[@class='detailBody' and contains(span, 'Example')]/span[@class='label']/following-sibling::*"):
      element.getparent().remove(element)
    self.events = self.doc.xpath("//div[@class='detailSectionHeader' and contains(text(), 'Event Detail')]/following::div[@class='detailBody']/a[2]/code/text()")
    self.eventsDesc = self.get_events_desc_internal(self.doc.xpath("//div[@class='detailSectionHeader' and contains(text(), 'Event Detail')]/following::div[@class='detailBody']/p[4]"))
    # Then remove them, as it confuse the method parser 
    for element in self.doc.xpath("//div[@class='detailSectionHeader' and contains(text(), 'Event Detail')]/following::*"):
      element.getparent().remove(element)

    expr = "//div[@class='detailSectionHeader' and contains(text(), 'Event Detail')]/following::*"


    
  def get_elementWithAttribute(elements, attributes):
    for element in elements:
       if (element.getAttribute(attributes[0]) == attributes[1]):
	 return element
	 
    return null	 
	
  def get_first_text(element):
     s = ""
     for child in element.childNodes:
       if child.nodeType == child.TEXT_NODE:
	 s += child.nodeValue
	 return s
	
     return s
  
  def get_signature(self):
    expr = '//td[@class="classSignature"]/text()'
    return self.doc.xpath(expr)[0]    

  def get_inheritance(self):
    expr = '//td[@class="inheritanceList"]/a/text()'
    return self.doc.xpath(expr)[0]    
  
  def get_description(self):
    expr = '//div[@class="MainContent"]/text()|//div[@class="MainContent"]/code/text()'
    return "".join(self.doc.xpath(expr))    
  
  def get_methods(self):
    expr = "//div[@class='detailBody']/code"
    elements = self.doc.xpath(expr)
    methodList = []
    s = ""
    for element in elements:
      txt = " ".join(element.itertext())
      if txt.strip().find(" get ") != -1 or txt.strip().find(" set ") != -1:
	 continue
      if txt.strip().find("<") != -1 or txt.strip().find(">") != -1: # or txt.strip().find(".") != -1:
	 # Generics are supported, but only with interfaces
	 if txt.strip().find(".<") == -1:
	   continue
      if txt.strip().find(":") == -1 and txt.strip().find("(") == -1:
	 continue
      if txt.strip().find(" ") == -1 and txt.strip().find(":") == -1:
	 continue
      if txt.strip()[0] == "(":
	 continue
       
      if len(s):
         methodList.append(s)
      s = txt
    if len(s):
      methodList.append(s)
    return methodList

  def get_events_desc_internal(self, events):
    eventList = []
    lastParent = None
    s = ""
    for element in events:
      txt = " ".join(element.itertext())
      if element.getparent() != lastParent:
         lastParent = element.getparent()
	 if len(s):
            eventList.append(s)
            s = ""
      else:
	 if len(txt.strip()) == 0:
	    continue
         
      s += txt
    if len(s):
      eventList.append(s)
    
    return eventList
    
  def get_methods_desc(self):
    expr = "//div[@class='detailBody']/code/following-sibling::p[position() >= 2]"
    elements = self.doc.xpath(expr)
    methodList = []
    lastParent = None
    s = ""
    for element in elements:
      txt = " ".join(element.itertext())
      if txt.strip() == "See also" or txt.strip() == "Parameters" or txt.strip()[0:5] == "Note:": 
         continue
      if element.getparent() != lastParent:
         lastParent = element.getparent()
	 if len(s):
            methodList.append(s)
            s = ""
      else:
	 if len(txt.strip()) == 0:
	    continue
         
      s += txt
    if len(s):
      methodList.append(s)
    
    return methodList
    
  def get_events(self):
    return self.events
  def get_events_desc(self):
    return self.eventsDesc