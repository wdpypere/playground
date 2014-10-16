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
        
    def generate_png(self, dotfile = "test.dot", pngfile = "test.png", drawengine = "twopi"):
        dot = gv.write(self.graphhandler, dotfile)
        gvv = gv.read(dotfile)
        gv.layout(gvv, drawengine)
        gv.render(gvv,'png', pngfile)
        
def handle_node():
    pass

def handle_default(graph, node, parent):
    graph.add_node(node)
    graph.add_connection(parent, node)
    
def main():
    actions = {
        'node': handle_node,
    }


    mygraphs = mygraph()
    quattor = Quattor(re.compile('[a-ln-z].*\.muk\..*'))

    for node, pprofile in Quattor.allparsedprofiles(quattor):
        pprofile.get_icinga_parents()
        action_taken = False
        for key in actions:
            if node.startswith(key):
                actions[key]()
                action_taken = True
                break

        if not action_taken:
           handle_default(mygraphs, node, pprofile.icingaparents[0])


#        if node.startswith("node") or node.startswith("ilo") or node.startswith("bmc") or node.startswith("imm"):
#            pass
#        else:
#            mygraphs.add_node(node)
#            pprofile.get_icinga_parents()
#            for parent in pprofile.icingaparents:
#                print node + ' - ' + parent
#                mygraphs.add_connection(parent, node)
    
    mygraphs.generate_png()
    #for drawengine in engines:
    #    print drawengine
    #    mygraphs.generate_png(drawengine + '.dot', drawengine + '.png', drawengine)
if __name__ == '__main__':
    main()
