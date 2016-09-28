FROM scratch
ADD rootfs.tar.gz /
RUN apk --update add openssh
RUN apk --update add git
RUN apk --update add bash
RUN apk --update add gcc
RUN apk --update add openssl
RUN apk --update add openssl-dev
RUN apk --update add libffi-dev
RUN apk --update add musl-dev
RUN apk --update add python-dev
RUN apk --update add python && rm -f /var/cache/apk/*
RUN ssh-keygen -A
RUN echo "PermitRootLogin yes" >> /etc/ssh/sshd_config && \
  echo "PasswordAuthentication no" >> /etc/ssh/sshd_config && \
  echo "ChallengeResponseAuthentication no" >> /etc/ssh/sshd_config && \
  echo "Port 9022" >> /etc/ssh/sshd_config && \
  echo "StrictModes no" >> /etc/ssh/sshd_config

RUN adduser -D dev && passwd -d dev && mkdir /home/dev/.ssh && chown dev:nogroup /home/dev/.ssh && chmod 700 /home/dev/.ssh
VOLUME /home/dev/.ssh
RUN mkdir /root/.ssh && chown root:root /root/.ssh && chmod 700 /root/.ssh
VOLUME /root/.ssh
ADD motd /etc/motd
ADD harden.sh /usr/bin/harden.sh
RUN chmod 700 /usr/bin/harden.sh && /bin/ash /usr/bin/harden.sh
USER root
CMD ["/usr/sbin/sshd", "-D"]
