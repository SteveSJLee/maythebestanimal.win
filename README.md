# This is the Ansible deployment system for the animal-voting Flask app.
Please have git and python's virtualenv tool installed before beginning.

## To run the example playbooks:
1) Export your AWS credentials and AWS_REGION environment variables; e.g
```
  export AWS_ACCESS_KEY_ID={your AWS access key}
  export AWS_SECRET_ACCESS_KEY={your AWS secret key}
  export AWS_REGION=us-east-1
```

2) Clone the project and enter the directory:
```  
  git clone https://github.com/bretttegart/maythebestanimal.win.git && cd maythebestanimal.win/ansible
```

3) Create a virtualenv and install Ansible packages:
```
  virtualenv --python=python2 venv && . venv/bin/activate
  pip install -r requirements.txt
```

4) Review the global_vars.yml, aws_vars.yml, and app_vars.yml. Substitute your own values for any of the variables marked with {key}

5) (Optional) If desired, create AWS VPC and subnet:
```
  ansible-playbook -i inventory -e @global_vars.yml -e @aws_vars.yml aws_setup_playbook.yml
```

This will create the Animal_Voting VPC, a public subnet and internet gateway, an AWS instance, and tag it as Class: Webserver.

If you run this script, please allow the instance 2 minutes to start up before continuing. You can test if the instance is ready by connecting to its public IP using the AWS keypair you specified in step 4. For Fedora Atomic Host, the SSH username is "fedora".

6) Provision and start the Flask app:
```
  ansible-playbook -i ec2.py \
  -u fedora \
  --private-key ~/.ssh/{your-AWS-keypair} \
  -e @global_vars.yml \
  -e @app_vars.yml \
  host_configuration_playbook.yml
```

7) Point your domain DNS at the EC2 public IP address!


Security features:
- Firewalls at the AWS security group and instance level- SSH, HTTP and HTTPS are the only accessible services
- MySQL is inaccessible from outside the Docker virtual network
- Fedora Atomic Linux on the host greatly reduces attack surface and configuration drift- most of the filesystem is read-only and system can only be updated via signed atomic update images. SELinux is installed and enforced.

Ways to improve security:
- Limit SSH on AWS security group to known IP pool
- Set up regular Atomic updates, centralized cron, system logging, and backups
- Install Cloudflare TLS certificate on load balancer for encrypted traffic between Cloudflare and webservers. At that point port 80 can be closed.

Ways to easily scale:
- Break out database container to its' own instance, with attached GP2 SSD volume for DB storage.
- Stand up Elastic Load Balancer or HAProxy in front of webservers
- Container could be easily set up with Elastic Beanstalk
- Kubernetes cluster is easy to set up with Fedora Atomic Host- this would allow for instance-level failover and would provide an excellent load balancing framework.
