Name:		hootenanny
Version:	0.2.20_277_gd3bbfc9_dirty
Release:	1%{?dist}
Summary:	Hootenanny is a vector conflation suite.

Group:		Applications/Engineering
License:	GPLv3
URL:		https://github.com/ngageoint/hootenanny

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	git doxygen wget w3m words automake gcc zip unzip
Source0:        %{name}-%{version}.tar.gz

%description
Hootenanny was developed to provide an open source, standards-based approach to
geospatial vector data conflation. Hootenanny is designed to facilitate
automated and semi-automated conflation of critical foundation GEOINT features
in the topographic domain, namely roads (polylines), buildings (polygons), and
points-of-interest (POI's) (points). Conflation happens at the dataset level,
where the user's workflow determines the best reference dataset and source
content, geometry and attributes, to transfer to the output map.

%package core
Summary:	Hootenanny Core
Requires:       %{name}-core-deps
Group:		Applications/Engineering

%description core
Hootenanny was developed to provide an open source, standards-based approach to
geospatial vector data conflation. Hootenanny is designed to facilitate
automated and semi-automated conflation of critical foundation GEOINT features
in the topographic domain, namely roads (polylines), buildings (polygons), and
points-of-interest (POI's) (points). Conflation happens at the dataset level,
where the user's workflow determines the best reference dataset and source
content, geometry and attributes, to transfer to the output map.

This package contains the core algorithms and command line interface.

%prep
%setup -q -n %{name}-%{version}

%build
source ./SetupEnv.sh
./configure --with-rnd -q \
	--prefix=$RPM_BUILD_ROOT/usr/ \
	--datarootdir=$RPM_BUILD_ROOT/usr/share/hootenanny/ \
        --docdir=$RPM_BUILD_ROOT/usr/share/doc/hootenanny/ \
	--localstatedir=$RPM_BUILD_ROOT/var/lib/hootenanny/ \
	--sysconfdir=$RPM_BUILD_ROOT/etc/

echo Remove this stuff
cp ~/hootenanny/conf/*.rf ~/hootenanny/conf/words1.sqlite conf/

# Use ccache if it is available
cp LocalConfig.pri.orig LocalConfig.pri
command -v ccache >/dev/null 2>&1 && echo "QMAKE_CXX=ccache g++" >> LocalConfig.pri

make -s %{?_smp_mflags}

%install

./configure --with-rnd -q \
	--prefix=$RPM_BUILD_ROOT/usr/ \
	--datarootdir=$RPM_BUILD_ROOT/usr/share/hootenanny/ \
        --docdir=$RPM_BUILD_ROOT/usr/share/doc/hootenanny/ \
	--localstatedir=$RPM_BUILD_ROOT/var/lib/hootenanny/ \
	--sysconfdir=$RPM_BUILD_ROOT/etc/

make install

%check
source ./SetupEnv.sh
HootTest --slow

%clean
rm -rf %{buildroot}

%files core
%{_includedir}/hoot
%{_libdir}/*
%docdir /usr/share/docs/hootenanny/*
%config /var/lib/hootenanny/conf/hoot.json
%config /var/lib/hootenanny/conf/DatabaseConfig.sh


%package core-devel-deps
Summary:	Development dependencies for Hootenanny Core
Group:		Development/Libraries
Requires:	%{name}-core-deps = %{version}-%{release}
Requires:	autoconf automake boost-devel cppunit-devel gcc-c++
Requires:       gdal-devel >= 1.10.1
Requires:       gdb
Requires:       geos-devel = 3.4.2
Requires:       git glpk-devel libicu-devel nodejs-devel opencv-devel
Requires:       postgresql91-devel proj-devel protobuf-devel python-argparse python-devel qt-devel v8-devel
# Needed to build the documentation
Requires:       texlive-collection-langcyrillic

%description core-devel-deps
Hootenanny was developed to provide an open source, standards-based approach to
geospatial vector data conflation. Hootenanny is designed to facilitate
automated and semi-automated conflation of critical foundation GEOINT features
in the topographic domain, namely roads (polylines), buildings (polygons), and
points-of-interest (POI's) (points). Conflation happens at the dataset level,
where the user's workflow determines the best reference dataset and source
content, geometry and attributes, to transfer to the output map.

This packages contains the dependencies to build and develop the Hootenanny
core. Use this if you want to build from github.

%files core-devel-deps

%package core-deps
Summary:	Dependencies for Hootenanny Core
Group:		Development/Libraries
Requires:	asciidoc cppunit dblatex doxygen FileGDB_API
Requires:       gdal >= 1.10.1
Requires: 	gdal-esri-epsg >= 1.10.1
Requires:       geos = 3.4.2, gnuplot, graphviz
# Needed by gnuplot for report generation
Requires:       liberation-fonts-common liberation-sans-fonts
Requires:       libxslt nodejs opencv postgresql91-libs protobuf qt
Requires:       texlive
Requires:       unzip w3m wget words
Requires:       zip

%description core-deps
Hootenanny was developed to provide an open source, standards-based approach to
geospatial vector data conflation. Hootenanny is designed to facilitate
automated and semi-automated conflation of critical foundation GEOINT features
in the topographic domain, namely roads (polylines), buildings (polygons), and
points-of-interest (POI's) (points). Conflation happens at the dataset level,
where the user's workflow determines the best reference dataset and source
content, geometry and attributes, to transfer to the output map.

This packages contains the dependencies to run the Hootenanny core.

%files core-deps

%changelog
* Thu Jan 21 2016 Jason R. Surratt <jason.surratt@digitalglobe.com> - 0.2.21+
- Initial attempt
