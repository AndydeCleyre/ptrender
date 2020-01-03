ptrender & vwrite
=================

Conveniences for rendering text files from pyratemp templates and json or yaml var files
----------------------------------------------------------------------------------------

See pyratemp__ for template syntax.

__ https://www.simple-is-better.org/template/pyratemp.html

ptrender
--------

::

<!--(for line in ptrender_help.splitlines())-->
    $! line !$
<!--(end)-->

vwrite
------

::

<!--(for line in vwrite_help.splitlines())-->
    $! line !$
<!--(end)-->

Installation
------------

.. code:: bash

    pip install ptrender

For yaml support:

.. code:: bash

    pip install 'ptrender[yaml]'
