#!/usr/bin/env python

import argparse
import requests
import os
import re
import sys
import tarfile

LOOP = (
    'listener',
    'log_dest',
    'log_type',
    'auth_plugin',
)

LOOP_INLINE = (
    '',
)

NEEDS_QUOTE = (
    'persistent_client_expiration',
    'tls_version',
    'max_connections',
    'ciphers',
    )

DEFAULTS = {
    'acl_file': '"{{ mqtt_config_dir }}/acl',
    'auth_plugin': '[]',
    'auto_id_prefix': '""',
    'bind_address': '"{{ ansible_facts.default_ipv4_address }}"',
    'bridge_cafile': '""',
    'bridge_capath': '""',
    'bridge_certfile': '""',
    'bridge_identity': '""',
    'bridge_keyfile': '""',
    'bridge_psk': '""',
    'cafile': "''",
    'capath': "''",
    'certfile': "''",
    'client_id_prefixes': '""',
    'crlfile': "''",
    'http_dir': '"{{ mqtt_data_dir }}"',
    'include_dir': '"{{ mqtt_config_dir }}/conf.d"',
    'keyfile': "''",
    'listener': '[]',
    'local_client_id': '""',
    'log_dest': '\n  - file /var/log/mosquitto.log',
    'log_facility': 'daemon',
    'log_type': '\n  - error\n  - warning',
    'mount_point': "''",
    'notification_topic': '$SYS/broker/connection/<clientid>/state',
    'password_file': '"{{ mqtt_config_dir }}/passwd"',
    'persistence': 'true',
    'persistence_location': '"{{ mqtt_data_dir }}/"',
    'persistent_client_expiration': '1d',
    'pid_file': '/var/run/mosquitto.pid',
    'psk_file': "''",
    'psk_hint': 'Greetings from mosquitto',
    'remote_clientid': '""',
    'remote_password': '""',
    'remote_username': '""',
    'tls_version': '1.2',
}

DEFINED_BY_DEFAULT = (
    'user',
    'pid_file',
    'user',
    'port',
    'listener',
    'persistence',
    'persistence_file',
    'persistence_location',
    'log_dest',
    'log_type',
    'auth_plugin',
    'username_as_clientid',
    'include_dir',
)

parser = argparse.ArgumentParser(description='Generate a Jinja2 template from mosquitto config file')
parser.add_argument('--version', type=str, help='mosquitto version to fetch config for', default='1.5.5')
parser.add_argument('--prefix', type=str, help='prefix added to each variable', default='mqtt_')
parser.add_argument('--filename', type=str, help='file to extract', default='mosquitto.conf')

args = parser.parse_args()

# Get URL
os.chdir(os.path.abspath(os.path.dirname(sys.argv[0])))
filename = 'mosquitto-{version}.tar.gz'.format(version=args.version)
if os.path.isfile(filename):
    print('Files {filename} already exists. Skipping download'.format(filename=filename))
else:
    url = 'https://mosquitto.org/files/source/{filename}'.format(filename=filename)
    req = requests.get(url)

    if req.status_code != 200:
        sys.exit('Failed to download {0}'.format(filename))
    with open(filename, 'wb') as file:
        file.write(req.content)

# Unarchive config file from URL
with tarfile.open(filename, 'r') as tgz:
    members = tgz.getnames()
    conffile = 'mosquitto-{version}/{filename}'.format(version=args.version, filename=args.filename)
    tgz.extract(conffile, path='.')

# Parse config file
with open(conffile, 'r') as cf:
    lines = cf.readlines()
    # lines.sort()

output_dir = 'output-{version}'.format(version=args.version)
if not os.path.isdir(output_dir):
    os.mkdir(output_dir)


# Write out defaults/main.yml, table of vars for README, and a Jinja template file
param_re = re.compile('^#([\w-]+)\s?(.*?)(?: #.*)?$')
skip_re = re.compile('#(ffdc_output|max_log_entries|trace_level|trace_output)')
template_file = '{output_dir}/mosquitto.conf.j2'.format(output_dir=output_dir)
defaults_file = '{output_dir}/defaults_main.yml'.format(output_dir=output_dir)
readme_file = '{output_dir}/README.md'.format(output_dir=output_dir)

with open(template_file, 'w') as template, \
     open(readme_file, 'w') as readme, \
     open(defaults_file, 'w') as defaults:

    written_params = []
    table_line = '| `{prefix}{var_param}` | `{value}` |  |\n'
    default_line_quoted = "# {prefix}{var_param}: '{value}'\n"
    template_loop_end = '{% endfor %}\n'

    readme.write('# Mosquitto #\n\n'
                 '| Name              | Default Value       | Description          |\n'
                 '|-------------------|---------------------|----------------------|\n')

    template.write('# {{ ansible_managed }}\n')

    for line in lines:

        default_line = '# {prefix}{var_param}: {value}\n'
        default_line_bool = '{prefix}{var_param}: {value}\n'
        template_conditional = '{{% if {prefix}{var_param} is defined %}}\n'
        template_loop_start = ''
        template_line = '{orig_param} {{{{ {prefix}{var_param} }}}}\n'
        template_line_bool = '{var_param} {{{{ {prefix}{var_param} | string | lower }}}}\n'

        if skip_re.match(line):
            continue

        param_match = param_re.match(line)
        if param_match:
            # Keep the original parameter name and make a copy with underscores
            # instead of dashes
            orig_param = param_match.groups()[0]
            var_param = param_match.groups()[0].replace('-', '_')

            # Only process the option once even if it occurs multiples times in the example config
            if orig_param not in written_params:
                written_params.append(orig_param)

                # Put in my own default values rather than what is found in the example config
                if orig_param in DEFAULTS.keys():
                    value = DEFAULTS[orig_param]
                else:
                    value = param_match.groups()[1]

                # Parameters that I want to pass in as a list and generate one line per item
                if orig_param in LOOP:
                    var_param = '{0}s'.format(var_param)
                    value = '[]'
                    if orig_param in DEFAULTS.keys():
                        value = DEFAULTS[orig_param]
                    template_conditional = ''
                    template_loop_start = '{{% for item in {prefix}{var_param} %}}\n'
                    template_line = '{orig_param} {{{{ item }}}}\n'

                # If there isn't a default value on the line, assume it's a boolean value and default to 'false'
                # unless it has a default value specified in DEFAULTS
                elif not param_match.groups()[1] and orig_param not in DEFAULTS.keys():
                    #template_conditional = '{{% if {prefix}{var_param} %}}\n'
                    template_line = template_line_bool
                    value = 'false'

                if 'true' in value or 'false' in value:
                    template_line = template_line_bool

                # Quote the line if it contains values that are problematic for YAML
                if orig_param in NEEDS_QUOTE:
                    default_line = default_line_quoted

                # Remove the '# ' if this value is defined by default
                if orig_param in DEFINED_BY_DEFAULT:
                    default_line = default_line[2:]

                # Write out the template, defaults/main.yml, and README files
                if template_conditional:
                    template.write(template_conditional.format(prefix=args.prefix, var_param=var_param))
                if template_loop_start:
                    template.write(template_loop_start.format(prefix=args.prefix, var_param=var_param))
                template.write(template_line.format(prefix=args.prefix, orig_param=orig_param, var_param=var_param))

                # Scrub trailing spaces on variables that are multi-line lists
                if value != '[]' and orig_param in LOOP or orig_param in LOOP_INLINE:
                    default_line = default_line.replace(': ', ':')

                defaults.write(default_line.format(prefix=args.prefix, var_param=var_param, value=value))

                # Translate multi-line YAML into single line YAML for the README
                if value != '[]' and orig_param in LOOP or orig_param in LOOP_INLINE:
                    value = re.sub(r'^\n\s+-\s', '', value)
                    value = re.sub(r'\n\s+-\s', ', ', value)
                    value = '[{line}]'.format(line=value)
                table_formatted_line = table_line.format(prefix=args.prefix, var_param=var_param, value=value).replace('"', '')
                readme.write(table_formatted_line)
                if template_loop_start:
                    template.write(template_loop_end)
                if template_conditional:
                    template.write('{% endif %}\n')
