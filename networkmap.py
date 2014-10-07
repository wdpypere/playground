#!/usr/bin/python

import gv, re
from vsc.quattor.quattor import Quattor
engines = ['dot', 'fdp', 'neato', 'sfdp', 'twopi', 'circo']


class mygraph(object):
    def __init__(self):
        self.graphhandler = gv.graph("whatever")
        gv.setv(self.graphhandler, "overlap", "false")
            
    def add_node(self, nodename):
        print "adding node: " + nodename
        gv.node(self.graphhandler, nodename) 
        
    def add_connection(self, node1, node2):
        print "adding connection between " + node1 + " and " + node2 
        gv.edge(self.graphhandler, str(node1), str(node2))
        
    def generate_png(self, dotfile = "test.dot", pngfile = "test.png", drawengine = "dot"):
        dot = gv.write(self.graphhandler, dotfile)
        gvv = gv.read(dotfile)
        gv.layout(gvv, drawengine)
        gv.render(gvv,'png', pngfile)

def main():
    mygraphs = mygraph()

    quattor = Quattor(re.compile('[a-ln-z].*\.muk\..*'))
    for node, pprofile in Quattor.allparsedprofiles(quattor):
        mygraphs.add_node(node)
        pprofile.get_icinga_parents()
        for parent in pprofile.icingaparents:
            print node + ' - ' + parent
            mygraphs.add_connection(parent, node)
    
    #mygraphs.generate_png()
    for drawengine in engines:
        print drawengine
        mygraphs.generate_png(drawengine + '.dot', drawengine + '.png', drawengine)
if __name__ == '__main__':
    main()
