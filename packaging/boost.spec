Name:    boost
Summary: The Boost C++ Libraries
Version: 1.51.0
Release: 6
License: BSL-1.0
URL:     http://www.boost.org/
Group:   System/Libraries
Source:  boost-1.51.0.tar.gz

Obsoletes: boost-doc <= 1.30.2
Obsoletes: boost-python <= 1.30.2
Provides:  boost-doc = %{version}-%{release}

# boost is an "umbrella" package that pulls in all other boost components
Requires: boost-chrono = %{version}-%{release}
Requires: boost-program-options = %{version}-%{release}
Requires: boost-thread = %{version}-%{release}
Requires: boost-test = %{version}-%{release}
Requires: boost-filesystem = %{version}-%{release}
Requires: boost-system = %{version}-%{release}
Requires: boost-date-time = %{version}-%{release}
Requires: boost-regex = %{version}-%{release}
Requires: boost-serialization = %{version}-%{release}
Requires: boost-iostreams = %{version}-%{release}
Requires: boost-random = %{version}-%{release}

BuildRequires: libstdc++-devel
BuildRequires: bzip2-libs
BuildRequires: bzip2-devel
BuildRequires: zlib-devel
BuildRequires: python-devel
BuildRequires: libicu-devel
BuildRequires: chrpath

%bcond_with tests
%bcond_with docs_generated

%description
Boost provides free peer-reviewed portable C++ source libraries.  The
emphasis is on libraries which work well with the C++ Standard
Library, in the hopes of establishing "existing practice" for
extensions and providing reference implementations so that the Boost
libraries are suitable for eventual standardization. (Some of the
libraries have already been proposed for inclusion in the C++
Standards Committee's upcoming C++ Standard Library Technical Report.)

%package chrono
Summary: Run-Time component of boost chrono library
Group: System Environment/Libraries
Provides: libboost_chrono.so.%{version}

%description chrono
Run-Time support for Boost.Chrono, a set of useful time utilities.

%package program-options
Summary:  Runtime component of boost program_options library
Group: System/Libraries
Provides: libboost_program_options.so.%{version}

%description program-options
Runtime support of boost program options library, which allows program
developers to obtain (name, value) pairs from the user, via
conventional methods such as command line and config file.

%package thread
Summary: Runtime component of boost thread library
Group: System/Libraries
Provides: libboost_thread.so.%{version}

%description thread
Runtime component Boost.Thread library, which provides classes and
functions for managing multiple threads of execution, and for
synchronizing data between the threads or providing separate copies of
data specific to individual threads.

%package system
Summary:  Runtime component of boost system library
Group: System/Libraries
Provides: libboost_system.so.%{version}

%description system
Runtime component Boost. System library, which provides simple, light-weight
error_code objects that encapsulate system-specific error code values,
yet also provide access to more abstract and portable error conditions via
error_condition objects.

%package filesystem
Summary:  Runtime component of boost filesystem library
Group: System/Libraries
Provides: libboost_filesystem.so.%{version}

%description filesystem
Runtime component Boost. FileSystem library, which provides facilities
to manipulate files and directories, and the paths that identify them.

%package date-time
Summary:  A set of date-time libraries based on generic programming concepts.
Group: System/Libraries
Provides: libboost_date_time.so.%{version}

%description date-time
The motivation for this library comes from working with and helping build several date-time libraries on several projects.
Date-time libraries provide fundamental infrastructure for most development projects.

%package regex
Summary: Runtime component of boost system library
Group: System/Libraries
Provides: libboost_regex.so.%{version}
Requires: libicu

%description regex
Runtime support for boost regular expression library.

%package serialization
Summary: Runtime component of boost serialization library
Group: System/Libraries
Provides: libboost_serialization.so.%{version}

%description serialization
Runtime support for serialization for persistence and marshalling.

%package iostreams
Summary: Runtime component of boost IOStreams library
Group: System/Libraries
Provides: libboost_iostreams.so.%{version}

%description iostreams
Runtime support for boost IOStreams library

%package random
Summary: Runtime component of boost random library
Group: System/Libraries
Provides: libboost_random.so.%{version}

%description random
Runtime support for boost random library

%package devel
Summary: The Boost C++ headers and shared development libraries
Group: Development/Libraries
Requires: boost = %{version}-%{release}
Provides: boost-devel = %{version}-%{release}

%description devel
Headers and shared object symlinks for the Boost C++ libraries.

%package static
Summary: The Boost C++ static development libraries
Group: Development/Libraries
Requires: boost-devel = %{version}-%{release}
Obsoletes: boost-devel-static < 1.34.1-14
Provides: boost-devel-static = %{version}-%{release}

%description static
Static Boost C++ libraries.

%package test
Summary:  Runtime component of boost program_options library
Group: System/Libraries
Provides: libboost_test.so.%{version}

%description test
Boost Test

%package doc
Summary: The Boost C++ html docs
Group: Documentation
Provides: boost-python-docs = %{version}-%{release}

%description doc
HTML documentation files for Boost C++ libraries.

%prep
%setup -q

%build
BOOST_ROOT=`pwd`
export BOOST_ROOT

BOOST_LIBS="program_options,thread,system,filesystem,date_time,regex,serialization,iostreams,random,test"
REGEX_FLAGS="--with-icu"

# build make tools, ie bjam, necessary for building libs, docs, and testing
#(cd tools/jam/src && ./build.sh)
./bootstrap.sh --with-libraries=$BOOST_LIBS $REGEX_FLAGS --prefix=$RPM_BUILD_ROOT/usr --with-toolset=gcc
#BJAM=`find . -name bjam -a -type f`
#./b2

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr
mkdir -p $RPM_BUILD_ROOT%{_libdir}
mkdir -p $RPM_BUILD_ROOT%{_includedir}
mkdir -p $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

mkdir -p %{buildroot}/%{_datadir}/license
cp -rf %{_builddir}/%{name}-%{version}/packaging/%{name} %{buildroot}/%{_datadir}/license

# LICENSE
mkdir -p %{buildroot}/usr/share/license
cp -af packaging/boost %{buildroot}/usr/share/license/%{name}

./b2 install

# install lib
#for i in `find stage -type f -name \*.a`; do
#  NAME=`basename $i`;
#  install -p -m 0644 $i $RPM_BUILD_ROOT%{_libdir}/$NAME;
#done;
#for i in `find stage \( -type f -o -type l \) -name \*.so*`; do
#  NAME=`basename $i`;
#  install -p -m 0644 $i $RPM_BUILD_ROOT%{_libdir}/$NAME;
#  strip $RPM_BUILD_ROOT%{_libdir}/$NAME;
#done;

# install include files
#find %{name} -type d | while read a; do
#  mkdir -p $RPM_BUILD_ROOT%{_includedir}/$a
#  find $a -mindepth 1 -maxdepth 1 -type f \
#  | xargs -r install -m 644 -p -t $RPM_BUILD_ROOT%{_includedir}/$a
#done

# install doc files
DOCPATH=$RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/
find libs doc more -type f \( -name \*.htm -o -name \*.html \) \
    | sed -n '/\//{s,/[^/]*$,,;p}' \
    | sort -u > tmp-doc-directories
sed "s:^:$DOCPATH:" tmp-doc-directories | xargs -r mkdir -p
cat tmp-doc-directories | while read a; do
    find $a -mindepth 1 -maxdepth 1 -name \*.htm\* \
    | xargs install -m 644 -p -t $DOCPATH$a
done
rm tmp-doc-directories
install -p -m 644 -t $DOCPATH LICENSE_1_0.txt index.htm

# install pkgconfig file
mkdir -p $RPM_BUILD_ROOT%{_libdir}/pkgconfig
install -D -m 644 packaging/boost.pc $RPM_BUILD_ROOT%{_libdir}/pkgconfig

# remove scripts used to generate include files
find $RPM_BUILD_ROOT%{_includedir}/ \( -name '*.pl' -o -name '*.sh' \) -exec rm {} \;

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post chrono -p /sbin/ldconfig
%postun chrono -p /sbin/ldconfig

%post program-options -p /sbin/ldconfig
%postun program-options -p /sbin/ldconfig

%post thread -p /sbin/ldconfig
%postun thread -p /sbin/ldconfig

%post system -p /sbin/ldconfig
%postun system -p /sbin/ldconfig

%post filesystem -p /sbin/ldconfig
%postun filesystem -p /sbin/ldconfig

%post date-time -p /sbin/ldconfig
%postun date-time -p /sbin/ldconfig

%post regex -p /sbin/ldconfig
%postun regex -p /sbin/ldconfig

%post serialization -p /sbin/ldconfig
%postun serialization -p /sbin/ldconfig

%post iostreams -p /sbin/ldconfig
%postun iostreams -p /sbin/ldconfig

%post random -p /sbin/ldconfig
%postun random -p /sbin/ldconfig

%post doc -p /sbin/ldconfig
%postun doc -p /sbin/ldconfig

%post devel -p /sbin/ldconfig
%postun devel -p /sbin/ldconfig

%post static -p /sbin/ldconfig
%postun static -p /sbin/ldconfig

%post test -p /sbin/ldconfig
%postun test -p /sbin/ldconfig

%files
%manifest boost.manifest
%{_datadir}/license/%{name}

%files chrono
%manifest boost.manifest
%defattr(-, root, root, -)
%{_libdir}/libboost_chrono*.so.%{version}

%files program-options
%manifest boost.manifest
%defattr(-, root, root, -)
%{_libdir}/libboost_program_options*.so.%{version}

%files thread
%manifest boost.manifest
%defattr(-, root, root, -)
%{_libdir}/libboost_thread*.so.%{version}

%files system
%manifest boost.manifest
%defattr(-, root, root, -)
%{_libdir}/libboost_system*.so.%{version}

%files filesystem
%manifest boost.manifest
%defattr(-, root, root, -)
%{_libdir}/libboost_filesystem*.so.%{version}

%files date-time
%manifest boost.manifest
%defattr(-, root, root, -)
%{_libdir}/libboost_date_time*.so.%{version}

%files regex
%manifest boost.manifest
%defattr(-, root, root, -)
%{_libdir}/libboost_regex*.so.%{version}

%files serialization
%manifest boost.manifest
%defattr(-, root, root, -)
%{_libdir}/libboost_serialization*.so.%{version}
%{_libdir}/libboost_wserialization*.so.%{version}

%files iostreams
%manifest boost.manifest
%defattr(-, root, root, -)
%{_libdir}/libboost_iostreams*.so.%{version}

%files random
%manifest boost.manifest
%defattr(-, root, root, -)
%{_libdir}/libboost_random*.so.%{version}

%files doc
%manifest boost.manifest
%defattr(-, root, root, -)
%doc %{_docdir}/%{name}-%{version}

%files devel
%defattr(-, root, root, -)
%{_includedir}/boost
%{_libdir}/*.so
%{_libdir}/pkgconfig/boost.pc

%files static
%manifest boost.manifest
%defattr(-, root, root, -)
%{_libdir}/*.a

%files test
%manifest boost.manifest
%defattr(-, root, root, -)
%{_libdir}/libboost_unit_test_framework*.so.%{version}
%{_libdir}/libboost_prg_exec_monitor*.so.%{version}
