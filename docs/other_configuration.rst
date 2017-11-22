
---------
Variables
---------

This section goes over all the available settings to tweak as well as their default values.
**N.B.** :: These values can and should all be modified in your production _variables_ file, you should not need to edit any values in ``build.json``

^^^^^^^^^^^^^^^
Packer Settings
^^^^^^^^^^^^^^^

* ``aws_access_key`` - Access Key ID to use. Default: `AWS_ACCESS_KEY_ID` environment variable
* ``aws_secret_key`` - Secret Key ID to use. Default: `AWS_SECRET_ACCESS_KEY` environment variable
* ``ec2_vpc_id`` - ID of the VPC to launch the build instance into or default VPC if left blank. Default: `vpc-4a254c2f`
* ``ec2_subnet_id`` - ID of the subnet to launch the build instance into or default subnet if left blank. Default: `subnet-e7307482`
* ``ec2_source_ami`` - AMI to use as base image. Default: `ami-34d32354`
* ``ec2_region`` - EC2 Region to build AMI in. Default: `us-west-2`
* ``ec2_ssh_username`` - Username to SSH as for AMI builds. Default: `ubuntu`
* ``ec2_security_groups`` - Comma-separated list of EC2 Security Groups to apply to the instance on launch. Default: `sg-0c0aa368,sg-de1db4ba`
* ``ec2_instance_profile`` - Name of an IAM Instance profile to launch the instance with. Default: `CinqInstanceProfile`

* ``vbox_base_ova_path`` - Path to the base OVA / OVF image for VirtualBox builds. Default: `../../../ubuntu_base.ova`
* ``vbox_ssh_username`` - User to SSH as for Virtual Box builds. Default: `vagrant`
* ``vbox_ssh_password`` - Password for Virtual Box SSH access. Default: `vagrant`

^^^^^^^^^^^^^^^^^^
Installer Settings
^^^^^^^^^^^^^^^^^^

* ``tmp_base`` - Base folder for temporary files during installation, will be created if missing. Must be writable by the default ssh user. Default: `/tmp/packer`
* ``install_base`` - Base root folder to install to. Default: `/opt`
* ``frontend_dir`` - Subdirectory of `install_base` for frontend code. Default: `cinq-frontend`
* ``backend_dir`` - Subdirectory of `install_base` for backend code. Default: `cinq-backend`
* ``app_apt_upgrade`` - Run `apt-get upgrade` as part of the build process. Default: `True`

^^^^^^^^^^^^^^^
Common Settings
^^^^^^^^^^^^^^^

* ``app_debug`` - Run Flask in debug mode. Default: `False`

^^^^^^^^^^^^^^^^^
Frontend Settings
^^^^^^^^^^^^^^^^^

* ``app_frontend_api_path`` - Absolute path for API location. Default: `/api/v1`
* ``app_frontend_login_url`` - Absolute path for SAML Login redirect URL. Default: `/saml/login`

^^^^^^^^^^^^^^^^
Backend Settings
^^^^^^^^^^^^^^^^

* ``app_db_uri`` - **IMPORTANT:** Database connection URI. Example: ``mysql://cinq:changeme@localhost:3306/cinq``
* ``app_api_host`` - Hostname of the API backend. Default: ``127.0.0.1``
* ``app_api_port`` - Port of the API backend. Default: ``5000``
* ``app_api_workers`` - Number of worker threads for API backend. Default: ``10``
* ``app_ssl_enabled`` - Enable SSL on frontend and backend. Default: ``True``
* ``app_ssl_cert_data`` - Base64 encoded SSL public key data, used if not using self-signed certificates. Default: ``None``
* ``app_ssl_key_data`` - Base64 encoded SSL private key data, used if not using self-signed certificates. Default: ``None``


===
FYI
===
The vast majority of these settings should be left at their default values. Some items have been marked as **IMPORTANT**, meaning that the default values should **never** be used for anything other than local development work at best but ideally should never be used at all. See `here </packer/variables/variables.json.sample>`_ for an example JSON variables file.
