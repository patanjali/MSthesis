'''
Created on Oct 6, 2015

@author: Subhojyoti
'''

import math
import random
import numpy

class MOSS(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        
        
    
    def upperBound(self, step, numPlays):
        #return math.sqrt(2 * math.log(step + 1) / numPlays)
        return math.sqrt(max(math.log((self.numRounds)/(1.0*self.numActions*numPlays)),0.0) / numPlays)
        #return math.sqrt(max(math.log((step + 1.0)/(self.numActions*numPlays)),0.0) / numPlays)
    
     
    def rewards(self,choice):
        
        #return sum(numpy.random.binomial(1,self.means[choice],1))/1.0
        return random.gauss(self.means[choice],self.variance[choice])
        
    def moss(self,numActions):
    
        #Set the environment
        self.numActions=numActions
        
        self.payoffSums = [0] * self.numActions
        self.numPlays = [0] * self.numActions
        self.ucbs = [0] * self.numActions
        self.upbs = [0] * self.numActions
        #self.numRounds = self.numActions*self.numActions*self.numActions
        self.numRounds = 300000
        #self.numRounds = self.numActions*math.pow(10,3)
        
        self.arm_reward = [0]*numActions
        
        #bestAction=arms/2
        self.bestAction=self.numActions-2
        
        
        self.means =[0.01 for i in range(self.numActions)]
        self.variance=[0.25 for i in range(self.numActions)]


        for i in range(0,1*self.numActions/3):
            self.means[i]=0.07
            self.variance[i]=0.01

        '''
        #i=(1*self.numActions)/3
        for i in range(self.numActions/3):
            self.means[i]=0.01
        '''
        '''
        i=(2*self.numActions)/3
        while i<self.numActions:
            self.means[i]=0.4
            i=i+1
        '''
        self.means[self.bestAction]=0.09
        self.variance[self.bestAction]=0.25
        
        print self.means
        
        # initialize empirical sums
        
        cumulativeReward = 0
        bestActionCumulativeReward = 0
        self.actionRegret=[]
        t=1
        
        for i in range(self.numActions):
            theReward = self.rewards(i)
            #self.numPlays[i]=self.numPlays[i]+1
            
            action=i
            theReward = self.rewards(action)
            #print theReward,action
            self.arm_reward[action]=self.arm_reward[action]+theReward
            self.numPlays[action] += 1
            self.payoffSums[action] += theReward
            
            #f1.writelines("ucbs: (%s)" % (', '.join(["%.8f" % ucb for ucb in ucbs])))
            #f1.writelines("\tupbs: (%s)\n" %( ', '.join(["%.8f" % upb for upb in upbs])))
            
            #yield action, theReward, ucbs
            
            
            
            cumulativeReward += theReward
            bestActionCumulativeReward += theReward if action == self.bestAction else self.rewards(self.bestAction)
            regret = bestActionCumulativeReward - cumulativeReward
            
            self.actionRegret.append(regret)
            t=t+1
            
        #t = numActions    
        
        t=self.numActions
        while True:
            ucbs = [(self.payoffSums[i] / self.numPlays[i]) + self.upperBound(t, self.numPlays[i]) for i in range(self.numActions)]
            #upbs = [self.upperBound(t, self.numPlays[i]) for i in range(self.numActions)]
            #print "upbs"
            #print upbs
            #print ucbs
            #getting the maximum of the ucbs
            action = max(range(self.numActions), key=lambda i: ucbs[i])
            theReward = self.rewards(action)
            #print theReward,action
            self.arm_reward[action]=self.arm_reward[action]+theReward
            self.numPlays[action] += 1
            self.payoffSums[action] += theReward
            
            #f1.writelines("ucbs: (%s)" % (', '.join(["%.8f" % ucb for ucb in ucbs])))
            #f1.writelines("\tupbs: (%s)\n" %( ', '.join(["%.8f" % upb for upb in upbs])))
            
            #yield action, theReward, ucbs
            
            
            
            cumulativeReward += theReward
            bestActionCumulativeReward += theReward if action == self.bestAction else self.rewards(self.bestAction)
            regret = bestActionCumulativeReward - cumulativeReward
            
            self.actionRegret.append(regret)
            
            
            if t%10000==0:
                print t,regret
            
            
            t = t + 1
            
            #print t
            
            
            
            if t>=self.numRounds:
                break
    
        action=max(range(self.numActions), key=lambda i: self.arm_reward[i])
        #print self.arm_reward

        
        f = open('NewExpt/expt2/testRegretMOSS01.txt', 'a')
        for r in range(len(self.actionRegret)):
            f.write(str(self.actionRegret[r])+"\n")
        f.close()
        
        return cumulativeReward,bestActionCumulativeReward,regret,action,t
        

if __name__ == "__main__":
    
    wrong=0
    i=100
    while i<=100:
        turn=0
        for j in range(turn,100):
            
            random.seed(i+j)
            obj=MOSS()
            cumulativeReward,bestActionCumulativeReward,regret,arm,timestep=obj.moss(i)
            if arm!=i-2:
            #if arm!=i/2:
                wrong=wrong+1
            print "turn: "+str(turn+1)+"\twrong: "+str(wrong)+"\tarms: "+str(i)+"\tbarm: "+str(arm)+"\tReward: "+str(cumulativeReward)+"\tbestCumReward: "+str(bestActionCumulativeReward)+"\tregret: "+str(regret)
            f = open('NewExpt/expt2/testMOSS01.txt', 'a')
            f.writelines("arms: %d\tbArms: %d\ttimestep: %d\tregret: %d\tcumulativeReward: %.2f\tbestCumulativeReward: %.2f\n" % (i, arm, timestep, regret, cumulativeReward, bestActionCumulativeReward))
            f.close()
            
            turn=turn+1
        i=i+10
        
