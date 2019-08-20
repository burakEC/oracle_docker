#!/usr/bin/python
# Author : Tim Hall
# Save Script as : set_keystore.py

import time
import getopt
import sys
import re

# Set all variables from values in properties file.
msName=os.environ.get('MS_NAME')
ksIdentityPath=os.environ.get('IDENTITY_PATH','/oracle/middleware/user_projects/keystore/identity.jks')
ksIdentityPassword=os.environ.get('IDENTITY_PASSWORD','password1')
ksTrustPath=os.environ.get('TRUST_PATH','/oracle/middleware/user_projects/keystore/trust.jks')
ksTrustPassword=os.environ.get('TRUST_PASSWORD','password1')
ksPhrase=os.environ.get('KS_PHRASE','password1')
ksPkAlias=os.environ.get('PK_ALIAS','selfsigned')

# Display the variable values.
print 'msName=', msName
print 'ksIdentityPath=', ksIdentityPath
print 'ksIdentityPassword=', ksIdentityPassword
print 'ksTrustPath=', ksTrustPath
print 'ksTrustPassword=', ksTrustPassword
print 'ksPhrase=', ksPhrase
print 'ksPkAlias=', ksPkAlias

execfile('/oracle/commonfuncs.py')

# Connect to the AdminServer.
connectToAdmin()

edit()
startEdit()

# Set keystore information.
cd('/Servers/' + msName)
cmo.setKeyStores('CustomIdentityAndCustomTrust')

activate()

startEdit()
cmo.setCustomIdentityKeyStoreFileName(ksIdentityPath)
cmo.setCustomIdentityKeyStoreType('JKS')
set('CustomIdentityKeyStorePassPhrase', ksIdentityPassword)
cmo.setCustomTrustKeyStoreFileName(ksTrustPath)
cmo.setCustomTrustKeyStoreType('JKS')
set('CustomTrustKeyStorePassPhrase', ksTrustPassword)

activate()

startEdit()

cd('/Servers/' + msName + '/SSL/' + msName)
cmo.setServerPrivateKeyAlias(ksPkAlias)
set('ServerPrivateKeyPassPhrase', ksPhrase)

cmo.setHostnameVerificationIgnored(false)
cmo.setHostnameVerifier(None)
cmo.setTwoWaySSLEnabled(false)
cmo.setClientCertificateEnforced(false)
cmo.setJSSEEnabled(true)

save()
activate()

try:
    stop(msName, 'Server')
    start(msName, 'Server')
except:
    dumpStack()

disconnect()
exit()
