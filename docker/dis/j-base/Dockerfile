FROM openjdk:8-jre-slim

ARG JMETER_VERSION=5.0

RUN apt-get clean && \
    apt-get update && \
    apt-get -qy install \
                wget \
                telnet \
                net-tools \
                vim

RUN mkdir /jmeter \
	&& cd /jmeter/ \
	&& wget https://archive.apache.org/dist/jmeter/binaries/apache-jmeter-$JMETER_VERSION.tgz \
	&& tar -xzf apache-jmeter-$JMETER_VERSION.tgz \
	&& rm apache-jmeter-$JMETER_VERSION.tgz

ENV JMETER_HOME /jmeter/apache-jmeter-$JMETER_VERSION/

ENV PATH $JMETER_HOME/bin:$PATH

WORKDIR $JMETER_HOME

COPY config/user.properties bin/user.properties
COPY scripts/install_plugin-manager.sh .
COPY scripts/docker-entrypoint.sh /docker-entrypoint.sh

RUN chmod +x install_plugin-manager.sh /docker-entrypoint.sh
RUN ./install_plugin-manager.sh

EXPOSE 6000 1099 50000
ENTRYPOINT ["/docker-entrypoint.sh"]
