**************************************
Quick Start Guide for Cloud Inquisitor
**************************************

This tutorial will walk you through installing and configuring ``Cloud Inquisitor``. The tool currently runs on *Amazon Web Services* (AWS) but it has been designed to be platform-independent.

This tutorial assumes you are familiar with AWS & that you have an `AWS`_ account. You'll need to retrieve your ``Access Key ID`` and ``Secret Access Key`` from the web-based console.

.. _`AWS`: https://aws.amazon.com/

===========================
Installing Cloud Inquisitor
===========================

------------------
Build Requirements
------------------

* `Packer <https://packer.io/downloads.html>`_ > v0.12.3

    * AWS Credentials - API Keys or an AWS instance role with `appropriate permissions <https://www.packer.io/docs/builders/amazon.html>`_.

* `VirtualBox <https://www.virtualbox.org/>`_ - (for local development)

    * Vagrant > 1.9.0 for local development
    * A base Ubuntu image with SSH login *vagrant/vagrant*.

------------------
Building an Image
------------------

All the files required for building images can be found in the `packer </packer>`_ folder. There are three folders (`files </packer/files>`_, `scripts </packer/scripts>`_, and `variables </packer/variables>`_) and the main packer build script (`build.json </packer/build.json>`_).

------------------
Files Directory
------------------
::

    files/
    ├── backend-settings.py
    ├── nginx-nossl.conf
    ├── nginx-ssl.conf
    └── supervisor.conf

* `backend-settings.py </packer/files/backend-settings.py>`_ - template for the backend application configuration.

    * Install location: ``BACKEND_INSTALL_BASE/settings/production.py``

* `nginx-nossl.conf </packer/files/nginx-nossl.conf>`_ - the configuration files used for nginx, if SSL has not been enabled.

    * Install location: ``/etc/nginx/sites-available/cloudinquisitor.conf``

* `nginx-ssl.conf </packer/files/nginx-ssl.conf>`_ - the configuration files used for nginx, if SSL has been enabled.

    * Install location: ``/etc/nginx/sites-available/cloudinquisitor.conf``

* `supervisor.conf` - template for supervisor configuration

    * Install location: ``/etc/supervisor/conf.d/cloudinquisitor.conf``

-----------------
Scripts Directory
-----------------
::

    scripts/
    └── install.sh

* `install.sh </packer/scripts/install.sh>`_ - the main build script, which performs the actual installation.

-------------------
Variables Directory
-------------------

This folder contains an example of the JSON file required to pass in variables for the installer script. Variables in Packer can either be loaded from a file like the `variables.json.sample </packer/variables/variables.json.sample>`_ or they can be passed in through the command line when running packer or a mix between file and command line arguments. Any arguments passed in through the command line will override both the variables file passed in as well as default values in the main packer build script.
::

    variables/
    └── variables.json.sample

----------
build.json
----------

This is the main build definition for Packer which is where we define what and how to build.

-----------------
Building an Image
-----------------

Once you have all the variables set up in the file you're passing in, you just need to run the following command to build a new version of Cloud Inquisitor (either AMI or OVA).::

    bash packer build -only <builder> -var-file variables/production-variables.json build.json

See `build.json </packer/build.json>`_ for build target names such as *ami*, *local*, or  *ami-with-tests*

**Please note** that If you do not supply the `-only` argument, all builders will be used. 

--------------------
Overriding Variables
--------------------

You can override configuration variables from the command line. The order of ``-var`` parameters is important: the last takes priority. For example, if you want to override the database password while building an Amazon AMI you would run the following command: ::

    bash packer build -only ami -var-file variables/production.json -var 'db_password=verysecretpassword' build.json

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
