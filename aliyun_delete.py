#!/usr/bin/python
import sys
import createDriver
import time
print "0. DRIVER CREATE " 
a = createDriver.createDriver()
driver = a.getDriver()


print "1. Target FILE NAME : " + sys.argv[1] +"\n"
filename = sys.argv[1]
f = open(filename, 'r')

Instance_array = []
Vswitch_array = []



line = f.readline()
while line:
	tokenized_name = line.split(":")[0].strip()
	tokenized_value =  line.split(":")[1].strip()

	if tokenized_name == "INSTANCE_ID" :
		Instance_array.append(tokenized_value)

		if driver.list_nodes(ex_node_ids=[tokenized_value]) != None :
			print "2. Destroy Instance : " + tokenized_value  + " will be destroyed  " 
			print " RESULT : " + str(driver.destroy_node(driver.list_nodes(ex_node_ids=[tokenized_value])[0]))

	if tokenized_name == "EIP_ALLOCATION_ID" :
			time.sleep(10)
			print "Release EIP_ALLOCATION_ID : " + tokenized_value  + " RESULT : " + str(driver.ex_ReleaseEipAddress(tokenized_value))
		 
	if tokenized_name == "VSWITCH_ID" :
		print "Destroy VSWITCH : " + tokenized_value  + " RESULT : " + str(driver.ex_delete_subnet(tokenized_value))

	if tokenized_name== "NEW_VPC_ID" :
		print "Delete VPC_ID : " + tokenized_value + "\n"
		NEW_VPC_ID = tokenized_value 
	
	if tokenized_name == "SecurityGroupId" :
		print  " DELETE SECURITy GROUP : " + str(driver.ex_delete_security_group_by_id(tokenized_value))

	line = f.readline()



	

print "DELETE VPC ... " 
print "DELETE VPC : " + str(driver.ex_delete_networks(NEW_VPC_ID))


f.close()

print "FILE DELETE...."
import os
os.system('rm '+filename)
