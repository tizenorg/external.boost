Name: boost
Summary: The Boost C++ Libraries
Version: 1.46.1
Release: 4
License: Boost
URL: http://www.boost.org/
Group: System/Libraries
Source: boost-1.46.1.tar.gz
Obsoletes: boost-doc <= 1.30.2
Obsoletes: boost-python <= 1.30.2
Provides: boost-doc = %{version}-%{release}

# boost is an "umbrella" package that pulls in all other boost components
Requires: boost-program-options = %{version}-%{release}
Requires: boost-thread = %{version}-%{release}
Requires: boost-test = %{version}-%{release}

BuildRequires: libstdc++-devel
BuildRequires: bzip2-libs
BuildRequires: bzip2-devel
BuildRequires: zlib-devel
BuildRequires: python-devel
BuildRequires: libicu-devel
BuildRequires: chrpath

%bcond_with tests
%bcond_with docs_generated
#%define sonamever 5

%description
Boost provides free peer-reviewed portable C++ source libraries.  The
emphasis is on libraries which work well with the C++ Standard
Library, in the hopes of establishing "existing practice" for
extensions and providing reference implementations so that the Boost
libraries are suitable for eventual standardization. (Some of the
libraries have already been proposed for inclusion in the C++
Standards Committee's upcoming C++ Standard Library Technical Report.)

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

%package devel
Summary: The Boost C++ headers and shared development libraries
Group: Development/Libraries
Requires: boost = %{version}-%{release}
Requires: boost-program-options = %{version}-%{release}
Requires: boost-thread = %{version}-%{release}
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
#%setup -q -n %{name}_1_46_1

#%patch0 -p0
#sed 's/_FEDORA_OPT_FLAGS/%{optflags}/' %{PATCH1} | %{__patch} -p0 --fuzz=0
#%patch2 -p0
#sed 's/_FEDORA_SONAME/%{sonamever}/' %{PATCH3} | %{__patch} -p0 --fuzz=0
#%patch4 -p0
#%patch5 -p0
#%patch6 -p0
#%patch7 -p0

%build
BOOST_ROOT=`pwd`
export BOOST_ROOT

BOOST_LIBS="program_options,thread,test"

# build make tools, ie bjam, necessary for building libs, docs, and testing
#(cd tools/jam/src && ./build.sh)
./bootstrap.sh --with-libraries=$BOOST_LIBS
BJAM=`find . -name bjam -a -type f`
./bjam

#CONFIGURE_FLAGS="--with-toolset=gcc"
#PYTHON_VERSION=$(python -c 'import sys; print sys.version[:3]')
#PYTHON_FLAGS="--with-python-root=/usr --with-python-version=$PYTHON_VERSION"
#REGEX_FLAGS="--with-icu"
#./bootstrap.sh $CONFIGURE_FLAGS $PYTHON_FLAGS $REGEX_FLAGS

#%ifarch %{arm}
#LONGDOUBLE="--disable-long-double"
#%else
#LONGDOUBLE=""
#%endif

#BUILD_VARIANTS="variant=release threading=single,multi debug-symbols=on"
#BUILD_FLAGS="-d2 --layout=system $BUILD_VARIANTS $LONGDOUBLE"
#$BJAM $BUILD_FLAGS %{?_smp_mflags} stage

# build docs, requires a network connection for docbook XSLT stylesheets
#%if %{with docs_generated}
#cd ./doc
#chmod +x ../tools/boostbook/setup_boostbook.sh
#../tools/boostbook/setup_boostbook.sh
#USER_CFG=$BOOST_ROOT/tools/build/v2/user-config.jam
#$BOOST_ROOT/$BJAM --v2 -sICU_PATH=/usr --user-config=$USER_CFG html
#cd ..
#%endif
#
#%check
#%if %{with tests}
#echo "<p>" `uname -a` "</p>" > status/regression_comment.html
#echo "" >> status/regression_comment.html
#echo "<p>" `g++ --version` "</p>" >> status/regression_comment.html
#echo "" >> status/regression_comment.html
#
#cd tools/regression/build
##$BOOST_ROOT/$BJAM
#cd ../test
##python ./test.py
#cd ../../..
#
#results1=status/cs-`uname`.html
#results2=status/cs-`uname`-links.html
#email=benjamin.kosnik@gmail.com
#if [ -f $results1 ] && [ -f $results2 ]; then
#  echo "sending results starting"
#  testdate=`date +%Y%m%d`
#  testarch=`uname -m`
#  results=boost-results-$testdate-$testarch.tar.bz2
#  tar -cvf boost-results-$testdate-$testarch.tar $results1 $results2
#  bzip2 -f boost-results-$testdate-$testarch.tar 
#  echo | mutt -s "$testdate boost regression $testarch" -a $results $email 
#  echo "sending results finished"
#else
#  echo "error sending results"
#fi
#%endif

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_libdir}
mkdir -p $RPM_BUILD_ROOT%{_includedir}
mkdir -p $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

# install lib
for i in `find stage -type f -name \*.a`; do
  NAME=`basename $i`;
  install -p -m 0644 $i $RPM_BUILD_ROOT%{_libdir}/$NAME;
done;
for i in `find stage \( -type f -o -type l \) -name \*.so*`; do
  NAME=`basename $i`;
  install -p -m 0644 $i $RPM_BUILD_ROOT%{_libdir}/$NAME;
#  SONAME=$i.%{sonamever};
#  VNAME=$i.%{version};
#  base=`basename $i`;
#  NAMEbase=$base;
#  SONAMEbase=$base.%{sonamever};
#  VNAMEbase=$base.%{version};
#  mv $i $VNAME;
#
#  # remove rpath
#  chrpath --delete $VNAME;
#
#  ln -s $VNAMEbase $SONAME;
#  ln -s $VNAMEbase $NAME;
#  install -p -m 755 $VNAME $RPM_BUILD_ROOT%{_libdir}/$VNAMEbase;
#
#  mv $SONAME $RPM_BUILD_ROOT%{_libdir}/$SONAMEbase;
#  mv $NAME $RPM_BUILD_ROOT%{_libdir}/$NAMEbase;
done;

# install include files
find %{name} -type d | while read a; do
  mkdir -p $RPM_BUILD_ROOT%{_includedir}/$a
  find $a -mindepth 1 -maxdepth 1 -type f \
  | xargs -r install -m 644 -p -t $RPM_BUILD_ROOT%{_includedir}/$a
done

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

# remove scripts used to generate include files
find $RPM_BUILD_ROOT%{_includedir}/ \( -name '*.pl' -o -name '*.sh' \) -exec rm {} \;

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%post program-options -p /sbin/ldconfig

%postun program-options -p /sbin/ldconfig


%post thread -p /sbin/ldconfig

%postun thread -p /sbin/ldconfig


%post doc -p /sbin/ldconfig

%postun doc -p /sbin/ldconfig


%post devel -p /sbin/ldconfig

%postun devel -p /sbin/ldconfig


%post static -p /sbin/ldconfig

%postun static -p /sbin/ldconfig


%post test -p /sbin/ldconfig

%postun test -p /sbin/ldconfig


%files

%files program-options
%defattr(-, root, root, -)
%{_libdir}/libboost_program_options*.so.%{version}

%files thread
%defattr(-, root, root, -)
%{_libdir}/libboost_thread*.so.%{version}

%files doc
%defattr(-, root, root, -)
%doc %{_docdir}/%{name}-%{version}

%files devel
%defattr(-, root, root, -)
%{_includedir}/boost
%{_libdir}/*.so

%files static
%defattr(-, root, root, -)
%{_libdir}/*.a

%files test
%defattr(-, root, root, -)
%{_libdir}/libboost_unit_test_framework*.so.%{version}
%{_libdir}/libboost_prg_exec_monitor*.so.%{version}
