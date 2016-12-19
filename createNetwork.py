#!/usr/bin/python

"from XML : cidr_block, vpc_name, subnet_name"
from libcloud.utils.xml import findall, findattr, findtext


class createNetwork :

	def listVPC(self, driver, RegionId):
		return driver.ex_list_networks(RegionId)

	def createVPC(self, driver, RegionId, cidr_block, vpc_name):
		new_vpc = driver.ex_create_network(RegionId, cidr_block, vpc_name);
		print "New Create vpc : " , new_vpc
		return new_vpc

	def createSubnet(self, driver, vpc_id, cidr_block, availibilty_zone, subnet_name):
		subnet = driver.ex_create_subnet(vpc_id, cidr_block, availibilty_zone, subnet_name);
		print subnet
		return subnet

	def createIGW(self,driver):
		new_igw = driver.ex_create_internet_gateway();
		return new_igw

	def attachIGW(self, driver, new_igw, new_vpc) :
		return driver.ex_attach_internet_gateway(new_igw, new_vpc);	


	def findRouteTableIndex(self, driver, new_vpc_id) :
		for i,v in enumerate(driver.ex_list_route_tables()) :
			if v.__dict__['extra']['vpc_id'] == new_vpc_id :
				return driver.ex_list_route_tables()[i];

	def associate_RouteTable(self, driver, new_route_table, new_subnet) :
		new_route_table = driver.ex_associate_route_table(new_route_table, new_subnet);
		return new_route_table;
		
		
	def create_Route(self, driver, new_route_table, cidr, new_igw) :
		return driver.ex_create_route(new_route_table, cidr, new_igw );
		
		 
	def create_Route_Table(self, driver, new_vpc, custom_route_table_name) :
		return driver.ex_create_route_table(new_vpc, custom_route_table_name);


	def findDefaultRouteTableIndex(self, driver, new_vpc_id) :
		for i,v in enumerate(driver.ex_list_route_tables()) :
			if v.__dict__['extra']['vpc_id'] == new_vpc_id and len(v.__dict__['routes']) == 1:
				return driver.ex_list_route_tables()[i];
