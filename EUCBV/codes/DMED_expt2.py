'''
Created on May 12, 2016

@author: Subhojyoti
'''


import math
import random
import numpy

class DMED(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        
    def kl(self,p,q,eps = 1e-15):
        p = max(p, eps); 
        p = min(p, 1-eps);  
        q = max(q, eps); 
        q = min(q, 1-eps);
        y = p*math.log(p/q) + (1-p)*math.log((1-p)/(1-q));
        return y
   
    
    def rewards(self,choice):
        return random.gauss(self.means[choice],self.variance[choice])
        #print sum(numpy.random.binomial(1,self.means[choice],200))/200.0
        #return sum(numpy.random.binomial(1,self.means[choice],1))/1.0
        
    def DMED(self,numActions):

        #genuine = true -> DMED, false -> DMED+(less aggressive)

        #Set the environment
        self.numActions=numActions
        
        self.N = [0] * self.numActions
        self.S = [0] * self.numActions
        self.L = [i for i in range(self.numActions)]
        
        self.payoffSums = [0] * self.numActions
        self.numPlays = [0] * self.numActions
        self.ucbs = [0] * self.numActions
        self.upbs = [0] * self.numActions
        #self.numRounds = 3000000
        self.numRounds = 300000
        #numRounds = 250000
        
        self.arm_reward = [0]*numActions
        
        #bestAction=arms/2
        self.bestAction=self.numActions-2
        
        #biases = [1.0 / k for k in range(5,5+numActions)]
        #means = [0.5 + b for b in biases]
        self.means =[0.01 for i in range(self.numActions)]
        self.variance =[0.25 for i in range(self.numActions)]


        i=(1*self.numActions)/3
        while i<self.numActions:
            self.means[i]=0.07
            self.variance[i]=0.01
            i=i+1

        '''
        i=(2*self.numActions)/3
        while i<self.numActions:
            self.means[i]=0.03
            i=i+1
        '''
        self.means[self.bestAction]=0.09
        self.variance[self.bestAction]=0.25
        
        self.genuine=False
        
        cumulativeReward = 0
        bestActionCumulativeReward = 0
        self.actionRegret=[]

        t=0

        for i in range(self.numActions):
            theReward = self.rewards(i)
            self.numPlays[i]=self.numPlays[i]+1
            
            action=i
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
            
            t = t + 1
        
        while True:
            
            
            
            if len(self.L) > 0:
                # Play action on the list and update the list
                action = self.L[0]
                #lastAction=action
                self.L1=[]
                for i in range(1,len(self.L)):
                    self.L1.append(self.L[i])
                self.L=[]
                for i in range(0,len(self.L1)):
                    self.L.append(self.L1[i])
            else:
                # Make new list an play first action
                ucbs = [(self.payoffSums[i] / self.numPlays[i])  for i in range(self.numActions)]
                c = max(range(self.numActions), key=lambda i: ucbs[i]) # Current best empirical mean
                #print c
                if (self.genuine):
                    
                    for i in range(self.numActions):
                        take=self.numPlays[i]*self.kl((self.payoffSums[i] / self.numPlays[i]), self.payoffSums[c]/self.numPlays[c])
                        if take< math.log(t/self.numPlays[i]):
                            self.L.append(i) 
                else:
                    
                    for i in range(self.numActions):
                        take=self.numPlays[i]*self.kl((self.payoffSums[i] / self.numPlays[i]),self.payoffSums[c] / self.numPlays[c])
                        if take< math.log(t):
                            self.L.append(i)
                    #self.L = self.find(self.numPlays[i]*self.kl(self.payoffSums[c] / self.numPlays[c]) < math.log(t));
                
                #print self.L,self.L1
                if len(self.L)>-1:
                    #print "L: "+str(self.L)
                    action = self.L[0]
                    #lastAction=action
                    self.L1=[]
                    for i in range(1,len(self.L)):
                        self.L1.append(self.L[i])
                    self.L=[]
                    
                    for i in range(0,len(self.L1)):
                        self.L.append(self.L1[i])
                    #print "L: "+str(self.L)    
            #action = lastAction;
            
            #ucbs = [(self.payoffSums[i] / self.numPlays[i]) + self.upperBound(t, self.numPlays[i]) for i in range(self.numActions)]
            #upbs = [self.upperBound(t, self.numPlays[i]) for i in range(self.numActions)]
            #print "upbs"
            #print upbs
            #print ucbs
            #getting the maximum of the ucbs
            #action = max(range(self.numActions), key=lambda i: ucbs[i])
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
            
            if t>=self.numRounds:
                break
            
            t = t + 1
            
            #print t

            if t%10000==0:
                print t,regret

            
    
        action=max(range(self.numActions), key=lambda i: self.arm_reward[i])
        #print self.arm_reward
        

        f = open('NewExpt/expt2/testRegretDMED01.txt', 'a')
        for r in range(len(self.actionRegret)):
            f.write(str(self.actionRegret[r])+"\n")
        f.close()

        return cumulativeReward,bestActionCumulativeReward,regret,action,t
        

if __name__ == "__main__":
    
    wrong=0
    i=100
    while i<=100:
        turn=0
        for j in range(0,100):
            
            random.seed(i+j)
            
            obj=DMED()
            cumulativeReward,bestActionCumulativeReward,regret,arm,timestep=obj.DMED(i)
            if arm!=i-2:
            #if arm!=i/2:
                wrong=wrong+1
            print "turn: "+str(turn)+"\twrong"+str(wrong)+"\tarms: "+str(i)+"\tbarm: "+str(arm)+"\tReward: "+str(cumulativeReward)+"\tbestCumReward: "+str(bestActionCumulativeReward)+"\tregret: "+str(regret)
            f = open('NewExpt/expt2/testDMED01.txt', 'a')
            f.writelines("arms: %d\tbArms: %d\ttimestep: %d\tregret: %d\tcumulativeReward: %.2f\tbestCumulativeReward: %.2f\n" % (i, arm, timestep, regret, cumulativeReward, bestActionCumulativeReward))
            f.close()
            
            turn=turn+1
        i=i+1
        