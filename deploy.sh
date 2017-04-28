#!/bin/sh
curl -L https://github.com/EnMasseProject/enmasse/releases/download/0.9.0/enmasse-deploy.sh -o enmasse-deploy.sh
bash enmasse-deploy.sh -c "https://openshift.amq.io:8443" -u admin -p enmasse -s server-cert.pem -k server-key.pem -t https://github.com/EnMasseProject/enmasse/releases/download/0.9.0/sasldb-tls-enmasse-template.yaml
