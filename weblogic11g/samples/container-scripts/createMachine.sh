#!/bin/bash
#
#Copyright (c) 2014-2018 Oracle and/or its affiliates. All rights reserved.
#
#Licensed under the Universal Permissive License v 1.0 as shown at http://oss.oracle.com/licenses/upl.
#

# If log.nm does not exists, container is starting for 1st time
# So it should start NM and also associate with AdminServer
# Otherwise, only start NM (container restarted)
if [ ! -f $DOMAIN_HOME/nodemanager_logs/$MS_NAME.log ]; then
  echo "Cannot find node manager log file..." 
  ADD_MACHINE=1
else
  ADD_MACHINE=-1
fi

# Wait for AdminServer to become available for any subsequent operation
/oracle/waitForAdminServer.sh

# Update nodemanager properties file if runnig first time

if [ $ADD_MACHINE -eq 1 ]; then
  echo "Trying to create node manager properties file for the first time..."
  wlst.sh create-nm-profile.py
fi

# Start Node Manager
echo "Starting NodeManager in background..."
nohup startNodeManager.sh > $DOMAIN_HOME/nodemanager_logs/$MS_NAME.log 2>&1 &
echo "NodeManager started."

# Add a Machine to the AdminServer only if 1st execution
if [ $ADD_MACHINE -eq 1 ]; then
  echo "Trying to add machine to domain for the first time..."
  wlst.sh /oracle/add-machine.py
fi

# print log
tail -f $DOMAIN_HOME/nodemanager_logs/$MS_NAME.log

