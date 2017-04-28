# Setting up EnMasse on AWS EC2

This guide will walk through setting up EnMasse on an AWS EC2 instance.

## Prerequisites

First, you must have created an [EC2 instance](https://aws.amazon.com/ec2/).i EnMasse runs on OpenShift and Kubernetes. For this guide, we will install OpenShift, so have a look at the [OpenShift prerequisites](https://docs.openshift.org/latest/install_config/install/prerequisites.html) for the required hardware configuration. The installation will be done using [ansible](https://www.ansible.com), so make sure ansible is installed on laptop or workstation.

### Configure ansible to handle passwordless sudo

For EC2 instance, the default is a passwordless sudo, and ansible requires a minor configuration modification to deal with that.  On the host you will be running ansible from, edit /etc/ansible/ansible.cfg, and make sure that the `sudo_flags` parameter is set to `-H -S` (remove the `-n`).

## Setting up OpenShift

Installing OpenShift is easy, especially when using [ansible](https://www.ansible.com). Save the
following configuration to a file called `ansible-inventory.txt`:

    [OSEv3:children]
    masters
    nodes

    [OSEv3:vars]
    deployment_type=origin
    openshift_master_identity_providers=[{'name': 'htpasswd_auth', 'login': 'true', 'challenge': 'true', 'kind': 'HTPasswdPasswordIdentityProvider', 'filename': '/etc/origin/master/htpasswd'}]
    openshift_master_default_subdomain=<yourdomain>
    openshift_public_hostname=openshift.<yourdomain>
    openshift_hostname=<ec2 instance hostname>
    openshift_metrics_hawkular_hostname=hawkular-metrics.<yourdomain>

    openshift_install_examples=false
    openshift_hosted_metrics_deploy=true

    [masters]
    <ec2 host> openshift_scheduleable=true openshift_node_labels="{'region': 'infra'}"

    [nodes]
    <ec2 host> openshift_scheduleable=true openshift_node_labels="{'region': 'infra'}"

If you don't have a domain with wildcard support, you can replace <yourdomain> with <ip>.nip.io, and
you will have a working setup without having a specialized domain. This will setup OpenShift so that
it can only be accessed by users defined in `/etc/origin/master/htpasswd`.

You can now download the ansible playbooks. The simplest way to do this is to just clone the git
repository:

    git clone https://github.com/openshift/openshift-ansible.git

To install OpenShift, run the playbook like this

    ansible-playbook -u ec2-user -b --private-key=<keyfile>.pem -i ansible-inventory.txt openshift-ansible/playbooks/byo/openshift-cluster/config.yml

This command will take a while to finish.

### Creating a user

To be able to deploy applications in OpenShift, a user must be created. Log on to your EC2
instance, and create the user:

    htpasswd -c /etc/origin/master/htpasswd <myuser>

Where `<myuser>` is the username you want to use. The command will prompt you for a password that
you will later use when deploying EnMasse.

## (Optional) Setting up grafana

Although the openshift ansible deployment installs hawkular to store the metrics, it does not
provide any way to view metrics. 

## Creating certificates

To be able to access your EnMasse cluster outside OpenShift, you must create a certificate for it.
For testing purposes, you can create a self-signed key and certificate like this:

    openssl req -new -x509 -batch -nodes -out server-cert.pem -keyout server-key.pem

## Setting up EnMasse

You can find the latest version of EnMasse [here](https://github.com/EnMasseProject/enmasse/releases/latest). To deploy EnMasse, it is recommended to use the deploy script together with a template of the latest version. At the time of writing, the latest version is 0.8.0, which can be deployed as follows:

    curl -L https://github.com/EnMasseProject/enmasse/releases/download/0.8.0/enmasse-deploy.sh -o enmasse-deploy.sh
    bash enmasse-deploy.sh -c https://openshift.<yourdomain>:8443 -p enmasse -t https://github.com/EnMasseProject/enmasse/releases/download/0.8.0/tls-enmasse-template.yaml -u <myuser> -k server-key.pem -s server-cert.pem

Now you have EnMasse deployed 
