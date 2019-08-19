#!/bin/bash
#
#Copyright (c) 2014-2018 Oracle and/or its affiliates. All rights reserved.
#
#Licensed under the Universal Permissive License v 1.0 as shown at http://oss.oracle.com/licenses/upl.
#
echo "Domain Home is: " $DOMAIN_HOME
echo "Managed Server Name: "  $MS_NAME
echo "NodeManager Name: "  $NM_NAME

if [ -z $ADMIN_PASSWORD ]; then
   echo "      ----> NO 'weblogic' admin password set"
   echo ""
else
   s=${ADMIN_PASSWORD}
   echo "      ----> 'weblogic' admin password: $s"
fi
sed -i -e "s|ADMIN_PASSWORD|$s|g" /oracle/commonfuncs.py

# If log.nm does not exists, container is starting for 1st time
# So it should start NM and also associate with AdminServer, as well Managed Server
# Otherwise, only start NM (container is being restarted)
if [ ! -f $DOMAIN_HOME/nodemanager_logs/$MS_NAME.log ]; then
  echo "Cannot find node manager log file..."
  ADD_SERVER=1
else
  ADD_SERVER=-1
fi

# Wait for AdminServer to become available for any subsequent operation
/oracle/waitForAdminServer.sh

# Update nodemanager properties file if runnig first time

if [ $ADD_SERVER -eq 1 ]; then
  echo "Trying to create node manager properties file for the first time..."
  wlst.sh create-nm-profile.py
fi

# Set and Start Node Manager
echo "Setting NodeManager"
if [ -z $NM_NAME ]; then
  echo "      ----> No NodeManager Name set"
  NM_NAME="Machine_$MS_NAME"
  echo "Node Manager Name: " $NM_NAME
  export $NM_NAME
fi

NODEMGR_HOME_STR="NODEMGR_HOME=\"$NM_HOME\""
DOMAINSFILE_STR="DomainsFile=$NM_HOME/nodemanager.domains"
NODEMGRHOME_STR="NodeManagerHome=$NM_HOME"
LOGFILE_STR="LogFile=$DOMAIN_HOME/nodemanager_logs/$MS_NAME.log"

echo "NODEMGR_HOME_STR: " $NODEMGR_HOME_STR
echo "NODEMGRHOME_STR: " $NODEMGRHOME_STR
echo "DOMAINSFILE_STR: " $DOMAINSFILE_STR
echo "LOGFILE_STR: " $LOGFILE_STR

echo "Starting NodeManager in background..."
nohup startNodeManager.sh > $DOMAIN_HOME/nodemanager_logs/$MS_NAME.log 2>&1 &
echo "NodeManager started."

# Add this 'Machine' and 'ManagedServer' to the AdminServer only if 1st execution
if [ $ADD_SERVER -eq 1 ]; then
 # Create managed server and nodemanager
  wlst.sh /oracle/add-machine.py
  wlst.sh /oracle/add-server.py
# Create datasources if passed as comma separeted variable
if [ -z "$DS_LIST" ]; then
    echo "No datasource will be created..."
  else
  for i in $(echo $DS_LIST | sed "s/,/ /g")
  do
    echo "$i DS will be created..."
    wlst.sh /oracle/create-data-source.py -p /oracle/datasource_properties/$i
    wlst.sh /oracle/target-data-source.py -p /oracle/datasource_properties/$i
  done
fi
 # Assign self-signed ssl if requested
  if [ "$SELF_SIGN_SSL" = true ]; then
    wlst.sh /oracle/set-keystore.py
  fi
fi

# print log
tail -f $DOMAIN_HOME/nodemanager_logs/$MS_NAME.log $DOMAIN_HOME/servers/$MS_NAME/logs/$MS_NAME.out

