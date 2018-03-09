#!/bin/bash
set -euxo pipefail

## Get variables.
set +u
GIT_COMMIT="${1:-develop}"
set -u
source "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"/Vars.sh

# The container used to build Hootenanny archive.
BUILD_IMAGE=${BUILD_IMAGE:-hootenanny/rpmbuild-hoot-release}

echo "pea soup"

run_hoot_build_image \
    -i $BUILD_IMAGE -s rw \
    /bin/sh -c "su-exec postgres pg_ctl -D /var/lib/pgsql/9.5/data -s start &> /dev/null && /rpmbuild/scripts/hoot-checkout.sh ${GIT_COMMIT} && /rpmbuild/scripts/hoot-archive.sh"
