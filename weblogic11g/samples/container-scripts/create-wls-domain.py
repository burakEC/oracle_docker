#Copyright (c) 2014-2018 Oracle and/or its affiliates. All rights reserved.
#
#Licensed under the Universal Permissive License v 1.0 as shown at http://oss.oracle.com/licenses/upl.
#
# WebLogic on Docker Default Domain
#
# Domain, as defined in DOMAIN_NAME, will be created in this script. Name defaults to 'base_domain'.
#
# Since : July, 2017
# Author: monica.riccelli@oracle.com
# ==============================================
#Env Vars
# ------------------------------
import os
import socket

domain_name      = os.environ.get("DOMAIN_NAME")
admin_name       = os.environ.get("ADMIN_NAME", "AdminServer")
admin_host       = os.environ.get("ADMIN_HOST", '')
admin_port       = int(os.environ.get("ADMIN_PORT", "7001"))
admin_pass       = os.environ.get("ADMIN_PASSWORD", "welcome1")
cluster_name     = os.environ.get("CLUSTER_NAME", "DockerCluster")
domain_path      = os.environ.get("DOMAIN_HOME")
production_mode  = os.environ.get("MODE", "prod")

print('domain_name     : [%s]' % domain_name);
print('admin name      : [%s]' % admin_name);
print('admin pass      : [%s]' % admin_pass);
print('admin_host      : [%s]' % admin_host);
print('admin_port      : [%s]' % admin_port);
print('cluster_name    : [%s]' % cluster_name);
print('domain_path     : [%s]' % domain_path);
print('production_mode : [%s]' % production_mode);

# Open default domain template
# ======================
readTemplate("/oracle/middleware/wlserver/common/templates/domains/wls.jar")

set('Name', domain_name)
setOption('DomainName', domain_name)

# Disable Admin Console
# --------------------
# cmo.setConsoleEnabled(false)

# Configure the Administration Server and SSL port.
# =========================================================
cd('/Servers/AdminServer')
set('Name', admin_name)
set('ListenAddress', admin_host)
set('ListenPort', admin_port)

create('AdminServer','SSL')
cd('SSL/AdminServer')
set('Enabled', 'True')
set('ListenPort', admin_port + 10)

cd('/Servers/AdminServer/SSL/AdminServer')
cmo.setHostnameVerificationIgnored(true)
cmo.setHostnameVerifier(None)
cmo.setTwoWaySSLEnabled(false)
cmo.setClientCertificateEnforced(false)

# Define the user password for weblogic
# =====================================
cd('/Security/%s/User/weblogic' % domain_name)
cmo.setPassword(admin_pass)

# Write the domain and close the domain template
# ==============================================
setOption('OverwriteDomain', 'true')
setOption('ServerStartMode',production_mode)

# Setting the JDK home. Change the path to your installed JDK for weblogic
#setOption('JavaHome','/usr/lib/jvm/java-1.6.0-jrockit-1.6.0.45_R28.2.7_4.1.0.x86_64/jre')
#setOption('OverwriteDomain', 'true')

#cd('/')
#create(machine_name, 'UnixMachine')
#cd('Machines/' + machine_name)
#create(machine_name, 'NodeManager')
#cd('NodeManager/' + machine_name)
#set('NMType', 'Plain')
#set('ListenAddress', nm_address)
#set('ListenPort', int(nm_port))

#set('CrashRecoveryEnabled', 'true')
#set('NativeVersionEnabled', 'true')
#set('StartScriptEnabled', 'false')
#set('SecureListener', 'false')
#set('LogLevel', 'FINEST')
#set('DomainsDirRemoteSharingEnabled','true')

# Set the Node Manager user name and password (domain name will change after writeDomain)
#cd('/SecurityConfiguration/base_domain')
#set('NodeManagerUsername', 'weblogic')
#set('NodeManagerPasswordEncrypted', admin_pass)

# Define a WebLogic Cluster
# =========================
cd('/')
create(cluster_name, 'Cluster')

cd('/Clusters/%s' % cluster_name)
cmo.setClusterMessagingMode('unicast')

# Write Domain
# ============
writeDomain(domain_path)
closeTemplate()

# Exit WLST
# =========
exit()
