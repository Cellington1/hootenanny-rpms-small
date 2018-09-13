#!/bin/bash
set +euxo pipefail
HOOT_REPO="${HOOT_REPO:-$HOME/hootenanny}"

if [ ! -d $HOOT_REPO/.git ]; then
    echo 'Please checkout Hootenanny repository first.'
    exit 1
fi

pushd $HOOT_REPO
cp LocalConfig.pri.orig LocalConfig.pri


# TODO: Do we add `ccache` like in original `BuildArchive.sh`?
#echo "QMAKE_CXX=ccache g++" >> LocalConfig.pri

# Temporarily allow undefined variables to allow us to source `SetupEnv.sh`.
set +u
source SetupEnv.sh
set -u

source conf/database/DatabaseConfig.sh

# Start postgres
su-exec postgres pg_ctl -D /var/lib/pgsql/9.5/data -s start


#Generate configure script.
aclocal
autoconf
autoheader
automake --add-missing --copy

# Run configure, enable R&D, services, and PostgreSQL.
./configure --quiet --with-rnd --with-services 

# --with-services
# Update the license headers.
./scripts/copyright/UpdateAllCopyrightHeaders.sh

echo "Start Fortify"

echo "Clean the compiled job"
/opt/hp_fortify_sca/bin/sourceanalyzer -b hootenanny_2018_4_27 -clean


# echo "Compile hootenanny"
# /opt/hp_fortify_sca/bin/sourceanalyzer -b hootenanny_2018_4_26a  -logfile comp.log make -j$(nproc)

# Setup dummy files
mkdir -p tmp/release
touch tmp/release/HootSwig
touch tmp/release/HootRnd
touch tmp/release/HootHadoop
touch tmp/release/HootCoreTest
touch tmp/release/HootCmd
touch tmp/release/HootCore
touch tmp/release/HootTest
touch tmp/release/HootJS


echo "Compile hootenanny"
/opt/hp_fortify_sca/bin/sourceanalyzer -b hootenanny_2018_4_27  make -j$(nproc)

# cat comp.log

echo "Scan hootenanny"
# Perform the scan
/opt/hp_fortify_sca/bin/sourceanalyzer -b hootenanny_2018_4_27 -64 -Xmx24G -scan -f Hootenanny_Core_2018_4_27.fpr

# cat scan.log
# Make the archive.
#make -j$(nproc) clean
#make -j$(nproc) archive

# Move the second maven run here, to see if we can get past the cache issue
#make -j$(nproc) archive

# Copy in source archive to RPM sources.

#e#cho "Current location"
pwd
# Copy fpr to mounted volume
cp /root/hootenanny/Hootenanny_Core_2018_4_27.fpr /mnt
cp -v hootenanny-[0-9]*.tar.gz /rpmbuild/SOURCES 
ls -la
pwd
ls -la /root/SOURCES && ls -la /root && ls -la /rpmbuild
popd

