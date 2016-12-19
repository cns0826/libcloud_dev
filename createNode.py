#!/usr/bin/python

"from XML : cidr_block, vpc_name, subnet_name"

class createNode :
	def get_Index_image(self, driver, image_id):
		return driver.get_image(image_id)

	def find_Index_images(self, driver, image_id):
		images = driver.list_images()
		for index, image in enumerate(images):
			if image.id == image_id :
				print index, image.id
				return images[index];

	def find_Index_sizes(self, driver, size_id):
		sizes = driver.list_sizes()
		for index, size in enumerate(sizes):
			if size.id == size_id :
				print index, size
				return sizes[index];
		
	def import_SSH_key(self, driver, key_name, private_key):
		driver.import_key_pair_from_string(key_name, private_key)


	def create_Node(self, driver, 
			node_name,
			ssh_key_name,
			public_key,
			new_security_group_id,
			image,
			size,
			terminate_on_shutdown,
			new_subnet
			):
			return	driver.create_node(
				name = node_name,
				ex_keyname = ssh_key_name,
				ssh_key = public_key,
				ex_security_group_ids=new_security_group_id,
				image = image,
				size = size,
				ex_terminate_on_shutdown = terminate_on_shutdown,
				ex_subnet = new_subnet
				)


	def create_EIP(self, driver):
		return driver.ex_allocate_address()

	
	def allocate_EIP_NODE(self, driver, new_node, new_eip):
		return driver.ex_associate_address_with_node(
			new_node,
			new_eip
			)

