import os
import socket

# Variables
# =========
# Environment Vars

java_home      = os.environ.get('JAVA_HOME', '/usr/java/default')
nm_home	       = os.environ.get('MM_HOME', '/oracle/middleware/wlserver_10.3/common/nodemanager')
nm_type	       = os.environ.get('NM_TYPE',"Plain")
nm_address     = os.environ.get('NM_HOST', '')
nm_port        = os.environ.get('NM_PORT', '5556')
domain_name    = os.environ.get('DOMAIN_NAME', 'docker')
domain_home    = os.environ.get('DOMAIN_HOME', '/oracle/middleware/user_projects/domains/docker')

print('java_home     : [%s]' % java_home);
print('nm_home       : [%s]' % nm_home);
print('nm_type       : [%s]' % nm_type);
print('nm_address    : [%s]' % nm_address);
print('nm_port       : [%s]' % nm_port);
print('domain_name   : [%s]' % domain_name);
print('domain_home   : [%s]' % domain_home);

# Create a NodeManager properties file.
def createNodeManagerPropertiesFile(javaHome, nodeMgrHome, nodeMgrType, nodeMgrListenAddress, nodeMgrListenPort):
  print ('Create Nodemanager Properties File for home: '+nodeMgrHome)
  #print (lineSeperator)
  nmProps=nodeMgrHome+'/nodemanager.properties'
  fileNew=open(nmProps, 'w')
  fileNew.write('#Node manager properties\n')
  #fileNew.write('#%s\n' % str(datetime.now()))
  fileNew.write('DomainsFile=%s/%s\n' % (nodeMgrHome,'nodemanager.domains'))
  fileNew.write('LogLimit=0\n')
  fileNew.write('PropertiesVersion=10.3\n')
  fileNew.write('AuthenticationEnabled=false\n')
  fileNew.write('NodeManagerHome=%s\n' % nodeMgrHome)
  fileNew.write('JavaHome=%s\n' % javaHome)
  fileNew.write('LogLevel=INFO\n')
  fileNew.write('DomainsFileEnabled=true\n')
  fileNew.write('ListenAddress=%s\n' % nodeMgrListenAddress)
  fileNew.write('NativeVersionEnabled=true\n')
  fileNew.write('ListenPort=%s\n' % nodeMgrListenPort)
  fileNew.write('LogToStderr=true\n')
  fileNew.write('weblogic.StartScriptName=startWebLogic.sh\n')
  if nodeMgrType == 'ssl':
    fileNew.write('SecureListener=true\n')
  else:
    fileNew.write('SecureListener=false\n')
  fileNew.write('LogCount=1\n')
  fileNew.write('QuitEnabled=true\n')
  fileNew.write('LogAppend=true\n')
  fileNew.write('weblogic.StopScriptEnabled=true\n')
  fileNew.write('StateCheckInterval=500\n')
  fileNew.write('CrashRecoveryEnabled=true\n')
  fileNew.write('weblogic.StartScriptEnabled=false\n')
  fileNew.write('LogFile=%s/%s\n' % (nodeMgrHome,'nodemanager.log'))
  fileNew.write('LogFormatter=weblogic.nodemanager.server.LogFormatter\n')
  fileNew.write('ListenBacklog=50\n')
  fileNew.flush()
  fileNew.close()

def createNodeManagerDomianPropFile(nodeMgrHome, domainName, domainHome):
  print ('Create Nodemanager Domian Properties File for home: '+nodeMgrHome)
  nmDomian=nodeMgrHome+'/nodemanager.domains'
  fileNew=open(nmDomian, 'w')
  fileNew.write('#Node manager domian properties\n')
  fileNew.write(domainName + "=" + domainHome)
  fileNew.flush()
  fileNew.close()

createNodeManagerPropertiesFile(java_home, nm_home, nm_type, nm_address, nm_port)
createNodeManagerDomianPropFile(nm_home, domain_name, domain_home)
