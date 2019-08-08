# LICENSE CDDL 1.0 + GPL 2.0
#
# ORACLE DOCKERFILES PROJECT
# --------------------------
# This Dockerfile extends an Oracle WebLogic image by creating a sample domain.
# Util scripts are copied into the image enabling users to plug NodeManager 
# magically into the AdminServer running on another container as a Machine.
#
# HOW TO BUILD THIS IMAGE
# -----------------------
# Put all downloaded files in the same directory as this Dockerfile
# Run: 
#      $ sudo docker build -t myweblogic .
#

# Pull base image
# ---------------
FROM oracle/weblogic:10.3.6

# Maintainer
# ----------
MAINTAINER Burak Emre COLAK <bcolak@innova.com.tr>

# WLS Admin Password (change it!)
# -------------------------------
ENV DOMAIN_NAME dockerdomain

# Get timezone from host (run tihs on host before -> timedatectl | awk '/Time zone:/ {print $3}' > /etc/timezone_host)
# -------------------------------
USER root
ARG timezone
ENV TZ=${timezone:-Europe/Istanbul}
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Add files required to build this image
COPY container-scripts/. /oracle/

USER root
RUN chown -R oracle.oracle /oracle/*

# Root commands
USER root
ENV DOMAIN_NAME dedasqa
RUN echo ". /oracle/middleware/user_projects/domains/$DOMAIN_NAME/bin/setDomainEnv.sh" >> /root/.bashrc && \
    echo "export PATH=$PATH:/oracle/middleware/wlserver/server/bin:/oracle/middleware/wlserver/common/bin:/oracle/middleware/user_projects/domains/$DOMAIN_NAME/bin" >> /root/.bashrc

# Configuration of WLS Domain
USER oracle
WORKDIR /oracle/middleware
RUN echo $DOMAIN_NAME
RUN echo ". /oracle/middleware/user_projects/domains/$DOMAIN_NAME/bin/setDomainEnv.sh" >> /oracle/.bashrc && \ 
    echo "export PATH=$PATH:/oracle/middleware/wlserver/server/bin:/oracle/middleware/wlserver/common/bin:/oracle/middleware/user_projects/domains/$DOMAIN_NAME/bin" >> /oracle/.bashrc

# Expose Node Manager default port, and also default http/https ports for admin console
EXPOSE $NM_PORT $ADMIN_PORT $ADMIN_PORT_SSL

# Final setup
WORKDIR /oracle

ENV PATH $PATH:/oracle/middleware/wlserver/server/bin:/oracle/middleware/wlserver/common/bin:/oracle/middleware/user_projects/domains/$DOMAIN_NAME/bin:/oracle

# Define default command to start bash. 
CMD ["createAndStartWLSDomain.sh"]
