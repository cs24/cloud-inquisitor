# aws-audits

This folder contains the source code and scripts to generate the Amazon Machine Images (AMI). For more information about the backend and frontend code, read the README's in the respective folders.

## Build Requirements

Before we get started you need to make sure you have the following software and information available on the machine you intend to run the build process on.

* packer
    * Instructions and links to downloads can be found at https://packer.io/downloads.html
    * Installation Methods can be found at https://www.packer.io/docs/installation.html
* VirtualBox - If you want to test using a local machine (much faster for rapid iteration than AMIs). Installer can be found at https://www.virtualbox.org/
* A base Ubuntu image that has a user (vagrant/vagrant) which can SSH and sudo. Image also requires curl to be installed.
* AWS API keys - For generating AMI's you need a pair of AWS Access and Secret keys with the appropriate permissions. https://www.packer.io/docs/builders/amazon.html contains a list of the permissions required for packer.

## Building an image

To build a new image is fairly trivial, all the files required for building images can be found in the `packer` folder. Inside this folder you will three folders (`files`, `scripts` and `variables`) and the main packer build script (`build.json`).

### files directory

```
files/
├── backend-settings.py
├── frontend-config.js
├── nginx-nossl.conf
├── nginx-ssl.conf
├── saml-settings.json
└── supervisor.conf
```

* `backend-settings.py` - template for the backend application configuration
    * Install location: `BACKEND_INSTALL_BASE/settings/production.py`
* `frontend-config.js` - template for the web frontend javascript application
    * Install location: `FRONTEND_INSTALL_BASE/js/awsaudits/config.js`
* `nginx-(ssl|nossl).conf` - the configuration files used for nginx, depending on whether or not SSL has been enabled
    * Install location: `/etc/nginx/sites-available/awsaudits.conf`
* `saml-settings.json` - configuration file for the SAML connector for the backend
    * Install location: `BACKEND_INSTALL_BASE/settings/settings.json`
* `supervisor.conf` - template for supervisor configuration
    * Install location: `/etc/supervisor/conf.d/awsaudits.conf`

### scripts directory

```
scripts/
└── install.sh
```
* `install.sh` - the main build script which handles doing the actual installation

### variables directory

This folder contains an example of the variables JSON file required to pass in variables for the installer script. Variables in packer can either be loaded from a file like the `example.json` or they can be passed in through the command line when running packer or a mix between file and command line arguments. Any arguments passed in through the command line will override both the variables file passed in as well as default values in the main packer build script

```
variables/
└── variables.json.sample
````

### build.json

This is the main build definition for packer which is where we define what and how to build.

### Building an image

To build a new version of AWS Audits (either AMI or OVA) all you need to do is run the following command, if you have all the variables setup in the file you are passing in.

```bash
packer build -only <builder-type> -var-file variables/production-variables.json build.json
```

The `-only <builder-type>` describes what type of machine you intend to build. This must be one of either `local` or `ami`. If you do not supply the `-only` argument, the script will attempt to build both an AMI and an OVA image.

### Overriding variables

You can, as previously mentioned, also override configuration variables from the command line. For example if you want to override the database password while building an Amazon AMI you would run the following command:

```bash
packer build -only ami -var-file variables/production.json \
   -var 'db_password=verysecretpassword' build.json
```

## Variables

This sections goes over all the available settings to tweak as well as their default values.
*N.B.* :: These values can and should all be modified in your production _variables_ file, you should not need to edit any values in `build.json`

**Packer Settings**

* `aws_access_key` - Access Key ID to use. Default: `AWS_ACCESS_KEY_ID` environment variable
* `aws_secret_key` - Secret Key ID to use. Default: `AWS_SECRET_ACCESS_KEY` environment variable
* `ec2_vpc_id` - ID of the VPC to launch the build instance into or default VPC if left blank. Default: `vpc-4a254c2f`
* `ec2_subnet_id` - ID of the subnet to launch the build instance into or default subnet if left blank. Default: `subnet-e7307482`
* `ec2_source_ami` - AMI to use as base image. Default: `ami-34d32354`
* `ec2_region` - EC2 Region to build AMI in. Default: `us-west-2`
* `ec2_ssh_username` - Username to SSH as for AMI builds. Default: `ubuntu`
* `ec2_security_groups` - Comma-separated list of EC2 Security Groups to apply to the instance on launch. Default: `sg-0c0aa368,sg-de1db4ba`
* `ec2_instance_profile` - Name of an IAM Instance profile to launch the instance with. Default: `AWSAuditsInstanceProfile`
 
* `vbox_base_ova_path` - Path to the base OVA / OVF image for VirtualBox builds. Default: `../../../ubuntu_base.ova`
* `vbox_ssh_username` - User to SSH as for Virtual Box builds. Default: `vagrant`
* `vbox_ssh_password` - Password for Virtual Box SSH access. Default: `vagrant`

**Installer Settings**

* `tmp_base` - Base folder for temporary files during installation, will be created if missing. Must be writable by the default ssh user. Default: `/tmp/packer`
* `install_base` - Base root folder to install to. Default: `/opt`
* `frontend_dir` - Subdirectory of `install_base` for frontend code. Default: `aws-audits-frontend`
* `backend_dir` - Subdirectory of `install_base` for backend code. Default: `aws-audits-backend`
* `app_apt_upgrade` - Run `apt-get upgrade` as part of the build process. Default: `True`

**Common Settings**

* `app_debug` - Run Flask in debug mode. Default: `False`

**Frontend Settings**

* `app_frontend_api_path` - Absolute path for API location. Default: `/api/v1`
* `app_frontend_login_url` - Absolute path for SAML Login redirect URL. Default: `/saml/login`

**Backend Settings**

* `app_db_uri` - **IMPORTANT:** Database connection URI. Default: `mysql://user:pass@localhost:3306/awsaudits`
* `app_api_host` - Hostname of the API backend. Default: `127.0.0.1`
* `app_api_port` - Port of the API backend. Default: `5000`
* `app_api_workers` - Number of worker threads for API backend. Default: `10`
* `app_ssl_enabled` - Enable SSL on frontend and backend. Default: `True`
* `app_ssl_cert_data` - Base64 encoded SSL public key data, used if not using self-signed certificates. Default: `None`
* `app_ssl_key_data` - Base64 encoded SSL private key data, used if not using self-signed certificates. Default: `None`

The vast majority of these settings should be left at their default values. Some items have been marked with **IMPORTANT**, meaning that the default values should never be used for anything other than local development work at best but ideally never be used at all. See `variables/variables.json.sample` for an example JSON variables file.

### Testing build

Once you have a succesful AMI built you should launch a new EC2 Instance based off the AMI to ensure that everything was installed correctly. Simply go to the EC2 console and Launch Instance,

![Launch EC2](https://gh.riotgames.com/OpSec/aws-audits/blob/master/images/ec2_dash.png "Launching EC2")

and then select the AMI you just created:

![Create from AMI](https://gh.riotgames.com/OpSec/aws-audits/blob/master/images/my_ami_dash.png "Create from AMI")

- As soon as the instance is up, connect to it via _ssh_.

- Check the status of the awsaudits processes in supervisor by running `sudo supervisorctl`, which should return

```bash
# supervisorctl status
awsaudits                   RUNNING    pid 4393, uptime 18 days, 18:55:44
awsaudits-scheduler         RUNNING    pid 22707, uptime 13 days, 0:23:28
```
If both processes are not in the *RUNNING* state, then please review:

* the */var/log/supervisor/awsaudits* file for errors. There is most likely an issue in your JSON *variables* file, so you should do a direct comparison with the production */opt/aws-audits-backend/settings/production.py* file.
* or the packer build output for errors (the _variables json_ file can sometimes be the issue with incorrect database details/credentials).

Once you have verified that both processes are running, you should terminate the scheduler since having multiple schedulers running at the same time can cause issues. To do this from the shell :

* run `supervisorctl stop awsaudits-scheduler`.
or from within the _supervisorctl_ prompt
* `supervisor> stop awsaudits-scheduler`
which results in

```bash
supervisor> status
awsaudits                   RUNNING    pid 1168, uptime 0:04:52
awsaudits-scheduler         STOPPED    Oct 13 05:32 PM
```

Once you have verified that everything is running as expected you can terminate the EC2 Instance.

### Updating AutoScalingGroup launch configurations
Once you have tested the image is good, you want to update the Launch Configuration for the ASG. Follow the steps below.

#### Creating Launch Configuration

1. Log into the AWS Console and go to the EC2 section
2. Click `Launch Configurations` in the `Auto Scaling` section
3. Locate the currently active Launch Configuration, right click it and choose `Copy launch configuration`. To identify the currently active Launch Configuration you can look at the details for the Auto Scaling Group itself.
4. On the first screen, click `Edit AMI` and paste the AMI ID you got from the packer build (or search by ami name)
5. Once you select the new AMI, the console will ask you to confirm that you want to proceed with the new AMI, select `Yes, I want to continue with this AMI` and click Next
6. On the instance type page, simply click `Next: Configure details` without modifying anything. The correct instance type will be pre-selected
7. On the Details page you want to modify the Name attribute of the launch configuration. Name should follow the standard `aws-audits-<year>-<month>-<day>_<index>` with index being an increasing number based per day. So the first launch configuration for a specific day is _1. Ideally you shouldn't have to make multiple revisions in a single day, but this lets us easily revert to a previous version if we need to. You should ensure that the IAM role is correctly set to `AWSAuditsInstanceProfile`.
8. After changing the launch configuration name, click the Next buttons until you reach the Review page. Make sure all the changes you made are reflected on the Review page and then hit `Create launch configuration`. Once you click create it will ask you to select the key-pair, select an appropriate key-pair and click the Create button. Our base AMI have the InfraSec SSH keys baked into it, so you should not need to worry too much about the key-pair, but its still a good idea to use a key-pair the entire team has access to, just in case.

#### Updating AutoScalingGroup

1. Notify the AWS Working Group on slack that you will be performing maintenance and AWS Audits will be unavailable briefly
2. Click on `Auto Scaling Groups` in the `EC2 Dashboard`
3. Locate the ASG you want to update, right click it and select `Edit`
4. From the `Launch Configuration` drop down box, locate the configuration you created in the previous step
5. Click `Save`
6. With the ASG selected, click on the `Instances` tab in the details pane.
7. Click on the instance ID to be taken to the details page for the EC2 instance
8. Right click EC2 Instance and select terminate. This will trigger the ASG to launch a new instance from the updated launch configuration on the new AMI. This process takens 3-5 minutes during which time AWS Audits will be unavailable
9. Go back to the ASG details page for the AWS Audits ASG, and by clicking the Refresh icon monitor that a new instance is being launched and goes into `InService` status. Once the new instance is in service verify that you are able to log into the UI at *https://aws-audits.service.riotgames.com/* or whatever the relevant URL is.
10. Update the AWS Working Group on Slack that AWS Audits is back in production
