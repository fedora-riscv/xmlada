Name:           xmlada
Version:        2015
Release:        8%{?dist}
Summary:        XML library for Ada
Group:          System Environment/Libraries
License:        GPLv2+
URL:            http://libre.adacore.com
## Direct download link is unavailable
## http://libre.adacore.com/libre/download/
Source0:        xmlada-gpl-%{version}-src.tar.gz 
## Fedora-specific
Patch2:         %{name}-%{version}-gprinstall.patch
BuildRequires:  gprbuild
BuildRequires:  gcc-gnat
BuildRequires:  fedora-gnat-project-common >= 2 
# xmlada and gcc-gnat only available on these:
ExclusiveArch:  %{GNAT_arches}


%description
XML/Ada includes support for parsing XML files, including DTDs, 
full support for SAX, 
and an almost complete support for the core part of the DOM.
It includes support for validating XML files with XML schemas.

%package devel 
Summary:        XML library for Ada devel package
Group:          Development/Libraries
License:        GPLv2+
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


%prep
%setup -q -n xmlada-gpl-%{version}-src
%patch2 -p1 

%build
%configure --disable-rpath --enable-shared --enable-static --enable-build=distrib
make GPROPTS="%{Gnatmake_optflags}" prefix=%{buildroot}/%{_prefix}


%install
rm -rf %{buildroot}
###export GPRINSTALL_OPTS="--build-name=relocatable --lib-subdir=%{buildroot}/%{_libdir}/%{name} --link-lib-subdir=%{buildroot}/%{_libdir} --sources-subdir=%{buildroot}/%{_includedir}/%{name}"
export GPRINSTALL_OPTS="--lib-subdir=%{buildroot}/%{_libdir}/%{name} --link-lib-subdir=%{buildroot}/%{_libdir}"
## Install the shared libraries first and then the static ones, because
## apparently the variant that gprinstall sees first becomes the default in the
## project files.
OS=Windows_NT make install-relocatable install-static prefix=%{buildroot}/%{_prefix} GPROPTS="${GPRINSTALL_OPTS}" PSUB="share/gpr"
# Setting OS to "Windows_NT" circumvents a hardcoded "lib" in the makefile.
# This also skips the removal of write permission from the ALI files, so the
# files section compensates for that.

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
## only-non-binary-in-usr-lib
cd %{buildroot}/%{_libdir} && ln -s %{name}/lib%{name}*.so.* .


%check
## Verify that there are no runpaths in the compiled libraries.
%{_rpmconfigdir}/check-rpaths


%files 
%defattr(-,root,root,-)
%doc README TODO AUTHORS COPYING*
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/static
%{_libdir}/lib%{name}_dom.so.*
%{_libdir}/lib%{name}_input_sources.so.*
%{_libdir}/lib%{name}_schema.so.*
%{_libdir}/lib%{name}_unicode.so.*
%{_libdir}/lib%{name}_sax.so.*
%{_libdir}/%{name}/lib%{name}*.so.*



%files devel
%defattr(-,root,root,-)
%{_includedir}/%{name}
%{_GNAT_project_dir}/%{name}*.gpr
%attr(444,-,-) %{_libdir}/%{name}/*.ali
%{_libdir}/%{name}/lib%{name}*.so
%{_libdir}/lib%{name}*.so
%{_GNAT_project_dir}/manifests


%files static
%{_libdir}/%{name}/*.a


%changelog
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
