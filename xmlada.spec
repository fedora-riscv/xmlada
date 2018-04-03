Name:           xmlada
Version:        2017
Release:        6%{?dist}
Summary:        XML library for Ada
Group:          System Environment/Libraries
License:        GPLv3+
URL:            http://libre.adacore.com
## Direct download link is unavailable
## http://libre.adacore.com/libre/download/
Source0:        xmlada-gpl-%{version}-src.tar.gz 
## Fedora-specific
Patch2:         %{name}-2016-gprinstall.patch

# Build on architectures where gprbuild is available
# on architectures without gprbuild provide source package only
# which is unpacked tarball for the purpose of bootstrapping of gprbuild
# bootstrap on ! %{GPRbuild_arches}
%ifarch %{GPRbuild_arches}
BuildRequires:  gprbuild
BuildRequires:  gcc-gnat
%endif

BuildRequires:  fedora-gnat-project-common >= 2 


%description
XML/Ada includes support for parsing XML files, including DTDs, 
full support for SAX, 
and an almost complete support for the core part of the DOM.
It includes support for validating XML files with XML schemas.

%ifarch %{GPRbuild_arches}
%package devel
Summary:        XML library for Ada devel package
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       fedora-gnat-project-common >= 2

%description devel
Xml library for ada devel package.


%package static
Summary:        XML library for Ada, static libraries
Group:          Development/Libraries
Requires:       %{name}-devel%{?_isa} = %{version}-%{release}

%description static
This package contains the XML/Ada libraries for static linking. It is needed
for linking GPRbuild statically so that GPRbuild will remain functional when
libraries are upgraded.

Other Fedora packages shall require xmlada-devel rather than xmlada-static if
possible.

%else

%global debug_package %{nil}

%package sources
Summary:        Source of XMLada for bootstrapping
Group:          Development/Libraries

%description sources
On architectures without gprbuild installs sources for gprbuild's bootstrap

%endif

%prep
%setup -q -n xmlada-gpl-%{version}-src
%patch2 -p1

%build
%ifarch %{GPRbuild_arches}
%configure --disable-rpath --enable-shared --disable-static --enable-build=distrib
make shared static GPROPTS="%{Gnatmake_optflags}" prefix=%{buildroot}/%{_prefix}
%else
%configure --enable-static --enable-build=distrib
%endif

%install
%ifarch %{GPRbuild_arches}
###export GPRINSTALL_OPTS="--build-name=relocatable --lib-subdir=%{buildroot}/%{_libdir}/%{name} --link-lib-subdir=%{buildroot}/%{_libdir} --sources-subdir=%{buildroot}/%{_includedir}/%{name}"
export GPRINSTALL_OPTS="--lib-subdir=%{buildroot}/%{_libdir} --link-lib-subdir=%{buildroot}/%{_libdir}"
## Install the shared libraries first and then the static ones, because
## apparently the variant that gprinstall sees first becomes the default in the
## project files.
make install-relocatable install-static prefix=%{buildroot}/%{_prefix} GPROPTS="${GPRINSTALL_OPTS}" PSUB="share/gpr"

## Revoke exec permissions
find %{buildroot} -name '*.gpr' -exec chmod -x {} \;
find %{buildroot}%{_docdir} -type f -exec chmod -x {} \;
## Delete old bash script (not needed now)
rm -f %{buildroot}%{_bindir}/xmlada-config
install -d -m 0755 %{buildroot}/%{_libdir}/%{name}/static/
## There is not GNAT programming studio in Fedora
## To enable GPS plugin delete this string and create subpackage
rm -f %{buildroot}/%{_datadir}/gps/plug-ins/%{name}_gps.py*
rm -f %{buildroot}/%{_libdir}/%{name}/static/*
## These Sphinx-generated files aren't needed in the package:
rm %{buildroot}%{_pkgdocdir}/{.buildinfo,objects.inv}

## Move a misplaced project file into place.
mv %{buildroot}%{_prefix}/lib/gnat/* %{buildroot}%{_GNAT_project_dir}/

## GPRinstall's manifest files are architecture-specific because they contain
## what seems to be checksums of architecture-specific files, so they must not
## be under _datadir. Their function is apparently undocumented, but my crystal
## ball tells me that they're used when GPRinstall uninstalls or upgrades
## packages. The manifest file is therefore irrelevant in this RPM package, so
## delete it.
rm -rf %{buildroot}%{_GNAT_project_dir}/manifests
%else
mkdir -p %{buildroot}/%{_includedir}/%{name}/sources
cp -r . %{buildroot}/%{_includedir}/%{name}/sources
find %{buildroot}/%{_includedir}/%{name}/sources -type f ! -name "*ad[sb]" ! -name "*gpr" -delete
find %{buildroot}/%{_includedir}/%{name}/sources -type d -empty -delete
%endif


%check
## Verify that there are no runpaths in the compiled libraries.
%{_rpmconfigdir}/check-rpaths


%files
%defattr(-,root,root,-)
%license COPYING*
%doc README.md TODO AUTHORS
%ifarch %{GPRbuild_arches}
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/static
%{_libdir}/lib%{name}_dom.so.*
%{_libdir}/lib%{name}_input_sources.so.*
%{_libdir}/lib%{name}_schema.so.*
%{_libdir}/lib%{name}_unicode.so.*
%{_libdir}/lib%{name}_sax.so.*
%{_libdir}/%{name}/lib%{name}*.so.*
%endif



%ifarch %{GPRbuild_arches}
%files devel
%defattr(-,root,root,-)
%{_includedir}/%{name}
%{_GNAT_project_dir}/%{name}*.gpr
%attr(444,-,-) %{_libdir}/%{name}/*.ali
%{_libdir}/%{name}/lib%{name}*.so
%{_libdir}/lib%{name}*.so
%{_pkgdocdir}/*.html
%{_pkgdocdir}/searchindex.js
%{_pkgdocdir}/_sources
%{_pkgdocdir}/_static
%{_pkgdocdir}/XMLAda.pdf


%files static
%{_libdir}/%{name}/*.a

%else
%files sources
%{_includedir}/%{name}
%endif

%changelog
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
