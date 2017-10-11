'''
Created on Jan 27, 2016

@author: Subhojyoti
'''

import math
import random
import numpy
import fileinput

class CreateEnvironment(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
    


    def readenv(self):
        data=[]
        filename="env/GR3.txt"
        for line in fileinput.input([filename]):

            try:
                line1 = [line.split(", ") or line.split("\n") ]
                #print numpy.shape(line1)
                #print line1
                take=[]
                for i in range(len(line1[0])):
                    take.append(float(line1[0][i]))
                #print take
                data.append(take)
            except ValueError,e:
                print e
        #print data
        self.means=(data[0])
        self.variance=(data[1])

    def create(self,numActions):
    
        #Set the environment

        self.numActions=numActions
        self.bestAction =  self.numActions - 2

        '''
        self.means =[]
        self.variance=[]
        self.readenv()
        '''

        self.means =[0.09 for i in range(self.numActions)]
        self.variance=[0.0 for i in range(self.numActions)]


        for i in range(0, int((0.5)*self.numActions)):
            self.variance[i]=numpy.random.uniform(0.0,0.05)

        for i in range(int((0.5)*self.numActions), self.numActions):
            self.variance[i]=numpy.random.uniform(0.19,0.24)

        for i in range(10, self.numActions):
            self.means[i]=numpy.random.uniform(0.09,0.09)

        self.means[self.bestAction] = 0.1
        self.variance[self.bestAction] = 0.25

        f = open('env/env3.txt', 'w')
        f.writelines("%s\n" % (', '.join(["%.3f" % i for i in self.means])))
        f.writelines("%s\n" % (', '.join(["%.3f" % i for i in self.variance])))
        f.close()


        print self.means
        print self.variance




        

if __name__ == "__main__":

        numActions=100
        obj=CreateEnvironment()
        obj.create(numActions)

                