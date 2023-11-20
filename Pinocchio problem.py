#Pinocchio problem: it's the search problem where there are only a limited number of questions you can ask (question threshold, pinocchio nose length)



import math 
import numpy as np
import random




N = 10
array = []
for j in range(N):
    r = int(random.uniform(1,N))
    array.append(r)
    
    
#Steps: Extremes or Regular 

##Regular: Linear Search or Divide-and-Conquer (Binary Search, Ternary Search, k-ary Search, Exponential Seach, Jump Search...etc): We chose Binary Search
def Binary_Search(arr,val,AccPino, PinoLimit):
    result = None
    Pinocchio_Counter = AccPino
    sorted_arr = np.sort(arr)
    mid = (len(arr))//2
    if Pinocchio_Counter < PinoLimit:
        if sorted_arr[mid] == val:
            result = mid
            return result
        elif val > sorted_arr[mid]:
            Pinocchio_Counter += 1
            return Binary_Search(arr[mid+1:],val)
        else:
            Pinocchio_Counter += 1
            return Binary_Search(arr[:mid],val)
    else:
        result = "Pinocchio limit is exceeded!"
        return result
    
    
##Extreme: Steps that are not regular, but they tend to be more effective on the off-chance best case scenario (luck is needed therefore) in eliminating diffusive cost (principle of indifference/insuffient reason) = Non-Egalitarian

###Types of extremes: Extremely small or Extremely large

#Implementation: Implementation is about going back-and-forth between extreme mode and regular mode.
## Types: Systematic (Constant, Bayesian (accumulative performance), Markovian (last performance), Alternative, Annealing) or Stochastic
  
#Value: Constant or Dynamic

#Compensation: Correlated Steps method (it works for memory-based implementations (not necessairly though) such as Bayesian or Markovian, similar to aspiration criteria. The memory stores the reward/punishment values of performance of each mode)
## => Compensation is in terms of mode alteration and step size




## Implementation = Systematic , Value = Constant

# Annealing (Extreme -> Regular)
def Annealing(arr,val,PinoLimit):
    result = None
    Pinocchio_Counter = 0
    Ex_Iter = len(arr)//4
    new_arr = np.sort(arr)
    l = 0
    r = len(arr) - 1
    t = 0
    i = int(random.uniform(0,len(new_arr)))
    while t < Ex_Iter:
        if new_arr[i] == val:
            result = i
            break
        if new_arr[i] < val:
            Pinocchio_Counter += 1
            l = i + 1
            R = int(random.uniform(0,2))
            if R == 1:
                i = i + 1
            else:
                s = len(new_arr) - 2 - i
                i = i + s
        
        if new_arr[i] > val:
            Pinocchio_Counter += 1
            r = i
            L = int(random.uniform(0,2))
            if L == 1:
                i = i - 1
            else:
                p = i + 2
                i = p - i
        if Pinocchio_Counter == PinoLimit:
            result = "Pinocchio limit is exceeded!"
            break
            
        new_arr = arr[l:r]
        
        t = t + 1

    if result == None: #Enters this code block only if Ex_Iter < PinoLimit with Pinocchio_Counter = Ex_Iter (for Annealing to work, Ex_Iter should therefore be chosen smaller than PinoLimit)
        result = Binary_Search(new_arr,val,Pinocchio_Counter, PinoLimit)
        
    return result


F = Annealing(array,4,10)
print(array)
print(F)


def Alternative(arr,val,Ex,Reg,PinoLimit):
    def Extreme(arr,val):
        result = None
        PC = 0
        Ex_Iter = Ex
        new_arr = np.sort(arr)
        l = 0
        r = len(arr) - 1
        t = 0
        i = int(random.uniform(0,len(new_arr)))
        while t < Ex_Iter:
            if new_arr[i] == val:
                result = i
                break
            if new_arr[i] < val:
                PC += 1
                l = i + 1
                R = int(random.uniform(0,2))
                if R == 1:
                    i = i + 1
                else:
                    s = len(new_arr) - 2 - i
                    i = i + s
        
            if new_arr[i] > val:
                PC += 1
                r = i
                L = int(random.uniform(0,2))
                if L == 1:
                    i = i - 1
                else:
                    p = i + 2
                    i = p - i
            
            new_arr = arr[l:r]
        
            t = t + 1
        return result, new_arr, PC
        
    def Regular(arr,val):
        result = None
        PC = 0
        Reg_Iter = Reg
        sorted_arr = np.sort(arr)
        mid = (len(arr)-1)//2
        init = 0
        final = len(arr)-1
        new_arr = sorted_arr[init:final]
        t = 0
        while t < Reg_Iter:
            if sorted_arr[mid] == val:
                result = mid
                return result
            elif val > sorted_arr[mid]:
                PC += 1
                init = mid + 1
                new_arr = sorted_arr[init:]
            else:
                PC += 1 
                final = mid
                new_arr = sorted_arr[:final]
            t = t + 1
        return result, new_arr, PC
    def Alteration(arr,val,j):
        if j%2 == 0:
            R = Regular(arr,val)[0]
            NEW_ARR = Regular(arr,val)[1]
            PCC = Regular(arr,val)[2]
        else:
            R = Extreme(arr,val)[0]
            NEW_ARR = Extreme(arr,val)[1]
            PCC = Extreme(arr,val)[2]
        return R,NEW_ARR,PCC
        
    
    t = 1
    Pinocchio_Counter = 0
    while Pinocchio_Counter < PinoLimit:
        #Let's start with Extreme            
        result = Alteration(arr,val,t)[0]
        if result == None:
            Pinocchio_Counter += Alteration(arr,val,t)[2]
            NArr = Alteration(arr,val,t)[1]
            result = Alteration(NArr,val,t)[0]
        else:
            break
        
        t = t + 1
    if result == None:
        result = "Pinocchio limit is exceeded!"
    return result

        
    
F = Alternative(array,4,1,1,10)
print(array)
print(F)






def Markovian(arr,val,PinoLimit):
    result = None
    #Performance Memory: Performance is measured as the difference between the actual val and the last expected val predicted by a given mode
    Regular_Memory = [] 
    Extreme_Memory = []
    PT = len(arr)//2 #Performance threshold
    def Regular(arr,val):
        result = None
        PC = 0
        sorted_arr = np.sort(arr)
        mid = (len(arr)-1)//2
        init = 0
        final = len(arr)-1
        new_arr = sorted_arr[init:final]
        t = 0
        while t < 1:
            if new_arr[mid] == val:
                result = mid
                return result
            elif val > new_arr[mid]:
                Regular_Memory.append(val - new_arr[mid])
                PC += 1
                init = mid + 1
                new_arr = new_arr[init:]
            else:
                Regular_Memory.append(new_arr[mid] - val)
                PC += 1 
                final = mid
                new_arr = new_arr[:final]
            t = t + 1
        return result
    
    def Extreme(arr,val):
        result = None
        PC = 0
        new_arr = np.sort(arr)
        l = 0
        r = len(arr) - 1
        t = 0
        i = int(random.uniform(0,len(new_arr)))
        while t < 1:
            if new_arr[i] == val:
                result = i
                break
            if new_arr[i] < val:
                Extreme_Memory.append(val - new_arr[i])
                PC += 1
                l = i + 1
                R = int(random.uniform(0,2))
                if R == 1:
                    i = i + 1
                else:
                    s = len(new_arr) - 2 - i
                    i = i + s
        
            if new_arr[i] > val:
                Extreme_Memory.append(new_arr[i] - val)
                PC += 1
                r = i
                L = int(random.uniform(0,2))
                if L == 1:
                    i = i - 1
                else:
                    p = i + 2
                    i = p - i
            
            new_arr = arr[l:r]
        
            t = t + 1
        return result, new_arr, PC
    def Alteration(arr,val,j):
        if Regular_Memory[j] <= PT and Extreme_Memory[j] > PT:
            R = Regular(arr,val)[0]
            NEW_ARR = Regular(arr,val)[1]
            PCC = Regular(arr,val)[2]
            return R, NEW_ARR, PCC 
        if Regular_Memory[j] > PT  and Extreme_Memory[j] <= PT:
            R = Extreme(arr,val)[0]
            NEW_ARR = Extreme(arr,val)[1]
            PCC = Extreme(arr,val)[2]
            return R, NEW_ARR, PCC 
        if Regular_Memory[j] <= PT and Extreme_Memory[j] <= PT:
            return Alteration(arr,val,j-1)
            
    
    
    t = 0
    Pinocchio_Counter = 0
    while Pinocchio_Counter < PinoLimit:
        #Let's start with Extreme            
        result = Alteration(arr,val,t)[0]
        if result == None:
            Pinocchio_Counter += Alteration(arr,val,t)[2]
            NArr = Alteration(arr,val,t)[1]
            result = Alteration(NArr,val,t)[0]
        else:
            break
        
        t = t + 1
    if result == None:
        result = "Pinocchio limit is exceeded!"
    return result









def Bayesian(arr,val,PinoLimit):
    result = None
    Performance_Memory = [] #Performance is measured as the difference between the actual val and the last expected val predicted by a given mode



def Constant(arr,val,C,PinoLimit): #Extreme Constant is very naive
    def Regular(arr,val):
        result = None
        PC = 0
        sorted_arr = np.sort(arr)
        mid = (len(arr)-1)//2
        init = 0
        final = len(arr)-1
        new_arr = sorted_arr[init:final]
        t = 0
        while t < len(arr):
            if sorted_arr[mid] == val:
                result = mid
                return result
            elif val > sorted_arr[mid]:
                PC += 1
                init = mid + 1
                new_arr = sorted_arr[init:]
            else:
                PC += 1 
                final = mid
                new_arr = sorted_arr[:final]
            t = t + 1
        return result
    
    def Extreme(arr,val):
        result = None
        PC = 0
        new_arr = np.sort(arr)
        l = 0
        r = len(arr) - 1
        t = 0
        i = int(random.uniform(0,len(new_arr)))
        while t < len(arr):
            if new_arr[i] == val:
                result = i
                break
            if new_arr[i] < val:
                PC += 1
                l = i + 1
                R = int(random.uniform(0,2))
                if R == 1:
                    i = i + 1
                else:
                    s = len(new_arr) - 2 - i
                    i = i + s
        
            if new_arr[i] > val:
                PC += 1
                r = i
                L = int(random.uniform(0,2))
                if L == 1:
                    i = i - 1
                else:
                    p = i + 2
                    i = p - i
            
            new_arr = arr[l:r]
        
            t = t + 1
        return result, new_arr, PC
    
    if C == 0:
        PinCounter = 0
        result = None
        while PinCounter < PinoLimit:
            result = Regular(arr,val)[0]
            PinCounter += Regular(arr,val)[2]
        if result == None:
            result = "Pinocchio limit is exceeded!"
        return result
    else:
        PinCounter = 0
        result = None
        while PinCounter < PinoLimit:
            result = Extreme(arr,val)[0]
            PinCounter += Extreme(arr,val)[2]
        if result == None:
            result = "Pinocchio limit is exceeded!"
        return result
    



 ## Implementation = Stochastic , Value = Constant


def Stochastic(arr,val,Ex,Reg,PinoLimit):
    def Extreme(arr,val):
        result = None
        PC = 0
        Ex_Iter = Ex
        new_arr = np.sort(arr)
        l = 0
        r = len(arr) - 1
        t = 0
        i = int(random.uniform(0,len(new_arr)))
        while t < Ex_Iter:
            if new_arr[i] == val:
                result = i
                break
            if new_arr[i] < val:
                PC += 1
                l = i + 1
                R = int(random.uniform(0,2))
                if R == 1:
                    i = i + 1
                else:
                    s = len(new_arr) - 2 - i
                    i = i + s
        
            if new_arr[i] > val:
                PC += 1
                r = i
                L = int(random.uniform(0,2))
                if L == 1:
                    i = i - 1
                else:
                    p = i + 2
                    i = p - i
            
            new_arr = arr[l:r]
        
            t = t + 1
        return result, new_arr, PC
        
    def Regular(arr,val):
        result = None
        PC = 0
        Reg_Iter = Reg
        sorted_arr = np.sort(arr)
        mid = (len(arr)-1)//2
        init = 0
        final = len(arr)-1
        new_arr = sorted_arr[init:final]
        t = 0
        while t < Reg_Iter:
            if sorted_arr[mid] == val:
                result = mid
                return result
            elif val > sorted_arr[mid]:
                PC += 1
                init = mid + 1
                new_arr = sorted_arr[init:]
            else:
                PC += 1 
                final = mid
                new_arr = sorted_arr[:final]
            t = t + 1
        return result, new_arr, PC
    def Alteration(arr,val,j):
        if j%2 == 0:
            R = Regular(arr,val)[0]
            NEW_ARR = Regular(arr,val)[1]
            PCC = Regular(arr,val)[2]
        else:
            R = Extreme(arr,val)[0]
            NEW_ARR = Extreme(arr,val)[1]
            PCC = Extreme(arr,val)[2]
        return R,NEW_ARR,PCC
        
    
    t = 1
    Pinocchio_Counter = 0
    while Pinocchio_Counter < PinoLimit:
        #Let's start with Extreme            
        result = Alteration(arr,val,t)[0]
        if result == None:
            Pinocchio_Counter += Alteration(arr,val,t)[2]
            NArr = Alteration(arr,val,t)[1]
            result = Alteration(NArr,val,t)[0]
        else:
            break
        
        t = int(np.random(1,3))
    if result == None:
        result = "Pinocchio limit is exceeded!"
    return result



# k-ary search algorithms spanning-atomistic property: Let k > 3
## If k is even then all k-ary search algorithms reduce back to binary search where the initial step of the k-ary search is mth step of the binary search where k = m*2
## If k is odd and divisible by 3 then all k-ary search algorithms reduces back to ternary search where the initial step of the k-ary search is mth step of the ternary search where k = m*3
## If k is a prime number, then this property doesn't hold in that k-ary search is needed
## If k is non-prime odd number nor divisible by 3, then it should factorized into primes pm => Perform pm-ary search where pm is the minimum prime number where the inital step of k-ary search is mth step of the pm-ary search where k = m*pm


