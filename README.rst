yamlfred
========

Manage Alfred Workflow via yaml templates.
Convert Alfred workflow into yaml templates and vice a versa.

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

