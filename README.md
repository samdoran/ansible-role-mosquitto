Mosquitto
=========
[![Galaxy](https://img.shields.io/badge/galaxy-samdoran.mosquitto-blue.svg?style=flat)](https://galaxy.ansible.com/samdoran/mosquitto)
[![Build Status](https://travis-ci.com/samdoran/ansible-role-mosquitto.svg?branch=master)](https://travis-ci.com/samdoran/ansible-role-mosquitto)

Install [Eclipse Mosquitto](https://mosquitto.org/), a lightweight [MQTT](https://en.wikipedia.org/wiki/MQTT) broker.

Requirements
------------

Docker if running in a container.

Role Variables
--------------

| Name              | Default Value       | Description          |
|-------------------|---------------------|----------------------|
| `mqtt_installation_method` | `native` | How to install the service, either `native` or `container`. |
| `mqtt_directories` | `[see defaults/main.yml]` | Paths for config, data, and logs |
| `mqtt_config_files` | `[see defaults/main.yml]` |  |
| `mqtt_touch_files` | `[see defaults/main.yml]` |  |
| `mqtt_include_dir` | `{{ mqtt_config_dir }}/conf.d` |  |
| `mqtt_accounts` | `[]` | List of accounts and their hash generated with `mosquitto_passwd` that will have access to the broker. |
| `mqtt_container_name` | `mqtt` | Name of the running container. |
| `mqtt_image_name` | `eclipse-mosquitte` | Name of the image to pull. |
| `mqtt_container_network_mode` | `host` | Container networking mode. |
| `mqtt_container_restart_policy` | `always` | Conatainer restart policy. Setting to `always` ensures the container will start when the Docker daemon launches. |
| `mqtt_container_data_path` | `/mosquitto` | Path inside running container where config will be available. |
| `mqtt_container_state` | `started` | State of the container. |
| `mqtt_container_published_ports` | `[see defaults/main.yml]` | Ports to publish from the container. |
| `mqtt_container_volumes` | `[see defaults/main.yml]` | Volumes to mount into the running container |
| `mqtt_sys_interval` | `10` |  |
| `mqtt_store_clean_interval` | `10` |  |
| `mqtt_pid_file` | `/var/run/mosquitto.pid` |  |
| `mqtt_user` | `mosquitto` |  |
| `mqtt_max_inflight_messages` | `20` |  |
| `mqtt_max_inflight_bytes` | `0` |  |
| `mqtt_max_queued_messages` | `100` |  |
| `mqtt_max_queued_bytes` | `0` |  |
| `mqtt_queue_qos0_messages` | `false` |  |
| `mqtt_message_size_limit` | `0` |  |
| `mqtt_allow_zero_length_clientid` | `true` |  |
| `mqtt_auto_id_prefix` | `` |  |
| `mqtt_persistent_client_expiration` | `1d` |  |
| `mqtt_allow_duplicate_messages` | `false` |  |
| `mqtt_upgrade_outgoing_qos` | `false` |  |
| `mqtt_set_tcp_nodelay` | `false` |  |
| `mqtt_per_listener_settings` | `false` |  |
| `mqtt_bind_address` | `{{ ansible_facts.default_ipv4_address }}` |  |
| `mqtt_port` | `1883` |  |
| `mqtt_max_connections` | `-1` |  |
| `mqtt_protocol` | `mqtt` |  |
| `mqtt_http_dir` | `{{ mqtt_data_dir }}` |  |
| `mqtt_use_username_as_clientid` | `false` |  |
| `mqtt_cafile` | `''` |  |
| `mqtt_capath` | `''` |  |
| `mqtt_certfile` | `''` |  |
| `mqtt_keyfile` | `''` |  |
| `mqtt_tls_version` | `1.2` |  |
| `mqtt_require_certificate` | `false` |  |
| `mqtt_use_identity_as_username` | `false` |  |
| `mqtt_use_subject_as_username` | `false` |  |
| `mqtt_crlfile` | `''` |  |
| `mqtt_ciphers` | `DEFAULT:!aNULL:!eNULL:!LOW:!EXPORT:!SSLv2:@STRENGTH` |  |
| `mqtt_psk_hint` | `Greetings from mosquitto` |  |
| `mqtt_listeners` | `[]` |  |
| `mqtt_mount_point` | `''` |  |
| `mqtt_autosave_interval` | `1800` |  |
| `mqtt_autosave_on_changes` | `false` |  |
| `mqtt_persistence` | `false` |  |
| `mqtt_persistence_file` | `mosquitto.db` |  |
| `mqtt_persistence_location` | `{{ mqtt_data_dir }}/` |  |
| `mqtt_log_dests` | `[file /var/log/mosquitto.log]` |  |
| `mqtt_log_facility` | `daemon` |  |
| `mqtt_log_types` | `[error, warning]` |  |
| `mqtt_websockets_log_level` | `0` |  |
| `mqtt_connection_messages` | `true` |  |
| `mqtt_log_timestamp` | `true` |  |
| `mqtt_clientid_prefixes` | `false` |  |
| `mqtt_allow_anonymous` | `true` |  |
| `mqtt_password_file` | `{{ mqtt_config_dir }}/passwd` |  |
| `mqtt_psk_file` | `''` |  |
| `mqtt_acl_file` | `{{ mqtt_config_dir }}/acl` |  |
| `mqtt_auth_plugins` | `[]` |  |
| `mqtt_connection` | `<name>` |  |
| `mqtt_address` | `<host>[:<port>] [<host>[:<port>]]` |  |
| `mqtt_topic` | `<topic> [[[out | in | both] qos-level] local-prefix remote-prefix]` |  |
| `mqtt_bridge_protocol_version` | `mqttv311` |  |
| `mqtt_bridge_attempt_unsubscribe` | `true` |  |
| `mqtt_round_robin` | `false` |  |
| `mqtt_remote_clientid` | `` |  |
| `mqtt_local_clientid` | `false` |  |
| `mqtt_cleansession` | `false` |  |
| `mqtt_notifications` | `true` |  |
| `mqtt_notification_topic` | `$SYS/broker/connection/<clientid>/state` |  |
| `mqtt_keepalive_interval` | `60` |  |
| `mqtt_start_type` | `automatic` |  |
| `mqtt_restart_timeout` | `30` |  |
| `mqtt_idle_timeout` | `60` |  |
| `mqtt_threshold` | `10` |  |
| `mqtt_try_private` | `true` |  |
| `mqtt_remote_username` | `` |  |
| `mqtt_remote_password` | `` |  |
| `mqtt_bridge_cafile` | `` |  |
| `mqtt_bridge_capath` | `` |  |
| `mqtt_bridge_certfile` | `` |  |
| `mqtt_bridge_keyfile` | `` |  |
| `mqtt_bridge_insecure` | `false` |  |
| `mqtt_bridge_identity` | `` |  |
| `mqtt_bridge_psk` | `` |  |


Dependencies
------------

- samdoran.docker (only if running in a container)

Example Playbook
----------------

    - hosts: all
      roles:
         - samdoran.mosquitto

License
-------

Apache 2.0
