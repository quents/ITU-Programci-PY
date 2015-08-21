from html.parser import HTMLParser

class ITU_HTMLParser(HTMLParser):
    foundClassTable=False
    parsedData=[]
    classInfo=[]
    ITU_HTMLParser_DEPCODEMODE = 0
    ITU_HTMLParser_CLASSMODE = 1
    def __init__(self,parsermode):
        self.mode = parsermode
        super(ITU_HTMLParser,self).__init__()

    def handle_starttag(self, tag, attrs):
        if self.mode == self.ITU_HTMLParser_DEPCODEMODE:
            if(tag == 'option'):
                for attr in attrs:
                    if attr[0] == 'value':
                        if attr[1] != '':
                            self.parsedData.append(attr[1])
        elif self.mode == self.ITU_HTMLParser_CLASSMODE:
            if tag == 'table' and attrs != [] and attrs[0][0] == 'class' and attrs[0][1] == 'dersprg':
                if not self.foundClassTable:
                    self.foundClassTable = True
            elif self.foundClassTable and tag == 'tr':
                self.classInfo = []

    def handle_data(self,data):
        if self.foundClassTable:
            self.classInfo.append(data)

    def handle_endtag(self,tag):
        if self.foundClassTable and tag =='tr':
            self.parsedData.append(self.classInfo)
        if self.foundClassTable and tag == 'table':
            self.foundClassTable = False

class ITUSIS_Parser:
    def __init__(self):
        import requests
        self.requests = requests

    def getDepartmentCodes(self):
        html = self.requests.get('http://www.sis.itu.edu.tr/tr/ders_programlari/LSprogramlar/prg.php').text
        self.parser = ITU_HTMLParser(ITU_HTMLParser.ITU_HTMLParser_DEPCODEMODE)
        self.parser.feed(html)
        return self.parser.parsedData

    def getClasses(self):
        for dep in self.getDepartmentCodes():
            html = self.requests.get('http://www.sis.itu.edu.tr/tr/ders_programlari/LSprogramlar/prg.php?fb='+dep).text
            self.parser = ITU_HTMLParser(ITU_HTMLParser.ITU_HTMLParser_CLASSMODE)
            self.parser.feed(html)
            #print(dep)
            print(self.parser.parsedData)
