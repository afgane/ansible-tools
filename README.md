[![Build Status](https://travis-ci.org/galaxyproject/ansible-galaxy-tools.svg?branch=master)](https://travis-ci.org/galaxyproject/ansible-galaxy-tools)

This Ansible role is for automated provisioning of Galaxy instances. It can:

* install tools from a Tool Shed into Galaxy.
* install workflows into Galaxy, based on `.ga` files.
* run [data manager tools](https://galaxyproject.org/admin/tools/data-managers/)

This role will install and use [ephemeris](https://github.com/galaxyproject/ephemeris) into a virtual environment.

Variables
---------

## Required variables ##

- `galaxy_tools_api_key`: the Galaxy API key to use. Can either be the API key for an existing user, or a [bootstrapping key](https://docs.galaxyproject.org/en/release_23.2/admin/config.html#bootstrap-admin-api-key) (one that can be used for installing tools and for creating a temporary bootstrap user).
- `galaxy_tools_create_bootstrap_user`: (default: `false`) whether to
  create a bootstrap Galaxy admin user. If `true`, installation of workflows, and datamanagers will use the API key for the newly created user.

### Workflows and Data Managers

Note that while *tools* must be installed using a boostrapping key, installing *workflows* and running *datamanagers* require the API key for a real user. Therefore, if you want to install datamanagers or workflows, you must either:

- set `galaxy_tools_create_bootstrap_user` to `true`
- set `galaxy_tools_create_bootstrap_user` to `false` and set `galaxy_tools_api_key` to the API key for a real admin user (not a bootrapping key).

### Data Managers

In addition to the above, running datamanagers requires two more steps:

- the email address for the admin user must be configured. If you set `galaxy_tools_create_bootstrap_user` to `true`, the email address will be automatically configured. If you set it to `false`, you must set `galaxy_tools_admin_user_email` yourself.
- the user whose API key will be used must be configured to be an admin user by adding their email in your `galaxy.yml`. If you are using `galaxy_tools_create_bootstrap_user`, this means the value of `galaxy_tools_bootstrap_user_username` must be added to `galaxy.yml`.

## Control flow variables ##
The following variables can be set to either `true` or `false` to indicate if the
given part of the role should be executed:

 - `galaxy_tools_install_tools`: (default: `true`) whether to run the
   tools installation script
 - `galaxy_tools_install_datamanagers`: (default: `false`) whether to run the
   workflow installation script
 - `galaxy_tools_install_workflows`: (default: `false`) whether to run the
   workflow installation script
 - `galaxy_tools_delete_bootstrap_user`: (default: `false`) whether to
   delete the created bootstrap Galaxy admin user after other tasks are completed. See `galaxy_tools_create_bootstrap_user` above.

## Optional variables

If you want to install tools, workflows, or run datamanagers, you have to specify their source using the following variables:

- `galaxy_tools_tool_list_files`: String or list of String of paths to YAML tool list files.
- `galaxy_tools_workflows`: String or list of String of paths to `.ga` workflow files.
- `galaxy_tools_data_managers`: String or list of String of paths to YAML datamanager files.

The filenames set in these variables will be looked up by Ansible in the Ansible file paths.

See the `molecule/_testfiles` directory for examples of each of these files.

See `defaults/main.yml` for the available variables and their defaults.

### Restarting Galaxy with a handler

You can optionally set a handler that restarts Galaxy, that will be called after new tools or data managers have been installed/run. You need to define the handler yourself, and set the `galaxy_tools_restart_handler` variable to the handler's task name. For example:

```
roles:
  - role: galaxy-tools
    vars:
      ...
      galaxy_tools_restart_handler: restart-galaxy

handlers:
  - name: Restart-Galaxy
    command: /path/to/galaxy/run.sh --pid-file=/path/to/pid --stop-daemon
```

...but of course you can also use e.g. `supervisorctl` or `systemd` to restart Galaxy.