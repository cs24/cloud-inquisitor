****************
Cloud Inquisitor
****************

.. image:: docs/images/cloud-inquisitor_logo.png

============
Introduction
============

Cloud Inquisitor improves the security posture of an AWS footprint through:

* monitoring AWS objects for ownership attribution, notifying account owners of unowned objects, and subsequently removing unowned AWS objects if ownership is not resolved.
* detecting `domain hijacking <https://labs.detectify.com/2014/10/21/hostile-subdomain-takeover-using-herokugithubdesk-more/>`_.
* verifying security services such as `Cloudtrail <https://aws.amazon.com/cloudtrail/>`_ and `VPC Flowlogs <https://docs.aws.amazon.com/AmazonVPC/latest/UserGuide/flow-logs.html>`_.
* managing `IAM policies <https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies.html>`_ across multiple accounts.

`Cloud Inquisitor Latest <../../releases/latest>`_

============
Architecture
============

Typically Cloud Inquisitor runs in a "Security" or "Audit" account with cross-account access through the use of `AssumeRole <https://docs.aws.amazon.com/STS/latest/APIReference/API_AssumeRole.html>`_.

=========
Platforms
=========

Cloud Inquisitor works on Python 3.5 or higher and Ubuntu 16.04. 

* Production deployment is done through Packer.
* Development supports deployment via Docker or Packer.

Please see the `Resources`_ section below for further information.

=======
Contact
=======

Any questions or comments regarding this project can be made via the project's `Slack Chat Room <https://cloud-inquisitor.slack.com>`_.

=========
Resources
=========

This project has a **docs** directory that contains many resources that will help you implement Cloud Inquisitor and contribute to the project.

* `Quickstart <docs/quickstart.rst>`_
* `Upgrading <docs/upgrade.rst>`_
* `Development Build <docs/develop.rst>`_
* `Changelog <docs/changelog.rst>`_
* `Source Code <https://www.github.com/riotgames/cloud-inquisitor>`_
* `Contribution Guidelines <docs/contributing.rst>`_
* `Contributors <docs/contributors.rst>`_
* `Roadmap <../../milestones>`_
* `Issue Tracker <../../issues>`_
* `Slack Chat Room <https://cloud-inquisitor.slack.com>`_
