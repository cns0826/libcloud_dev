#!/usr/bin/python

from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver


class createDriver:

        def getDriver(self):
                cls = get_driver(Provider.ALIYUN_ECS)
                "driver = cls(ACCESS_ID, SECRET_KEY, region=""cn-shenzhen"")"
                "driver = cls(ACCESS_ID, SECRET_KEY, region=""eu-west-1"")"
                driver = cls(ACCESS_ID, SECRET_KEY, region="cn-hongkong")
                "driver = cls(ACCESS_ID, SECRET_KEY, region=""ap-southeast-1"")"
                return driver

	def getACCESS_ID(self):
		return ACCESS_ID


	def getSECRET_KEY(self):
		return SECRET_KEY

