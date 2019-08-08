#Copyright (c) 2014-2018 Oracle and/or its affiliates. All rights reserved.
#
#Licensed under the Universal Permissive License v 1.0 as shown at http://oss.oracle.com/licenses/upl.
#
# Script to create and add a Managed Server automatically to the domain's AdminServer running on 'wlsadmin'.
#
# Since: October, 2014
# Author: bruno.borges@oracle.com
#
# =============================
import os
import random
import string
import socket

cluster_name  = os.environ.get("CLUSTER_NAME", "DockerCluster")
ms_port   = int(os.environ.get("MS_PORT", "9001"))
ms_ssl_port   = int(os.environ.get("MS_SSL_PORT", ms_port + 10))

print('cluster_name     : [%s]' % cluster_name);
print('ms_port          : [%s]' % ms_port);
print('ms_ssl_port      : [%s]' % ms_ssl_port);

execfile('/oracle/commonfuncs.py')

# Functions
def randomName():
  return ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(6)])


# ManagedServer details
msinternal = socket.gethostbyname(hostname)
msname = os.environ.get('MS_NAME', 'ManagedServer-%s@%s' % (randomName(), hostname))
nmname = os.environ.get('NM_NAME', 'Machine-' + hostname)
mshost = os.environ.get('MS_HOST', msinternal)
msport = os.environ.get('MS_PORT', ms_port)
mssslport = os.environ.get('MS_SSL_PORT', ms_ssl_port)
mssslportenabled = os.environ.get('MS_SSL_PORT_ENABLED', 'false')
memargs = os.environ.get('USER_MEM_ARGS', '')
instanceargs = os.environ.get('USER_INSTANCE_ARGS', '')
classpathargs = os.environ.get('CLASSPATH_ARGS', '')
addtoclstr = os.environ.get('ADD_TO_CLSTR', 'false')
wlplugin = os.environ.get('WL_PLUGIN', 'false')
msselfsignssl = os.environ.get('SELF_SIGN_SSL', 'false')

# Self sign certificate variables
ksIdentityPath=os.environ.get('IDENTITY_PATH','/oracle/middleware/user_projects/keystore/identity.jks')
ksIdentityPassword=os.environ.get('IDENTITY_PASSWORD','password1')
ksTrustPath=os.environ.get('TRUST_PATH','/oracle/middleware/user_projects/keystore/trust.jks')
ksTrustPassword=os.environ.get('TRUST_PASSWORD','password1')
ksPhrase=os.environ.get('KS_PHRASE','password1')
ksPkAlias=os.environ.get('PK_ALIAS','selfsigned')

print('msname     : [%s]' % msname);
print('nmname     : [%s]' % nmname);
print('mshost     : [%s]' % mshost);
print('msport     : [%s]' % msport);
print('mssslport  : [%s]' % mssslport);
print('mssslportenabled  : [%s]' % mssslportenabled);
print('memargs    : [%s]' % memargs);
print('classpathargs : [%s]' % classpathargs);
print('instanceargs : [%s]' % instanceargs);
print('addtoclstr : [%s]' % addtoclstr);
print('wlplugin : [%s]' % wlplugin);
# Connect to the AdminServer
# ==========================
connectToAdmin()

# Create a ManagedServer
# ======================
editMode()
cd('/')
cmo.createServer(msname)

cd('/Servers/' + msname)
cmo.setMachine(getMBean('/Machines/%s' % nmname))
if addtoclstr == 'true':
  print ("\n")
  print ('Adding to cluster...'+"\n")
  cmo.setCluster(getMBean('/Clusters/%s' % cluster_name))
else:
  print ("\n")
  print ('Adding as standalone instance...'+"\n")

# Default Channel for ManagedServer
# ---------------------------------
cmo.setListenAddress(msinternal)
cmo.setListenPort(int(msport))
cmo.setListenPortEnabled(true)
cmo.setExternalDNSName(mshost)

# Enable SSL Port for this ManagedServer if SSL port is specified
# ----------------------------------
if mssslportenabled == 'true':
  print ("\n")
  print('Enabling SSL port...'+"\n")
  cd('/Servers/%s/SSL/%s' % (msname, msname))
  cmo.setEnabled(true)
  set('ListenPort', int(mssslport))

if msselfsignssl == 'true':  
  # Set keystore information.
  print ("\n")
  print('Enabling self sign ssl certificate...'+"\n")
  cd('/Servers/' + msname)
  cmo.setKeyStores('CustomIdentityAndCustomTrust')

  cmo.setCustomIdentityKeyStoreFileName(ksIdentityPath)
  cmo.setCustomIdentityKeyStoreType('JKS')
  set('CustomIdentityKeyStorePassPhrase', ksIdentityPassword)
  cmo.setCustomTrustKeyStoreFileName(ksTrustPath)
  cmo.setCustomTrustKeyStoreType('JKS')
  set('CustomTrustKeyStorePassPhrase', ksTrustPassword)

  cd('/Servers/' + msname + '/SSL/' + msname)
  cmo.setServerPrivateKeyAlias(ksPkAlias)
  set('ServerPrivateKeyPassPhrase', ksPhrase)

  cmo.setHostnameVerificationIgnored(false)
  cmo.setHostnameVerifier(None)
  cmo.setTwoWaySSLEnabled(false)
  cmo.setClientCertificateEnforced(false)
  cmo.setJSSEEnabled(true)

if wlplugin == 'true':
  print ("\n")
  print('Enabling WL Plugin...'+"\n")
  cd('/Servers/' + msname)
  cmo.setWeblogicPluginEnabled(true)
  

# Custom Startup Parameters because NodeManager writes wrong AdminURL in startup.properties
# -----------------------------------------------------------------------------------------
cd('/Servers/%s/ServerStart/%s' % (msname, msname))
arguments = '-Djava.security.egd=file:/dev/./urandom -Dweblogic.Name=%s -Dweblogic.management.server=http://%s:%s %s %s' % (msname, admin_host, admin_port, memargs, instanceargs)
cmo.setArguments(arguments)
if classpathargs != "":
  classpath = (classpathargs)
  cmo.setClassPath(classpath)
saveActivate()

# Start Managed Server
# ------------
try:
    start(msname, 'Server')
except:
    dumpStack()

# Exit
# =========
exit()

