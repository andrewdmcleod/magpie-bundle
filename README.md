<!--
  Licensed to the Apache Software Foundation (ASF) under one or more
  contributor license agreements.  See the NOTICE file distributed with
  this work for additional information regarding copyright ownership.
  The ASF licenses this file to You under the Apache License, Version 2.0
  (the "License"); you may not use this file except in compliance with
  the License.  You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.
-->
## Overview

This bundle contains one charm: the Magpie charm. The purpose of this charm
is to test some fundamental networking - ICMP and DNS - on whichever
juju substrate / with whichever juju provider you choose.


## Deploying this bundle

This bundle deploys 2 physical machines and 2 lxc containers on each of
those machines.

    juju deploy magpie

Once the units form a peer relationship they will start testing ICMP
and DNS. To add more units:

    juju add-unit magpie -n 1
    juju add-unit magpie -n 2 --to lxc:1

This will add an additional magpie unit and 2 more lxc containers on 
machine 1.

[charm store]: https://jujucharms.com/
[juju-deployer]: https://pypi.python.org/pypi/juju-deployer/


## Status and Smoke Test

The services provide extended status reporting to indicate results:

    juju status --format=tabular

This is particularly useful when combined with `watch` to track the on-going
progress of the deployment:

    watch -n 0.5 juju status --format=tabular

More verbose information is sent to the juju logs, which can be watched:

    juju debug-log 


## Deploying in Network-Restricted Environments

Charms can be deployed in environments with limited network access. To deploy
in this environment, you will need a local mirror to serve required packages.


### Mirroring Packages

You can setup a local mirror for apt packages using squid-deb-proxy.
For instructions on configuring juju to use this, see the
[Juju Proxy Documentation](https://juju.ubuntu.com/docs/howto-proxies.html).


## Contact Information



## Resources

