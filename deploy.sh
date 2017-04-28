#!/bin/sh
curl -L https://github.com/EnMasseProject/enmasse/releases/download/0.8.0/enmasse-deploy.sh | bash /dev/stdin -c "https://openshift.amq.io:8443" -u demo -p enmasse -s server-cert.pem -k server-key.pem -t https://github.com/EnMasseProject/enmasse/releases/download/0.8.0/tls-enmasse-template.yaml
