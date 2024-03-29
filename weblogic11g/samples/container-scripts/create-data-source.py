#!/usr/bin/python
# Author : Tim Hall

import time
import getopt
import sys
import re

# Throw exception if already exists
from weblogic.descriptor import BeanAlreadyExistsException

# Get location of the properties file.
properties = ''
try:
   opts, args = getopt.getopt(sys.argv[1:],"p:h::",["properies="])
except getopt.GetoptError:
   print 'set_datasource.py -p <path-to-properties-file>'
   sys.exit(2)
for opt, arg in opts:
   if opt == '-h':
      print 'set_datasource.py -p <path-to-properties-file>'
      sys.exit()
   elif opt in ("-p", "--properties"):
      properties = arg
print 'properties=', properties

# Load the properties from the properties file.
from java.io import FileInputStream
 
propInputStream = FileInputStream(properties)
configProps = Properties()
configProps.load(propInputStream)

# Set all variables from values in properties file.
dsName=configProps.get("ds.name")
dsJNDIName=configProps.get("ds.jndi.name")
dsURL=configProps.get("ds.url")
dsDriver=configProps.get("ds.driver")
dsUsername=configProps.get("ds.username")
dsPassword=configProps.get("ds.password")
dsIsCluster=os.environ.get('ADD_TO_CLSTR', 'false')

# Change target name and type if clustered
if dsIsCluster == 'true':
  print ("\n")
  print ("Setting datasource target type as cluster...")
  dsTargetName=os.environ.get("CLUSTER_NAME", "DockerCluster")
  dsTargetType=str('Cluster')
else:
  print ("\n")
  print ("Setting datasource target type as server...")
  dsTargetName = os.environ.get('MS_NAME')
  dsTargetType=str('Server')

#dsTargetType=configProps.get("ds.target.type")
#dsTargetName=configProps.get("ds.target.name")
dsTransactionType=configProps.get("ds.transaction.type")

# Display the variable values.
print 'dsName=', dsName
print 'dsJNDIName=', dsJNDIName
print 'dsURL=', dsURL
print 'dsDriver=', dsDriver
print 'dsUsername=', dsUsername
print 'dsPassword=', dsPassword
print 'dsTargetType=', dsTargetType
print 'dsTargetName=', dsTargetName
print 'dsTransactionType=', dsTransactionType

execfile('/oracle/commonfuncs.py')

# Connect to the AdminServer.
connectToAdmin()

edit()
startEdit(waitTimeInMillis=180000)

try:

  # Create data source.
  cd('/')
  cmo.createJDBCSystemResource(dsName)

  cd('/JDBCSystemResources/' + dsName + '/JDBCResource/' + dsName)
  cmo.setName(dsName)

  cd('/JDBCSystemResources/' + dsName + '/JDBCResource/' + dsName + '/JDBCDataSourceParams/' + dsName)
  set('JNDINames',jarray.array([String(dsJNDIName)], String))

  cd('/JDBCSystemResources/' + dsName + '/JDBCResource/' + dsName + '/JDBCDriverParams/' + dsName)
  cmo.setUrl(dsURL)
  cmo.setDriverName(dsDriver)
  set('Password', dsPassword)

  cd('/JDBCSystemResources/' + dsName + '/JDBCResource/' + dsName + '/JDBCConnectionPoolParams/' + dsName)
  cmo.setTestTableName('SQL SELECT 1 FROM DUAL\r\n\r\n')

  cd('/JDBCSystemResources/' + dsName + '/JDBCResource/' + dsName + '/JDBCDriverParams/' + dsName + '/Properties/' + dsName)
  cmo.createProperty('user')

  cd('/JDBCSystemResources/' + dsName + '/JDBCResource/' + dsName + '/JDBCDriverParams/' + dsName + '/Properties/' + dsName + '/Properties/user')
  cmo.setValue(dsUsername)

  cd('/JDBCSystemResources/' + dsName + '/JDBCResource/' + dsName + '/JDBCDataSourceParams/' + dsName)
  cmo.setGlobalTransactionsProtocol(dsTransactionType)

#  cd('/SystemResources/' + dsName)
#  set('Targets',jarray.array([ObjectName('com.bea:Name=' + dsTargetName + ',Type=' + dsTargetType)], ObjectName))

except BeanAlreadyExistsException:
	print '*** Error: ' + dsName + ' datasource already exists... Exiting.'
	cancelEdit('y')
	exit()

save()
activate()

disconnect()
exit()
