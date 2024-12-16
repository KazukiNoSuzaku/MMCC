#Author: Kaustav Ghosh
#Student ID:720054122
#M/M/C/C Simulation (C=16)

import math
import numpy
import random 
import matplotlib.pyplot as plt
import pandas as pd

class Sim1():
  
  def __init__(self, Customer_total,mean_interarrival_Time,mean_service_Time):
    self.mean_interarrival =mean_interarrival_Time # Mean Interarrival Time (1/λ)
    self.mean_service=mean_service_Time # Mean Service Time (1/µ) (Note : It should be considered that Mean Service Time < Mean Interarrival Time)
    self.sim_time = 0.0 #simulation time
    self.C_servers=16 #total number of cell towers
    self.num_event = self.C_servers+1
    self.num_customers = 0
    self.num_customers_required = Customer_total #initialising the number of customers
    self.next_event_type=0
    self.server_status=numpy.zeros(self.C_servers+1)
    self.area_server_status=numpy.zeros(self.C_servers)
    self.time_next_event = numpy.zeros(self.C_servers+1)
    self.time_next_event[0]=self.sim_time+self.expon(self.mean_interarrival) #determine next arrival
    for i in range(1,self.C_servers+1):
      self.time_next_event[i]=math.inf
    self.server_idle=0 #determine next departure.
    self.server_utilization=numpy.zeros(self.C_servers)
    self.total_server_utilization=0
    self.Total_Loss=0

  #######################  Define MAIN() function
  def main(self):
    while (self.num_customers < self.num_customers_required):
      self.timing()
      self.update_time_avg_stats()
      if (self.next_event_type == 0):
        self.arrive()  ## next event is arrival
      else:
        self.j=self.next_event_type
        self.depart() ## next event is departure
    self.report()

  ######################### Define validationLoop 
  def validationLoop(self):
    while (self.num_customers < self.num_customers_required):
      self.timing()
      self.update_time_avg_stats()
      if (self.next_event_type == 0):
        self.arrive()  ## next event is arrival
      else:
        self.j=self.next_event_type
        self.depart() ## next event is departure
    self.validation()

  ########################  Define TIMING() function
  def timing(self):
    self.min_time_next_event = math.inf
      ##Determine the event type of the next event to occur
    for i in range(0,self.num_event):
      if (self.time_next_event[i] <= self.min_time_next_event):
          self.min_time_next_event=self.time_next_event[i]
          self.next_event_type=i

    self.time_last_event=self.sim_time
     ##advance the simulation clock
    self.sim_time=self.time_next_event[self.next_event_type]

  ########################  Define UPDATE_TIME_AVG_STATS() function
  def update_time_avg_stats(self):
    self.time_past=self.sim_time-self.time_last_event
    for i in range(1,self.C_servers+1):
      self.area_server_status[i-1]+=self.time_past*self.server_status[i]

 #########################   Define ARRIVAL() function
  def arrive(self):
    ix=0
    self.server_idle = 0

  ##Schedule next arrival
    self.time_next_event[0]=self.sim_time+self.expon(self.mean_interarrival)

    while (self.server_idle == 0 and ix<=self.C_servers):
      if (self.server_status[ix] == 0):
        self.server_idle = ix
      ix+=1

    if (self.server_idle != 0):  ## Someone is IDLE
      self.server_status [self.server_idle] = 1
      self.time_next_event[self.server_idle] =self.sim_time+ self.expon(self.mean_service)

    else:  ## server is BUSY
      self.Total_Loss +=1
    self.num_customers+=1

    ###########################   Define DEPARTURE() function
  def depart(self):
    # if (self.num_in_q == 0): ## queue empty
      self.server_status [self.j] = 0
      self.time_next_event [self.j] = math.inf

  def expon(self,mean):
    return (-1*mean*math.log(random.random()))
    #############################################################   Define REPORT() function
  def report(self):
    for i in range(0,self.C_servers):
      self.server_utilization[i]=self.area_server_status[i]/self.sim_time
      self.total_server_utilization+=self.area_server_status[i]
    self.total_server_utilization = self.total_server_utilization/(self.sim_time*self.C_servers)
    print ('----------------------------------Simulation Report from this Simulation----------------------------------')
    print('')
    meu=1/self.mean_service
    lambda1=1/self.mean_interarrival
    print('λ = ',lambda1)
    print('µ = ',meu)
    print ('Total Server Utilization =',self.total_server_utilization)#actual ultilization
    print ('Block Probability =',self.Total_Loss/self.num_customers_required)
    print('')
    print('')
    print ('----------------------------------Sumulation Report from Validation Formula----------------------------------')
    Temp1=0
    Temp2=0
    # Block Probability Calculation:
    for k in range (0,self.C_servers+1):
      Temp1+=((lambda1/meu)**k)/(math.factorial(k))
    self.Pc=(((lambda1/meu)**self.C_servers)/(math.factorial(self.C_servers)))/Temp1
    self.SU=lambda1/(self.C_servers*meu)
    print ()
    print ('Expected Total Server Utilization =',self.SU*(1-self.Pc))#expected utilization
    print ('Expected Block Probability =',self.Pc)

    ################################################################## Define Validation
  def validation(self):
    for i in range(0,self.C_servers):
      self.server_utilization[i]=self.area_server_status[i]/self.sim_time
      self.total_server_utilization+=self.area_server_status[i]
    self.total_server_utilization = self.total_server_utilization/(self.sim_time*self.C_servers)#actual utilization
    meu=1/self.mean_service
    lambda1=1/self.mean_interarrival
    self.Bc=self.Total_Loss/self.num_customers_required#actual bloacking probability
    Temp1=0

    #Validation
    for k in range (0,self.C_servers+1):
      Temp1+=((lambda1/meu)**k)/(math.factorial(k))
    self.Pc=(((lambda1/meu)**self.C_servers)/(math.factorial(self.C_servers)))/Temp1 #expected block probability
    self.SU=lambda1/(self.C_servers*meu) 
    self.eTSU= self.SU*(1-self.Pc) #expected utilization


obj = Sim1(Customer_total=100000,mean_interarrival_Time=5,mean_service_Time=100)
obj.main()

#Validation Though graphs and data
l1=[]#store utilization
l2=[]#store expected Utilization
l3=[]#Block probability
l4=[]#expected brock probability
l5=[]#arrival rate (λ)

#arrival rate .01 = 100 sec mean interarrival time and arrivale rate .1 = 10 sec
print('')
print ('----------------------------------Validating our Model----------------------------------')
print('')
for i in range(10,101):
  obj = Sim1(Customer_total=100000,mean_interarrival_Time=i,mean_service_Time=100)
  obj.validationLoop()
  x=obj.total_server_utilization
  y=obj.eTSU
  z=obj.Bc
  w=obj.Pc
  l1.append(x)
  l2.append(y)
  l3.append(z)
  l4.append(w)
  l5.append(1/i)
  print(x,y)
  


plt.plot(l1,l2)
plt.xlabel("Total Server Utilization")
plt.ylabel("Expected Utilization")
plt.show()

###################### Storing data in CSV
df= pd.DataFrame()
df['Utilization']=l1
df['Expected Utilization']=l2
df['Block Probability']=l3
df['Expected Block Probability']=l4
df['Arrival Rate']= l5
df.to_csv('Report_1.csv', index=False)

