yamlfred
========

The `Alfred Workflows <http://support.alfredapp.com/workflows>`_ management tool
with a "divide and rule" manner.

Alfred Workflows contains README and scripts in its info.plist,
hard to keep the "divide and rule" strategy.

yamlfred manage these files separately and translate an info.plist
into a simplified workflow.yml, with a "divide and rule" manner.
In addition, yamlfred has abilities to extract or create Alfred workflow,
translate a workflow.yml into an info.plist and vice a versa.

Installation
------------

To install yamlfred, use pip install::

  $ pip install git+https://github.com/uchida/yamlfred

For the case of uninstall, use pip uninstall yamlfred::

  $ pip uninstall yamlfred

Usage
-----

- Extract existing Alfred workflow::

     $ yamlfred extract <workflow>.alfredworkflow

  Creates following <workflow> directory::

     <workflow>
     |-- ...
     |-- info.plist
     |-- ...

- convert info.plist (in current directory)
  into yaml template (workflow.yml) and scripts::

    $ yamlfred to_yaml

- convert yaml template (workflow.yml) into info.plist::

    $ yamlfred to_plist

- create Alfred workflow (<workflow>.alfredworkflow)
  from workflow.yml, scripts and README::

    $ yamlfred create <workflow>

Examples
--------

These Alfred workflows uses yamlfred:

- `alfred-switch-vpn <https://github.com/uchida/alfred-switch-vpn>`_
- `alfred-switch-bluetooth <https://github.com/uchida/alfred-switch-bluetooth>`_
- `alfred-switch-audio <https://github.com/uchida/alfred-switch-audio>`_

On can upload github release page via CI services, such as `Circle CI <https://circleci.com/>`_
with `hub <https://github.com/github/hub/>`_ command and `GITHUB_TOKEN`
consult `circle.yml` in these repositories for detailed information.

