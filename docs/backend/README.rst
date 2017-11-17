***********************
CloudInquisitor Backend
***********************

This project provides two of the three pieces needed for the Cloud Inquisitor  system,
namely the API backend service and the scheduler process responsible for fetching and auditing
accounts. The code is built to be completely modular using ``pkg_resource`` entry points for
loading modules as needed. This allows you to easily build third-party modules without having to update
the original codebase.

==========
API Server
==========

The API server provides a RESTful interface for the `frontend <https://www.github.com/riotgames/inquisitor/frontend>`_.
web client.

==============
Authentication
==============

The backend service uses a JWT token based form of authentication, requiring the client to send an
Authorization HTTP header with each request. Currently the only supported method of federated
authentication is using the OneLogin based SAML workflow.

There is also the option to disable the SAML based authentication in which case no authentication is
required and all users of the system will have administrative privileges. This mode should only be
used for local development, however for testing SAML based authentication we have a OneLogin
application configured that will redirect to http://localhost based URL's and is the preferred method
for local development to ensure proper testing of the SAML code.

========
Auditors
========

Auditors are plugins which will alert and potentially take action based on data collected.

----------
Cloudtrail
----------

The CloudTail auditor will ensure that CloudTrail has been enabled for all accounts configured in the
Audits system. The system will automatically create a S3 bucket and SNS topics for log delivery notifications.
However, you must ensure that the proper access has been granted to the accounts attempting to log to a remote
S3 bucket. SNS subscriptions will need to be confirmed through an external tool such as the CloudTrail app.

^^^^^^^^^^^^^^^^^^^^^
Configuration Options
^^^^^^^^^^^^^^^^^^^^^

+---------------------------------------------+-------------------------------------------------------------+-------------------------------+----------+
| Option                                      | Description                                                 | Default Value                 | Required |
+=============================================+=============================================================+===============================+==========+
| ``AUDITOR_CLOUDTRAIL_ENABLED``              | Whether or not the auditor is run by the scheduler          | `True`                        | No       |
+---------------------------------------------+-------------------------------------------------------------+-------------------------------+----------+
| ``AUDITOR_CLOUDTRAIL_BUCKET_NAME``          | S3 bucket where CloudTrail log files should be delivered    | `None`                        | Yes      |
+---------------------------------------------+-------------------------------------------------------------+-------------------------------+----------+
| ``AUDITOR_CLOUDTRAIL_BUCKET_REGION``        | The region where to store the S3 bucket                     | `us-west-2`                   | No       |
+---------------------------------------------+-------------------------------------------------------------+-------------------------------+----------+
| ``AUDITOR_CLOUDTRAIL_BUCKET_ACCOUNT``       | AWS Account that owns the S3 bucket                         | `None`                        | Yes      |
+---------------------------------------------+-------------------------------------------------------------+-------------------------------+----------+
| ``AUDITOR_CLOUDTRAIL_GLOBAL_EVENTS_REGION`` | Region where global events (e.g. console logins) are logged | `us-west-2`                   | No       |
+---------------------------------------------+-------------------------------------------------------------+-------------------------------+----------+
| ``AUDITOR_CLOUDTRAIL_SNS_TOPIC_NAME``       | SNS Topic where log delivery notifications are sent.        | `cloudtrail-log-notification` | No       |
+---------------------------------------------+-------------------------------------------------------------+-------------------------------+----------+
| ``AUDITOR_CLOUDTRAIL_SQS_QUEUE``            | Queue for SNS notifications to be delivered to.             | `None`                        | Yes      |
+---------------------------------------------+-------------------------------------------------------------+-------------------------------+----------+

----------------
Domain Hijacking
----------------

The domain hijacking auditor will attempt to identify misconfigured DNS entries that would potentially
result in third parties being able to take over legitimate Riot owned DNS names and serve malicious
content to players from a real location.

This auditor will fetch information from AWS Route53, CloudFlare and our internal F5 based DNS servers,
and validate the records found against our known owned S3 buckets, Elastic BeanStalks and CloudFront CDN
distributions.

^^^^^^^^^^^^^^^^^^^^^
Configuration Options
^^^^^^^^^^^^^^^^^^^^^

+-----------------------------------+------------------------------------------------------------+--------------------------------------------------+----------+
| Option                            | Description                                                | Default Value                                    | Required |
+===================================+============================================================+==================================================+==========+
| ``AUDITOR_DOMAIN_HIJACK_ENABLED`` | Whether or not the auditor is run by the scheduler         | ``True``                                         | No       |
+-----------------------------------+------------------------------------------------------------+--------------------------------------------------+----------+
| ``EMAIL_METHOD``                  | Method to use when sending email alerts                    | ``ses``                                          | No       |
+-----------------------------------+------------------------------------------------------------+--------------------------------------------------+----------+
| ``EMAIL_FROM_ADDRESS``            | The address email alerts come from                         | ``None``                                         | Yes      |
+-----------------------------------+------------------------------------------------------------+--------------------------------------------------+----------+
| ``EMAIL_HIJACK_RECIPIENTS``       | Comma-separated list of addresses to recieve hijack alerts | ``None``                                         | Yes      |
+-----------------------------------+------------------------------------------------------------+--------------------------------------------------+----------+
| ``EMAIL_HIJACK_SUBJECT``          | Subject line for email alerts                              | ``Potential domain hijack possibility detected`` | No       |
+-----------------------------------+------------------------------------------------------------+--------------------------------------------------+----------+

---
IAM
---

The IAM roles and policy auditor will audit, and if enabled, manage the default Riot IAM policies and roles.

^^^^^^^^^^^^^^^^^^^^^
Configuration Options
^^^^^^^^^^^^^^^^^^^^^

+--------------------------------+---------------------------------------------------------------------------+--------------------------------+-----------------+
| Option                         | Description                                                               | Default Value                  | Required        |
+================================+===========================================================================+================================+=================+
| ``AUDITOR_IAM_ENABLED``        | Whether or not the auditor is run by the scheduler                        | ``True``                       | No              |
+--------------------------------+---------------------------------------------------------------------------+--------------------------------+-----------------+
| ``AUDITOR_IAM_MANAGE_ROLES``   | Set to ``True`` if you want roles and their linked policies to be managed | ``True``                       | No              |
+--------------------------------+---------------------------------------------------------------------------+--------------------------------+-----------------+
| ``AUDITOR_IAM_GIT_SERVER``     | Hostname of the Github server to clone policy repo from                   | ``github.com``                 | No              |
+--------------------------------+---------------------------------------------------------------------------+--------------------------------+-----------------+
| ``AUDITOR_IAM_GIT_REPO``       | Name of the Git repo to close                                             | ``riotgames/CloudInquisitor``  | No              |
+--------------------------------+---------------------------------------------------------------------------+--------------------------------+-----------------+
| ``AUDITOR_IAM_GIT_AUTH_TOKEN`` | Github auth token for API calls                                           | ``None``                       | Yes, if enabled |
+--------------------------------+---------------------------------------------------------------------------+--------------------------------+-----------------+

-------
Tagging
-------

Cloud Inquisitor audits EC2 instances for **tagging compliance** and shutdowns or terminates instances if they are not brought 
into compliance after a pre-defined amount of time.


**Note:** This is currently being extended to include all taggable AWS objects.


---------------
Action Schedule
---------------

+-----+--------+
| Age | Action |
+-----+--------+
| 0 days | Alert the AWS account owner via email. |
| 21 days | Alert the AWS account owner, warning that shutdown of instance(s) will happen in one week |
| 27 days | Alert the AWS account owner, warning shutdown of instance(s) will happen in one day |
| 28 days | Shutdown instance(s) and notify AWS account owner |
| 112 days | Terminate the instance and notify AWS account owner |
+-----+--------+

^^^^^^^^^^^^^^^^^^^^^
Configuration Options
^^^^^^^^^^^^^^^^^^^^^

+--------+-------------+---------------+----------+
| Option | Description | Default Value | Required |
+--------+-------------+---------------+----------+
| ``AUDITOR_TAGGING_ENABLED`` | Controls whether or not the auditor is run by the scheduler | ``True`` | No |
| ``EMAIL_FROM_ADDRESS`` | The address email alerts come from | ``None`` | Yes |
+--------+-------------+---------------+----------+

==========
Collectors
==========

Collectors are plugins which only job is to fetch information from the AWS API and update the local
database state.

---
EC2
---

Currently the only collector is the EC2 collector. This is responsible for fetching instance related
information such as instance type, state, tags and public IP address information.

^^^^^^^^^^^^^^^^^^^^^
Configuration Options
^^^^^^^^^^^^^^^^^^^^^

+--------+-------------+---------------+----------+
| Option | Description | Default Value | Required |
+========+=============+===============+==========+
| ``COLLECTOR_EC2_ENABLED`` | Controls whether or not the colletor is run by the scheduler | ``True`` | No |
+--------+-------------+---------------+----------+
| ``COLLECTOR_EC2_INTERVAL`` | Determines how often each account / region is polled for new data (in minutes) | ``15`` | No |
+--------+-------------+---------------+----------+
| ``COLLECTOR_EC2_MAX_INSTANCES`` | Maximum number of instances to fetch per AWS API call | ``1000`` | No |
+--------+-------------+---------------+----------+

========
Commands
========

Commands are ``flask-script`` additions for the ``manage.py`` script, which allows implementation of additional
CLI options.

--------
Accounts
--------

The accounts command allows updates to the AWS Accounts configured for the Audits system. The CLI allows
you to add, update and delete accounts from the system if for some reason the web frontend isn't working.

^^^^^^^^^^^^^^^^^^^^^
Add or Update Account
^^^^^^^^^^^^^^^^^^^^^

::

    python manage.py add_account [account_name] [account_number] [contact_email] <args>

**Arguments**

+--------+-------------+---------------+----------+
| Option | Description | Default Value | Required |
+--------+-------------+---------------+----------+
| ``account_name`` | Name of the AWS Account | ``None`` | Yes |
| ``account_number`` | The AWS Account number / ID | ``None`` | Yes |
| ``contact_email`` | Comma-separated list of email addresses which are responsible for the AWS account | ``None`` | Yes |
| ``--access-key` / `-a`` | AWS API Access Key | ``None`` | No |
| ``--secret-key` / `-s`` | AWS API Secret Key | ``None`` | No |
| ``--disabled` / `-d`` | Add the account, but do not enable data collection | ``False`` | No |
| ``--update`` | Update account if it already exists | ``False`` | No |
+--------+-------------+---------------+----------+

^^^^^^^^^^^^^^
Delete Account
^^^^^^^^^^^^^^

Removes an account from the system, will prompt for confirmation before account is deleted. When removed
all data associated with the account will also be deleted from the database and will not be able to be
regenerated without fetching it all from the AWS API.

::
    
    python manage.py delete_account [account_name]

**Arguments**

+--------+-------------+---------------+----------+
| Option | Description | Default Value | Required |
+--------+-------------+---------------+----------+
| ``account_name`` | Name of the AWS Account | ``None`` | Yes |
+--------+-------------+---------------+----------+

--------------
run_api_server
--------------

Starts a ``gunicorn`` based API server. This should be used instead of the default flask ``runserver``
command for any production workloads.

::

    python manage.py run_api_server <args>

^^^^^^^^^^^^^^^^^^^^^
Configuration Options
^^^^^^^^^^^^^^^^^^^^^

+--------+-------------+---------------+----------+
| Option | Description | Default Value | Required |
+--------+-------------+---------------+----------+
| ``API_HOST`` | IP Address to bind API server to | ``None`` | Yes |
| ``API_PORT`` | Port to bind API server to | ``None`` | Yes |
| ``API_WORKERS`` | Number of worker threads to spawn for API server | ``None`` | Yes |
| ``API_SSL`` | Enables SSL transport for API endpoint | ``None`` | Yes |
| ``API_SSL_KEY_PATH`` | Path to SSL private key | ``None`` | Yes, if `API_SSL` is `True`` |
| ``API_SSL_CERT_PATH`` | Path to SSL public key | ``None`` | Yes, if `API_SSL` is `True`` |
+--------+-------------+---------------+----------+

**Arguments**

In addition to the values from the configuration file, you can also override them using command
line arguments.

+--------+-------------+---------------+----------+
| Option | Description | Default Value | Required |
+--------+-------------+---------------+----------+
| ``--host` / `-H`` | IP Address to bind API server to | CFG: `API_HOST`` | Yes |
| ``--port` / `-p`` | Port to bind API server to | CFG: `API_PORT`` | Yes |
| ``--workers` / `-w`` | Number of worker threads to spawn for API server | CFG: `API_WORKERS`` | Yes |
+--------+-------------+---------------+----------+

-------------
run_scheduler
-------------

Executes the scheduler daemon. This is the main workhorse for gathering information and will execute
the enabled plugins on their pre-defined intervals.

::

    python manage.py run_scheduler <args>

^^^^^^^^^^^^^^^^^^^^^
Configuration Options
^^^^^^^^^^^^^^^^^^^^^

+--------+-------------+---------------+----------+
| Option | Description | Default Value | Required |
+--------+-------------+---------------+----------+
| ``SCHEDULER_WORKER_THREADS`` | Number of threads to spawn for the worker plugins | ``20`` | No |
| ``SCHEDULER_WORKER_INTERVAL`` | Interval between each worker thread being started | ``30`` (seconds) | No |
+--------+-------------+---------------+----------+

**Arguments**

In addition to the values from the configuration file, you can also override some of them using command
line arguments.

+--------+-------------+---------------+----------+
| Option | Description | Default Value | Required |
+--------+-------------+---------------+----------+
| ``--max-threads` / `-m`` | Number of threads to spawn for the worker plugins | CFG: ``SCHEDULER_WORKER_THREADS`` | No |
+--------+-------------+---------------+----------+

--------------
update_regions
--------------

Updates the local cache of EC2 regions from the AWS API. This command must be run the first time the
Audits system is installed on a machine, and should be run whenever there is a change to the available
regions from AWS.

::

    python manage.py update_regions

**Arguments**

If no secret or access key is provided on the CLI, the system will pick a random configured account
to use for this API call.

+--------+-------------+---------------+----------+
| Option | Description | Default Value | Required |
+========+=============+===============+==========+
| ``==access=key` / `=a`` | AWS API Access Key | ``None`` | No |
| ``--secret-key` / `-s`` | AWS API Secret Key | ``None`` | No |
+--------+-------------+---------------+----------+

----------------
domain_hijacking
----------------

This sub-module contains all the collection logic for the domain hijacking auditor. Due to the size
and complexity of the code, it was provided as a separate sub-module instead of inline for the auditor.

-----
views
-----

This module contains all the views (REST endpoints) for the Flask application. All endpoint URL's in the
sections below are prefixed with ``/api/v1``.

--------
\__init\__
--------

Contains the base view classes that all other views extend.

--------
Accounts
--------

AWS Account management, which is only accessible to administrative users.

**REST Endpoints**

* ``/account``

    * ``GET`` - Returns list of accounts
    * ``POST```` - Create new account (see list of arguments below)

        * ``account_name`` - Required
        * ``account_number`` - Required
        * ``contact_email`` - Required
        * ``enabled`` - Required (0 or 1)
        * ``required_groups`` - Optional, default ``[ ]``

* ``/account/<int:account_id>``

    * ``GET`` - Returns detailed information about a single account
    * ``PUT`` - Update account information

        * ``account_name`` - Required
        * ``account_number`` - Required
        * ``contact_email`` - Required
        * ``enabled`` - Required (0 or 1)
        * ``required_groups`` - Optional, default ``[ ]``

    * ``DELETE`` - Delete account from system
    
------
config
------

Most of the configuration for the application is stored in the database, and is exposed to admins only.

**REST Endpoints**

* ``/config``

    * ``GET`` - Return list of configuration keys
    * ``POST`` - Create a new configuration item

        * ``key`` - Key / Name for the config item. Required
        * ``type`` - Type of the item, must be one of ``string``, ``int``, ``float``, ``array``, ``json``, ``bool``. Required
        * ``value`` - Value of the configuration item. Required

* ``/config/<str:key>``

    * ``GET`` - Return information about a specific configuration item
    * ``PUT`` - Update configuration for specified key
        * ``type`` - Type of the item, must be one of ``string``, ``int``, ``float``, ``array``, ``json``, ``bool``
        * ``value`` - Value of the configuration item
    * ``DELETE`` - Remove the specified configuration item. **WARNING:** Deleting configuration
    items may cause the application to no longer start or load correctly.

----------------
domain_hijacking
----------------

Returns information about potentially hijacked sub-domains

**REST Endpoints**

* ``/domainhijacking``

    * ``GET`` - Returns list of all currently potentially compromised domains

^^^^^^^^^^^^^
ec2_instances
^^^^^^^^^^^^^

Returns information about EC2 Instances

**REST Endpoints**

* ``/ec2/instance/<string:instance_id>``

    * ``GET`` - Return detailed information about a specific instance

* ``/ec2/instance``

    * ``GET`` - Return list of instances based on the provided filters

        * ``count`` - Number of instances returned per request. Optional, default ``100``
        * ``page`` - Offset to use for request, to pagination results. Optional, default ``None``
        * ``account`` - Limit results to specific account by name. Optional, default ``None``
        * ``region`` - Limit results to specific AWS region. Optional, default ``None``
        * ``state`` - Limit results to a specific state. Optional, default ``None``. Valid options: ``None``, ``running``, ``stopped``

------
emails
------

See or re-send emails sent by the auditors.

**REST Endpoints**

* ``/emails``

    * ``GET`` - Return a list of emails 

        * ``page`` - Page offset to use. Optional, default ``1``
        * ``count`` - Number of items to return per page. Optional, default ``100``
        * ``subsystem`` - Limit request to only show emails for a specific subsystem. Optional, default ``None``

* ``/emails/<int:email_id>``

    * ``GET`` - Return content of a single email message
    * ``PUT`` - Re-send the email message

----
logs
----

Returns warning and error log information from the API server and scheduler processes. Only available
to administrative users.

**REST Endpoints**

* ``/logs``

    * ``GET`` - Get list of log entries based on filters

        * ``limit`` - Number of entires returned per request. Optional, default ``100``
        * ``page`` - Offset to use for request, to pagination results. Optional, default ``0``

* ``/logs/<int:log_event_id>``

    * ``GET`` - Return detailed information about specific log event, including full stack trace

--------
metadata
--------

Returns metadata used by frontend to control access to UI elements, as well as information about
AWS accounts and regions available to the user.

**REST Endpoints**

* ``/metadata``

    * ``GET`` - Returns metadata information.

-------
reports
-------

Returns information for reporting functionality such as Old EC2 Instances and tagging compliance

**REST Endpoints**

* ``/reports/required_tags``

    * ``GET`` - Returns information about EC2 instances which are non-compliant with tagging.

        * ``required_tags`` - List of required tags to filter by. Optional, default: ``[ 'Name', 'Owner', 'Accounting' ]``
        * ``count`` - Number of instances returned per request. Optional, default ``100``
        * ``page`` - Offset to use for request, to pagination results. Optional, default ``None``
        * ``account`` - Limit results to specific account by name. Optional, default ``None``
        * ``region`` - Limit results to specific AWS region. Optional, default ``None``
        * ``state`` - Limit results to a specific state. Optional, default ``None``. Valid options: ``None``, ``running``, ``stopped``

* ``/reports/old_instances``

    * ``GET`` - Returns information about EC2 instances older than the specified number of days

        * ``count`` - Number of instances returned per request. Optional, default ``100``
        * ``page`` - Offset to use for request, to pagination results. Optional, default ``None``
        * ``account`` - Limit results to specific account by name. Optional, default ``None``
        * ``region`` - Limit results to specific AWS region. Optional, default ``None``
        * ``age`` - Limit results to instances older than this value, in days. Optional, default ``730``
        * ``state`` - Limit results to a specific state. Optional, default ``None``. Valid options: ``None``, ``running``, ``stopped``

----
SAML
----

Handles all SAML based authentication for the application.

**REST Endpoints**

* ``/saml/login``

    * ``GET`` - Initiate SAML authentication workflow

* ``/saml/login/consumer``

    * ``POST`` - Process result from OneLogin SAML IdP and set JWT authentication token

* ``/saml/logout``

    * ``GET`` - Terminate OneLogin authenticated session

* ``/saml/logout/consumer``

    * ``GET`` - Process logout event from OneLogin SAML IdP

------
Search
------

Allows searching through all AWS accounts for specific EC2 Instance IDs or IP addresses

**REST Endpoints**

* ``/search/<string:keyword>``

    * ``GET`` - Return the results for the requested search keyword

-----
Stats
-----

Used to build the dashboard for the frontend user. Contains general statistics about the 
number of EC2 Instances and RFC-0026 compliance for all AWS accounts.

**REST Endpoints**

* ``/stats``

    * ``GET`` - Return statistical information
