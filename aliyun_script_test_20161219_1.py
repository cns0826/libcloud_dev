#!/usr/bin/python
#-*-coding:utf8;-*-


print "0. Initial Variables Setting From input.xml "

from xml.etree.ElementTree import parse
from libcloud.utils.xml import findall, findattr, findtext

import sys
try :
	xmlfile = sys.argv[1]
except :
	print "Usage python aliyun_script_test_20161218_1.py <FILE NAME> ...."
	quit()	



root = parse(xmlfile).getroot()

system_name = root.find('system/name').text
node_password = root.find('instance/node_password').text
vpc_cidr_block = root.find('vpc/cidr').text
vpc_name = root.find('vpc/name').text
ZoneId = root.find('system/zoneid').text
ssh_key_name = root.find('system/ssh_key_name').text


vswitch_name = []
vswitch_cidr = []
vswitch_id = []


for i in root.findall('vswitch'):
        vswitch_name.append(i.find('name').text)
        vswitch_cidr.append(i.find('cidr').text)
        vswitch_id.append(i.find('cidr').text)



IpProtocol = []
PortRange = []
SourceCidrIp = []


for i in root.findall('security_group/rule'):
        IpProtocol.append(i.find('IpProtocol').text)
        PortRange.append(i.find('PortRange').text)
        SourceCidrIp.append(i.find('SourceCidrIp').text)

SecurityGroupName = root.find('security_group/name').text
Description = root.find('security_group/description').text


instance_Image = []
instance_Size = []
instance_node_name = []
instance_Description = []
instance_Hostname = []
InternetChargeType =[]
Max_Bandwidth_out = []
Max_Bandwidth_in = []
instance_vswitch_name = []


for i in root.findall('instance'):
        instance_Image.append(i.find('instance_Image').text)
        instance_Size.append(i.find('instance_Size').text)
        instance_node_name.append(i.find('instance_node_name').text)
        instance_Description.append(i.find('instance_Description').text)
        instance_Hostname.append(i.find('HostName').text)
        InternetChargeType.append(i.find('InternetChargeType').text)
        Max_Bandwidth_out.append(i.find('Max_Bandwidth_out').text)
        Max_Bandwidth_in.append(i.find('Max_Bandwidth_in').text)
        instance_vswitch_name.append(i.find('instance_vswitch_name').text)




salt_master_ip = root.find('saltstack/master_ip').text


Instance_array = []
Vswitch_array = []



ecs_name_list = []
ecs_node_list = []
ecs_node_id_list = []
Eip_ip_list = []
Eip_AllocationId_list = []




from libcloud.utils.xml import findall, findattr, findtext
from libcloud.compute.base import NodeAuthSSHKey, NodeAuthPassword
from libcloud.compute.base import NodeAuthPassword

import os,sys 
import time

instance_count = len(instance_Image)
print instance_count , "ECS will be created..."
print ""
print ""
print ""
print ""
now  = time.localtime()
filename = "%04d-%02d-%02d_%02d:%02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)

print "0.CREATED FILE NAME : ", filename+".txt"

f=open(filename+".txt",'w')




print "1.DRIVER CREATE"

import createDriver
a = createDriver.createDriver()
driver = a.getDriver()

print "========= Input Param ============"
print " ACCESS_ID :", a.getACCESS_ID()
print " SECRET_KEY :", a.getSECRET_KEY()
print ""

print "============ Output =============="
print driver
print ""
print ""
print ""


print "2. REGION ID CHECK"
import createNetwork
RegionId = driver.__dict__['region']

print "RegionId : " , RegionId

print ""
print ""
print ""




print "3. NEW VPC instance CREATE"
print "========= Input Param ============"
print "RegionId : " , RegionId 
print "VPC_CIDR_BLOCK : " ,vpc_cidr_block 
print "VPC NAME : " , vpc_name
print ""

net = createNetwork.createNetwork()
new_vpc = net.createVPC(driver, RegionId, vpc_cidr_block, vpc_name)
result = findall(new_vpc, 'VpcId')
new_vpc_id = findall(new_vpc, 'VpcId')[0].__dict__['text']

print ""
print ""
print ""

"print VPC DELETE : driver.ex_delete_networks(new_vpc_id)"




while True:
	vpclist = net.listVPC(driver, RegionId)
	VpcsList = findall(vpclist,'Vpcs/Vpc')

	for i,v in enumerate(VpcsList) :
		for vpc_id in findall(v,'VpcId') :
			if vpc_id.__dict__['text'] == new_vpc_id :
				index = i
				print "index : " , index

		for status in findall(v,'Status') :
			if index == i :
				vpc_status = status.__dict__['text']
				print " vpc_status : " ,vpc_status

	if vpc_status != 'Available' :
                print "VPC is not ready.. wait 5 seconds... Status : ", vpc_status
                time.sleep(5)
        else :
                print "VPC is Ready.."
                break




print "============ Output =============="
print " new_vpc_id : " , new_vpc_id
print ""
print ""
print ""





for i in range(0,len(vswitch_cidr)) :

	print "4. PUBLIC  VSwitch CREATE (Subnet)"

	print "========= Input Param ============"
	print "ZONEID : " , ZoneId
	print "NEW_VPC_ID : " , new_vpc_id
	print "VSWITCH CIDR BLOCK : " , vswitch_cidr[i]
	print "" 
	print "" 
	print "" 

	vswitch = driver.ex_create_subnet(ZoneId, new_vpc_id, vswitch_cidr[i], vswitch_name[i])
	print vswitch
	print ZoneId , new_vpc_id, vswitch_cidr[i], vswitch_name[i]
	vswitch_id[i] = findall(vswitch, 'VSwitchId')[0].__dict__['text']

	PUBLIC_VSwitchId = vswitch_id[i]

	print "============ Output =============="
	print " VSwitchId : " , vswitch_id[i] 
	print ""
	Vswitch_array.append(vswitch_id[i])






	print "5. PUBLIC VSwitch Status CHECK"

	while True:

		VSwitchesResponse=driver.ex_list_VSwitches(new_vpc_id)

		VSwitchesList = findall(VSwitchesResponse,'VSwitches/VSwitch')
		print  VSwitchesList

		for i,v in enumerate(VSwitchesList) :
			for j,k in enumerate(findall(v,'VSwitchId')):
				if vswitch_id[i] == k.__dict__['text'] :
					index = i
			for a,b in enumerate(findall(v,'Status')):
				if index==i :
					vswitch_status =  b.__dict__['text']
					print vswitch_status, b.__dict__['text']

		if vswitch_status != 'Available' :
			print "VSwitche is not ready.. wait 5 seconds..."
			time.sleep(5)
		else :
			print "VSwitch is Ready.."
			break












"print List Subnet : driver.ex_list_subnets(new_vpc_id)"
"print Delete Subnet : driver.ex_delete_subnet(vswitch_id)"

" vswitch_list = findall(vwitch_list,'VSwitches/VSwitch')"
" vswitch_id_list = findall(vwitch_list,'VSwitches/VSwitch/VSwitchId')"


print "6. Security Group Create"
print "========= Input Param ============"
print "REGION ID : " , RegionId
print "SecurityGroupName : " , SecurityGroupName
print "NEW_VPC_ID : " , new_vpc_id
print ""

SecurityGroupId = driver.ex_create_security_group_kkh(RegionId, SecurityGroupName, Description, new_vpc_id )


"print Delete Security Group : driver.ex_delete_security_group_by_id(SecurityGroupId)"

print "============ Output =============="
print " SecurityGroupId : " , SecurityGroupId
print ""
print ""



print "7. Authorizing Security Group (Rule ADD)"

print ""

for i in range(0,len(IpProtocol)): 
	print "========= Input Param ============"
	print "SecurityGroupId : " , SecurityGroupId
	print "RegionId : " , RegionId 
	print "IpProtocol : " , IpProtocol[i]
	print "PortRange : " , PortRange[i]
	print "SourceCidrIp : " , SourceCidrIp [i]

	result = driver.ex_authorize_security_group(SecurityGroupId, RegionId, IpProtocol[i], PortRange[i], SourceCidrIp[i])

	print "============ Output =============="
	print "Authorizing Security Group RESULT : " , result




print "8. vRouter Check "
print "========= Input Param ============"
print " RegionId : " , RegionId 

vrouterlistRes = driver.ex_list_router(RegionId)
vRouterList = findall(vrouterlistRes,'VRouters/VRouter')


for i,v in enumerate(vRouterList):
	if(findall(v,'VpcId')[0].__dict__['text']==new_vpc_id) :
		VRouterId = findall(v,'VRouterId')[0].__dict__['text']


print "============ Output =============="
print " VRouterId : " , VRouterId
print ""
print ""
print ""
print ""






for i in range(0,instance_count):


	print "9. NODE SIZE CHECK"

	for j, v in enumerate(driver.list_sizes()) :
       		if(v.__dict__['id'] == instance_Size[i]) :
               		size = v


	image = driver.get_image(instance_Image[i])
	print "========= Input Param ============"
	print " size : " , size
	print " image : " , image
	print ""
	print ""
	print ""


	auth = NodeAuthPassword(node_password)



	print "10. FIRST INSTANCE CREATE"
	print i 
	print "Before  ECS Createing INSTANCE, we have to wait for 15 seconds.."

	time.sleep(15)

	for j in range(0, len(vswitch_name)):
		print "j : " , j
		print vswitch_name[j]
		print instance_vswitch_name[i]
		print vswitch_id[j]
		if vswitch_name[j] == instance_vswitch_name[i]:
			PUBLIC_VSwitchId = vswitch_id[j]

	print "========= Input Param ============"
	print "RegionId : " , RegionId
	print "Image : " , image
	print "Size : " , size
	print "Name : " , instance_node_name[i]
	print "ZoneId : " , ZoneId
	print "VSwitchId : " , PUBLIC_VSwitchId
	print "SecurityGroupId : " , SecurityGroupId
	print ""




	ecs_node = driver.create_node4(RegionId=RegionId,
       		         Image=image,
       		         Size=size,
       		         Name=instance_node_name[i],
               		 ZoneId=ZoneId,
	                 VSwitchId=PUBLIC_VSwitchId,
        	         SecurityGroupId=SecurityGroupId,
                	 ex_security_group_id=SecurityGroupId,
	                 ex_description=instance_Description[i],
        	         ex_hostname=instance_Hostname[i],
                	 auth=auth,
	                 ex_internet_charge_type=InternetChargeType[i],
	                 ex_internet_max_bandwidth_in=Max_Bandwidth_in[i],
	                 ex_internet_max_bandwidth_out=Max_Bandwidth_out[i],
        	         ex_vswitch_id=PUBLIC_VSwitchId
                	 )



	ecs_node_list.append(ecs_node)
	ecs_node_id = ecs_node.__dict__['id']
	ecs_node_id_list.append(ecs_node_id)
	print "============ Output =============="
	print " ecs_node_id : ", ecs_node.__dict__['id']
	print ""
	print ""
	print ""


print "11. EIP ALLOCATION"


print "========= Input Param ============"
print "RegionId : " , RegionId 

for i in range(0,instance_count):
	result = driver.ex_createEipAddress(RegionId)
	Eip_ip = findall(result,'EipAddress')[0].__dict__['text']
	Eip_AllocationId = findall(result,'AllocationId')[0].__dict__['text']

	Eip_ip_list.append(Eip_ip)
	Eip_AllocationId_list.append(Eip_AllocationId)

	print "============ Output =============="
	print "Eip_AllocationId : " , Eip_AllocationId
	print "Eip ip : ", Eip_ip
	print ""
	print ""




	print "12. EIP & ECS Bind..."
	print "========= Input Param ============"
	print "Eip_AllocationId : " , Eip_AllocationId[i]
	print "ecs_node_id : " , ecs_node_id[i]

	result = driver.ex_BingEipAddress(Eip_AllocationId_list[i], ecs_node_id_list[i])

	print "============ Output =============="
	print "12. EIP & ECS Bind result : " , result
	print ""
	print ""
	print ""
	print ""
	print ""
	print "ecs_node_ip : " , Eip_ip 


for i,k in enumerate(ecs_node_id_list) :
	f.write("INSTANCE_ID : " + k + "\n")

for i,k in enumerate(Eip_ip_list) :
	f.write("EIP : " + k + "\n")

for i,k in enumerate(Eip_AllocationId_list) :
	f.write("EIP_ALLOCATION_ID : " + k + "\n")

for i,k in enumerate(Vswitch_array) :
	f.write("VSWITCH_ID : "  + k + "\n")

for i,k in enumerate(instance_Size) :
	f.write("Instance Size: "  + k + "\n")

for i,k in enumerate(instance_Image) :
	f.write("Instance Image: "  + k + "\n")

f.write("SecurityGroupId : "+ SecurityGroupId + "\n")
f.write("NEW_VPC_ID : "+ new_vpc_id  + "\n")
f.write("ZONE_ID : "+ ZoneId  + "\n")
f.write("PASSWORD : "+ node_password + "\n")


f.close()


print "----------------------- SALT STACK INITIATION -------------------\n"




f=open("saltstack_install.sh",'w')
f.write("sudo yum update -y \n")
f.write("curl -L https://bootstrap.saltstack.com -o install_salt.sh \n")
f.write("sudo sh install_salt.sh -P \n")
f.close()


f=open("update_hosts.sh",'w')
f.write("echo "+salt_master_ip+ " salt >> /etc/hosts" + " \n")
f.close()

f=open("authorized_keys_update.sh",'w')

import commands
public_key_tuple = commands.getstatusoutput('cat ' + ssh_key_name+'.pub')
public_key = public_key_tuple[1]

f.write("mkdir .ssh" + " \n")
f.write("chmod 700 .ssh" + " \n")
f.write("touch .ssh/authorized_keys" + " \n")
f.write("echo "+ public_key + " >> .ssh/authorized_keys" + " \n")
f.close()



import os

for i in range(0,instance_count):
	
	print "SSH public Key Regist.. & /root/.ssh/authoirized_keys UPDATE "
	print "START"

	os.system('ssh-keygen -f /home/ubuntu/.ssh/known_hosts -R ' + Eip_ip_list[i])

	print " put "+ ssh_key_name + ".pub's Contents into .ssh/authorized_keys "

	print " scp authorized_keys_update.sh ...."
	os.system('scp authorized_keys_update.sh root@'+ Eip_ip_list[i] +':/root/')

	print " ssh & sh authorized_keys_update.sh ...."
	os.system('ssh  -t root@'+Eip_ip_list[i]+' sh /root/authorized_keys_update.sh ')

	print "END"



for i in range(0,instance_count):



	print Eip_ip_list[i] + " : saltstack_install start"

	os.system('ssh -i ' + ssh_key_name + ' -t root@'+Eip_ip_list[i]+' sudo yum update -y ')

	print ""
	print ""
	print ""
	print ""
	print Eip_ip_list[i] + " : scp saltstack_install.sh "
	print ""
	print ""
	print ""
	print ""
	os.system('scp -i ' + ssh_key_name + ' saltstack_install.sh root@'+ Eip_ip_list[i] +':/root')

	print ""
	print Eip_ip_list[i] + " : sh /saltstack_install.sh "
	os.system('ssh -i ' + ssh_key_name + ' -t root@'+ Eip_ip_list[i] +' sh saltstack_install.sh')
	print ""
	os.system('scp -i ' + ssh_key_name + ' update_hosts.sh root@'+Eip_ip_list[i]+':/root')
	print ""
	print Eip_ip_list[i]  + " : sh update_hosts.sh "
	print ""
	os.system('ssh -i ' + ssh_key_name + ' -t root@'+ Eip_ip_list[i] +' sh update_hosts.sh')


