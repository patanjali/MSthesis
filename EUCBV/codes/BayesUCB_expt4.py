'''
Created on Oct 6, 2015

@author: Subhojyoti
'''

import math
import random
import numpy
from scipy import special
from scipy.stats import beta
from scipy.stats import norm
from scipy.stats import t
#from random import betavariate
#from scipy.special import btdtri
import scipy
import fileinput

class ucb1_2(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''

    
     
    def rewards(self,choice):
        return random.gauss(self.means[choice],self.variance[choice])
        #return sum(numpy.random.binomial(1,self.means[choice],1))/1.0

    def readenv(self):
        data=[]
        filename="env/env3.txt"
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
        
    def ucb1(self,numActions):
    
        #Set the environment
        self.numActions=numActions
        
        self.payoffSums = [0] * self.numActions
        self.sqpayoffSums = [0] * self.numActions
        self.numPlays = [1] * self.numActions
        self.ucbs = [0] * self.numActions
        self.upbs = [0] * self.numActions
        self.numRounds = 400000
        #self.numRounds = 60000
        #numRounds = 250000
        
        self.arm_reward = [0]*numActions
        
        #bestAction=arms/2
        self.bestAction=self.numActions - 2
        
        #biases = [1.0 / k for k in range(5,5+numActions)]
        #means = [0.5 + b for b in biases]



        self.means=[]
        self.variance=[]
        self.readenv()

        print self.means
        
        
        # initialize empirical sums
        '''
        for i in range(self.numActions):
            self.payoffSums[i] = self.rewards(i)
            self.numPlays[i]=self.numPlays[i]+1
        '''
        
        theta=[1.0 for i in range(self.numActions)]
        cumulativeReward = 0
        bestActionCumulativeReward = 0
        self.actionRegret=[]


        self.timestep=1

        for i in range(self.numActions):
            theReward = self.rewards(i)
            #self.numPlays[i]=self.numPlays[i]+1

            action=i
            theReward = self.rewards(action)
            #print theReward,action
            self.arm_reward[action]=self.arm_reward[action]+theReward
            self.numPlays[action] += 1
            self.payoffSums[action] += theReward
            self.sqpayoffSums[action] += theReward*theReward

            #f1.writelines("ucbs: (%s)" % (', '.join(["%.8f" % ucb for ucb in ucbs])))
            #f1.writelines("\tupbs: (%s)\n" %( ', '.join(["%.8f" % upb for upb in upbs])))

            #yield action, theReward, ucbs



            cumulativeReward += theReward
            bestActionCumulativeReward += theReward if action == self.bestAction else self.rewards(self.bestAction)
            regret = bestActionCumulativeReward - cumulativeReward

            self.actionRegret.append(regret)
            self.timestep=self.timestep+1
            
        #t = numActions

        while True:
            #ucbs = [(self.payoffSums[i] / self.numPlays[i]) + self.upperBound(t, self.numPlays[i]) for i in range(self.numActions)]
            #upbs = [self.upperBound(t, self.numPlays[i]) for i in range(self.numActions)]
            #print "upbs"
            #print upbs
            #print ucbs
            #getting the maximum of the ucbs
            
            for i in range(self.numActions):
                #print random.betavariate(success[i]+1,failure[i]+1)
                #print random.betavariate(1.0 - (1.0/t),self.payoffSums[i])

                #theta[i]=beta.ppf(1.0 -(1.0/(1.0*t)),(self.payoffSums[i]+1.0),self.numPlays[i]-self.payoffSums[i]+1.0)
                #print t.ppf(1.0 -(1.0/(1.0*self.timestep)),(self.payoffSums[i]+1.0),(self.numPlays[i]-1))
                val=abs(self.sqpayoffSums[i] - ((self.payoffSums[i]*self.payoffSums[i])/(self.numPlays[i])))/(self.numPlays[i])
                #theta[i]= self.payoffSums[i]/(self.numPlays[i]) +  val*1.0* t.ppf(1.0 -(1.0/(1.0*self.timestep)),(self.payoffSums[i]+1.0),(self.numPlays[i]-self.payoffSums[i]+1.0))
                theta[i]= self.payoffSums[i]/(self.numPlays[i]) +  math.sqrt(val/self.numPlays[i])* t.ppf(1.0 -(1.0/(1.0*self.timestep)),(self.numPlays[i]))

                #theta[i]= self.payoffSums[i]/(self.numPlays[i]) +  val*1.0* t.ppf(1.0 -(1.0/(1.0*self.timestep)),(self.payoffSums[i]+1.0),(self.numPlays[i]-self.payoffSums[i]+1.0))
                #theta[i]= self.payoffSums[i]/(self.numPlays[i]+1) + (math.sqrt(self.sqpayoffSums[i]/(self.numPlays[i]+1))) * norm.ppf(1.0 -(1.0/(1.0*t)),(self.payoffSums[i]+1.0),(self.numPlays[i]-1.0))

                #theta[i]=special.betaincinv((1.0 - (1.0/(t))),success[i]+1,failure[i]+1)
                #print i,theta[i]
                #theta[i]=random.betavariate(1.0 - (1.0/t),(success[i]))
                #theta[i]=random.betavariate(success[i]+1,failure[i]+1)

            #maxq=max(range(self.numActions), key=lambda i: theta[i])
            maxq=max(theta)
            while True:
                take=random.randint(0,self.numActions-1)
                if theta[take]==maxq:
                    action=take
                    break

            #print theta,action,self.payoffSums,self.numPlays
            #print action
            #action=(1+math.floor(len(theta)*random.randint(0,self.numActions)))
            #self.posterior[arm].update(reward)
            #self.timestep += 1
            
            #def computeIndex(self, arm):
            #    return self.posterior[arm].sample()

            
            
            #action = max(range(self.numActions), key=lambda i: ucbs[i])
            theReward = self.rewards(action)


            
            #print theReward,action
            self.arm_reward[action]=self.arm_reward[action]+theReward
            self.numPlays[action] += 1
            self.payoffSums[action] += theReward
            self.sqpayoffSums[action] += theReward*theReward
            
            #f1.writelines("ucbs: (%s)" % (', '.join(["%.8f" % ucb for ucb in ucbs])))
            #f1.writelines("\tupbs: (%s)\n" %( ', '.join(["%.8f" % upb for upb in upbs])))
            
            #yield action, theReward, ucbs
            
            
            
            cumulativeReward += theReward
            bestActionCumulativeReward += theReward if action == self.bestAction else self.rewards(self.bestAction)
            regret = bestActionCumulativeReward - cumulativeReward
            
            self.actionRegret.append(regret)
            
            if self.timestep>=self.numRounds:
                break
            
            self.timestep = self.timestep + 1
            
            #print t
            
            if self.timestep%1000==0:
                print self.timestep,regret,str(max(range(self.numActions), key=lambda i: self.arm_reward[i])),str("expt5")
            
            
    
        action=max(range(self.numActions), key=lambda i: self.arm_reward[i])
        #print self.arm_reward
        

        f = open('NewExpt/expt5/testRegretBU01.txt', 'a')
        for r in range(len(self.actionRegret)):
            f.write(str(self.actionRegret[r])+"\n")
        f.close()

        return cumulativeReward,bestActionCumulativeReward,regret,action,self.timestep
        

if __name__ == "__main__":
    
    wrong=0
    i=100
    while i<=100:
        turn=0
        for turn in range(100):
            obj=ucb1_2()
            random.seed(i+turn)
            cumulativeReward,bestActionCumulativeReward,regret,arm,timestep=obj.ucb1(i)
            if arm!=i-2:
            #if arm!=i/2:
                wrong=wrong+1
            print "turn: "+str(turn+1)+"\twrong: "+str(wrong)+"\tarms: "+str(i)+"\tbarm: "+str(arm)+"\tReward: "+str(cumulativeReward)+"\tbestCumReward: "+str(bestActionCumulativeReward)+"\tregret: "+str(regret)

            f = open('NewExpt/expt5/testBU01.txt', 'a')
            f.writelines("arms: %d\tbArms: %d\ttimestep: %d\tregret: %d\tcumulativeReward: %.2f\tbestCumulativeReward: %.2f\n" % (i, arm, timestep, regret, cumulativeReward, bestActionCumulativeReward))
            f.close()

            turn=turn+1
        i=i+1
        