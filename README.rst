###############
CloudInquisitor
###############
`CloudInquisitor Latest </releases/latest>`_

============
Introduction
============

CloudInquisitor improves the security posture of your AWS 
account through:

* monitoring the AWS objects for ownership attribution, notifying account owners of unowned objects and subsequently removing unowned AWS objects, if ownership is not resolved.
* detecting `domain hijacking <https://labs.detectify.com/2014/10/21/hostile-subdomain-takeover-using-herokugithubdesk-more/>`_.
* verification of services such as Cloudtrail and VPC Flowlogs being enabled with the capability to enable if disabled.
* management of IAM policies across multiple accounts.

============
Architecture
============

Typically CloudInquisitor runs in a "Security" or "Audit" 
account with cross-account access through the use of 
`AssumeRole <https://docs.aws.amazon.com/STS/latest/APIReference/API_AssumeRole.html>`_.

=========
Platforms
=========

CloudInquisitor works on Python 3.5 or higher and it has been 
known to work on Ubuntu 16.04. 

* Production deployment is done through Packer.
* Development-wise, you can either use Docker or Packer.

Please see the `Resources`_ section below for further information.

=======
Contact
=======

Any questions or comments regarding this project can be made 
via the project's `Slack Chat Room <https://cinq.slack.com>`_.

=========
Resources
=========

This project has a **docs** directory that contains many resources 
that will help you both implement CloudInquisitor and contribute 
to the project.

* `Quickstart <docs/quickstart.rst>`_
* `Upgrading <docs/upgrade.rst>`_
* `Development Build <docs/develop.rst>`_
* `Changelog <docs/changelog.rst>`_
* `Source Code <https://www.github.com/riotgames/CloudInquisitor>`_
* `Contribution Guidelines <docs/contributing.rst>`_
* `Contributors <docs/contributors.rst>`_
* `Roadmap <docs/roadmap.rst>`_
* `Issue Tracker <../../issues>`_
* `Slack Chat Room <https://cinq.slack.com>`_
