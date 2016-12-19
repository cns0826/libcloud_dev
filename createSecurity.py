#!/usr/bin/python
"from XML : security_group_name, description"
class createSecurity :
	
	def createSecurityGroup(self, driver, security_group_name, security_description,
				 new_vpc_id):
		return driver.ex_create_security_group(security_group_name,
				security_description, new_vpc_id);

	def authorize_security_group_ingress(self, driver, new_security_group_id, from_port, to_port, cidr_ip, group_pairs, protocol):

		return driver.ex_authorize_security_group_ingress(
			new_security_group_id,
			from_port,
			to_port,
			cidr_ip,
			group_pairs,	
			protocol);



