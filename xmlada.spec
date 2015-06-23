Name:           xmlada
Version:        2015
Release:        1%{?dist}
Summary:        XML library for Ada
Group:          System Environment/Libraries
License:        GPLv2+
URL:            http://libre.adacore.com
## Direct download link is unavailable
## http://libre.adacore.com/libre/download/
Source0:        xmlada-gpl-%{version}-src.tar.gz 
## Fedora-specific
Patch1:         %{name}-%{version}-disable_static.patch
BuildRequires:  chrpath gprbuild
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

%prep
%setup -q -n xmlada-gpl-%{version}-src
%patch1 -p1 

%build
%configure --disable-rpath --enable-shared --disable-static
make LIBRARY_TYPE=relocatable GPROPTS="%{GNAT_optflags}" prefix=%{buildroot}/%{_prefix}


%install
rm -rf %{buildroot}
export GPRINSTALL_OPTS="--build-name=relocatable --lib-subdir=%{buildroot}/%{_libdir}/%{name} --link-lib-subdir=%{buildroot}/%{_libdir} --sources-subdir=%{buildroot}/%{_includedir}/%{name}"
make install LIBRARY_TYPE=relocatable  prefix=%{buildroot}/%{_prefix} GPROPTS="${GPRINSTALL_OPTS}" PSUB="share/gpr"
## Revoke exec permissions
find %{buildroot} -name '*.gpr' -exec chmod -x {} \;
find %{buildroot}%{_docdir} -type f -exec chmod -x {} \;
## Delete old bash script (not needed now)
rm -f %{buildroot}%{_bindir}/xmlada-config
## delete rpath manually (#674793)
chrpath --delete %{buildroot}%{_libdir}/%{name}/libxmlada*
install -d -m 0755 %{buildroot}/%{_libdir}/%{name}/static/
## There is not GNAT programming studio in Fedora
## To enable GPS plugin delete this string and create subpackage
rm -f %{buildroot}/%{_datadir}/gps/plug-ins/%{name}_gps.py*
rm -f %{buildroot}/%{_libdir}/%{name}/static/*
## only-non-binary-in-usr-lib
cd %{buildroot}/%{_libdir} && ln -s %{name}/lib%{name}*.so.* .

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
%dir %{_includedir}/%{name}
%{_GNAT_project_dir}/%{name}*.gpr
%{_includedir}/%{name}/*.adb
%{_includedir}/%{name}/*.ads
%{_libdir}/%{name}/*.ali
%{_libdir}/%{name}/lib%{name}*.so
%{_libdir}/lib%{name}*.so
%{_GNAT_project_dir}/manifests



%changelog
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
