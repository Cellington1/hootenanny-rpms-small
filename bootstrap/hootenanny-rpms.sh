#!/bin/bash
set -euo pipefail

sudo yum install -y git rpm-build
git clone -b el7-repo https://github.com/ngageoint/hootenanny-rpms.git
