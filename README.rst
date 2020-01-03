ptrender & vwrite
=================

Conveniences for rendering text files from pyratemp templates and json or yaml var files
----------------------------------------------------------------------------------------

See pyratemp__ for template syntax.

__ https://www.simple-is-better.org/template/pyratemp.html

ptrender
--------

::

    ptrender 0.0.3
    
    Use json or yaml var_files to render template_file to an adjacent
    file with the same name but the extension stripped
    
    Usage:
        ptrender [SWITCHES] template_file var_files...
    
    Meta-switches:
        -h, --help         Prints this help message and quits
        --help-all         Prints help messages of all sub-commands and quits
        -v, --version      Prints the program's version and quits
    
    Switches:
        -f, --force        Overwrite any existing destination file
    

vwrite
------

::

    vwrite 0.0.3
    
    Use json or yaml vars files to render each template file found recursively
    under the working folder, to an adjacent file with the same name but the
    extension stripped, overriding any vars in ./vars.json in the following
    order:
    
        <root_path>/vars.json,
        <root_path>/vars.yml,
        <root_path>/vars.yaml,
        <template.parent>/vars.json,
        <template.parent>/vars.yml,
        <template.parent>/vars.yaml
    
    Later entries override earlier ones.
    
    Usage:
        vwrite [SWITCHES] [root_path=<CWD>]
    
    Meta-switches:
        -h, --help                        Prints this help message and quits
        --help-all                        Prints help messages of all sub-commands and quits
        -v, --version                     Prints the program's version and quits
    
    Switches:
        -f, --force                       Overwrite any existing destination file
        -n, --vars-name VALUE:str         Filename (excluding extension) for each vars file; the default is vars
        -t, --template-ext VALUE:str      Filename extension for templates; the default is t
    

Installation
------------

.. code:: bash

    pip install ptrender

For yaml support:

.. code:: bash

    pip install 'ptrender[yaml]'
