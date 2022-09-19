# Set this variable to %GPRbuild_arches for bootstrapping of
# gprbuild on new architecture or in case of new major version of
# the gcc-gnat package.
%global bootstrap_arch    no_bootstrapping
#global bootstrap_arch    %GPRbuild_arches

# Upstream source information.
%global upstream_owner    AdaCore
%global upstream_name     xmlada
%global upstream_version  22.0.0
%global upstream_gittag   v%{upstream_version}

Name:           xmlada
Epoch:          2
Version:        %{upstream_version}
Release:        1%{?dist}
Summary:        XML library for Ada

License:        GPL-3.0-or-later WITH GCC-exception-3.1 AND Unicode-DFS-2016
# XML/Ada itself is licensed under GPL v3 or later with a runtime exception. The
# Unicode license is mentioned as Unicode data files were used as an input for
# generating some of XML/Ada's source code.

URL:            https://github.com/%{upstream_owner}/%{upstream_name}
Source0:        %{url}/archive/%{upstream_gittag}/%{upstream_name}-%{upstream_version}.tar.gz

# [Fedora specific] Copy artifacts (docs, examples, etc.) to the correct location.
Patch:          %{name}-gprinstall-relocate-artifacts.patch

BuildRequires:  make
%ifnarch %{bootstrap_arch}
BuildRequires:  gprbuild > 2018-10
BuildRequires:  gcc-gnat
BuildRequires:  fedora-gnat-project-common
BuildRequires:  python3-sphinx
BuildRequires:  python3-sphinx-latex
BuildRequires:  latexmk
%endif

# Build only on architectures where GPRbuild is available.
ExclusiveArch:  %{GPRbuild_arches}


%description
XML/Ada includes support for parsing XML files, including DTDs, 
full support for SAX, 
and an almost complete support for the core part of the DOM.
It includes support for validating XML files with XML schemas.

%ifnarch %{bootstrap_arch}

%package devel
Summary:        XML library for Ada devel package
Requires:       %{name}%{?_isa} = %{epoch}:%{version}-%{release}
Requires:       fedora-gnat-project-common

%description devel
Xml library for ada devel package.


%package static
Summary:        XML library for Ada, static libraries
Requires:       %{name}-devel%{?_isa} = %{epoch}:%{version}-%{release}

%description static
This package contains the XML/Ada libraries for static linking. It is needed
for linking GPRbuild statically so that GPRbuild will remain functional when
libraries are upgraded.

Other Fedora packages shall require xmlada-devel rather than xmlada-static if
possible.

%else

# When bootstrapping gprbuild, only a package that contains source code is
# produced, so a debug package is not needed.
%global debug_package %{nil}

%package sources
Summary:        Source of XMLada for bootstrapping

%description sources
On architectures without gprbuild installs sources for gprbuild's bootstrap

%endif

%prep
%autosetup -p1

# Set version number.
sed --in-place --expression 's/18.0w/%{version}/' configure configure.in

%build
%ifnarch %{bootstrap_arch}
%configure --enable-build=distrib --enable-shared

# Build the libraries.
%{make_build} shared static GPROPTS='%{GPRbuild_flags}'

# Make the documentation.
make -C docs html latexpdf

%else
%{configure} --enable-build=distrib

%endif

%install
%ifnarch %{bootstrap_arch}

export GPRINSTALL_OPTS="--no-manifest \
       --ali-subdir=%{buildroot}%{_libdir} \
       --lib-subdir=%{buildroot}%{_libdir} \
       --link-lib-subdir=%{buildroot}%{_libdir}"

# Install the shared libraries first and then the static ones, because
# apparently the variant that gprinstall sees first becomes the default in the
# project files.
make install-relocatable install-static \
     prefix=%{buildroot}%{_prefix} GPROPTS="${GPRINSTALL_OPTS}"

## Revoke exec permissions
find %{buildroot} -name '*.gpr' -exec chmod -x {} \;
find %{buildroot}%{_docdir} -type f -exec chmod -x {} \;

install -d -m 0755 %{buildroot}/%{_libdir}/%{name}/static/
rm -f %{buildroot}/%{_libdir}/%{name}/static/*

%else

# Copy the source files.
mkdir --parents %{buildroot}%{_includedir}/%{name}/sources
cp -r . %{buildroot}%{_includedir}/%{name}/sources
find %{buildroot}%{_includedir}/%{name}/sources -type f ! -name "*ad[sb]" ! -name "*gpr" -delete
find %{buildroot}%{_includedir}/%{name}/sources -type d -empty -delete

%endif


%files
%license COPYING3 COPYING.RUNTIME
%doc README* TODO AUTHORS
%ifnarch %{bootstrap_arch}
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/static
%{_libdir}/lib%{name}_dom.so.*
%{_libdir}/lib%{name}_input_sources.so.*
%{_libdir}/lib%{name}_schema.so.*
%{_libdir}/lib%{name}_unicode.so.*
%{_libdir}/lib%{name}_sax.so.*
%{_libdir}/%{name}/lib%{name}*.so.*
%endif

%ifnarch %{bootstrap_arch}

%files devel
%{_includedir}/%{name}
%{_GNAT_project_dir}/%{name}*.gpr
%attr(444,-,-) %{_libdir}/%{name}/*.ali
%{_libdir}/%{name}/lib%{name}*.so
%{_libdir}/lib%{name}*.so
%dir %{_pkgdocdir}
%{_pkgdocdir}/html
%{_pkgdocdir}/pdf
%{_pkgdocdir}/examples
# Exclude Sphinx-generated files that aren't needed in the package.
%exclude %{_pkgdocdir}/html/.buildinfo
%exclude %{_pkgdocdir}/html/objects.inv

%files static
%{_libdir}/%{name}/*.a

%else

%files sources
%{_includedir}/%{name}

%endif

%changelog
* Sun Feb 12 2023 Dennis van Raaij <dvraaij@fedoraproject.org> - 2:22.0.0-1
- Updated to v22.0.0, using the archive available on GitHub.
- Changed the epoch to mark the new upstream version scheme.
- Changed the epoch to 2 instead of 1 for consistency with the GNATcoll packages.
- Updated the license, a runtime exception has now been added.
- Added new build dependencies to build the documentation with Sphinx and LaTeX.
- Examples are now located in _pkgdocdir/examples.
- License field now contains an SPDX license expression.
- Added the Unicode license to cover all code that has been generated using Unicode data.
- Removed some post-install steps that are no longer required.

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2020-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Jan 17 2023 Björn Persson <Bjorn@Rombobjörn.se> - 2020-9
- Rebuilt with GCC 13.

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2020-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2020-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sun Jan 16 2022 Björn Persson <Bjorn@Rombobjörn.se> - 2020-6
- Rebuilt with GCC 12 prerelease.

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2020-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jan 28 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2020-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Dec 21 2020 Pavel Zhukov <pavel@zhukoff.net> - 2020-3
- Rebuild. Ali files invalidated by gcc update

* Tue Dec  8 2020 Pavel Zhukov <pzhukov@redhat.com> - 2020-2
- Disable gprbuild's bootstraping

* Tue Dec  8 2020 Pavel Zhukov <pzhukov@redhat.com> - 2020-1
- New version v2020

* Mon Dec 07 2020 Jeff Law <releng@fedoraproject.org> - 2019-4
- Gcc 11 bootstrap

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2019-3
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2019-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Feb 3 2020 Björn Persson <Bjorn@Rombobjörn.se> - 2019-1
- Upgraded to the 2019 release.

* Mon Feb  3 2020 Pavel Zhukov <pzhukov@redhat.com> - 2018-11
- rebuild with new gprbuild

* Mon Feb  3 2020 Pavel Zhukov <pzhukov@redhat.com> - 2018-10
- Gcc 10 bootstrap

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2018-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2018-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb  9 2019 Pavel Zhukov <pzhukov@redhat.com> - 2018-7
- Rebuld with new gnat-rpm-macros
- Build with gprbuild 2018

* Tue Feb  5 2019 Pavel Zhukov <pzhukov@redhat.com> - 2018-4
- Rebuild with new gprbuild

* Tue Feb  5 2019 Pavel Zhukov <pzhukov@redhat.com> - 2018-2
- Produce source only package in bootstrap mode

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2017-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2017-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Apr  3 2018 Pavel Zhukov <pzhukov@redhat.com> - 2017-6
- Build source packages on non gprbuild enabled arches for bootstraping

* Tue Feb  6 2018 Pavel Zhukov <pzhukov@redhat.com> - 2017-5
- Rebuild with new gnat

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2017-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2017-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Jul 15 2017 Pavel Zhukov <pzhukov@redhat.com> - 2017-2
- rebuild with new gprbuild

* Fri Jul  7 2017 Pavel Zhukov <pzhukov@redhat.com> - 2017-1
- New version (2017)

* Wed Apr 20 2017 Pavel Zhukov <<landgraf@fedoraproject.org>> - 2016-5
- Rebuild to fix non x86 arches ali versions

* Fri Feb 17 2017 Björn Persson <Bjorn@Rombobjörn.se> - 2016-4
- Reverted the temporary workaround.

* Sun Feb 12 2017 Björn Persson <Bjorn@Rombobjörn.se> - 2016-3
- Made a temporary workaround to rebuild with GCC 7 prerelease.

* Sat Feb  4 2017 Pavel Zhukov <pavel@zhukoff.net> - 2016-1
- Rebuild with new gnat

* Mon Aug 08 2016 Björn Persson <Bjorn@Rombobjörn.se> - 2016-1
- Upgraded to the 2016 release.
- Removed the irrelevant and FHS-violating manifest file.
- The license has changed to GPLv3+.

* Sun May 01 2016 Björn Persson <Bjorn@Rombobjörn.se> - 2015-12
- Tagged the license file as such.

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2015-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sun Jan 31 2016 Björn Persson <Bjorn@Rombobjörn.se> - 2015-10
- Rebuilt with GCC 6 prerelease.

* Sat Dec 19 2015 Björn Persson <Bjorn@Rombobjörn.se> - 2015-8
- Added a -static subpackage for linking GPRbuild statically.

* Wed Jun 24 2015 Pavel Zhukov <<landgraf@fedoraproject.org>> - 2015-7
- Remove temporary links

* Wed Jun 24 2015 Pavel Zhukov <<landgraf@fedoraproject.org>> - 2015-6
- Move sources to separate directories
- Add temporary symlinks to allow gprbuiild bootstraping
- Fix temporary (upgrade) links pattern
- Provide previous version to upgrade gprbuild

* Tue Jun 23 2015 Pavel Zhukov <<landgraf@fedoraproject.org>> - 2015-2
- Install xmlada.gpr

* Wed Jun 17 2015 Pavel Zhukov <<landgraf@fedoraproject.org>> - 2015-1
- New release (#2015)

* Wed Apr 29 2015 Peter Robinson <pbrobinson@fedoraproject.org> 2013-11
- rebuild (gcc / gnat 5)

* Sun Mar 15 2015 Pavel Zhukov <landgraf@fedoraproject.org> - 2013-10
- Create unversioned symlinks
 
* Sat Feb 14 2015 Pavel Zhukov <landgraf@fedoraproject.org> - 2013-9
- Rebuild with new gcc 4.9

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2013-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2013-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 13 2014 Peter Robinson <pbrobinson@fedoraproject.org> 2013-6
- Use GNAT_arches rather than an explicit list

* Tue May 13 2014 Peter Robinson <pbrobinson@fedoraproject.org> 2013-5
- aarch64 now has Ada

* Sun Apr 20 2014 Pavel Zhukov <landgraf@fedoraproject.org> - 2013-4
- Rebuild for new gcc 

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2013-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jul 13 2013 Pavel ZHukov <landgraf@fedoraproject.org> - 2013-2
- New release
- AdaCore has moved to years in version.
- Fix gpr error

* Sat Mar 09 2013 Pavel Zhukov <landgraf@fedoraproject.org> - 4.3-5
- Aws failed to bind with xmlada

* Fri Jan 25 2013 Kevin Fenzi <kevin@scrye.com> 4.3-4
- Rebuild for new libgnat

* Fri Jan 25 2013 Pavel Zhukov <landgraf@fedoraproject.org> - 4.3-3
- Rebuild with GCC 4.8

* Tue Dec 18 2012 Pavel Zhukov <landgraf@fedoraproject.org> - 4.3-2
- Fix gpr patch

* Mon Dec 17 2012 Pavel Zhukov <landgraf@fedoraproject.org> - 4.3-1
- New release
