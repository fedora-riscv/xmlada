Name:           xmlada
Version:        2013
Release:        10%{?dist}
Summary:        XML library for Ada
Group:          System Environment/Libraries
License:        GPLv2+
URL:            http://libre.adacore.com
## Direct download link is unavailable
## http://libre.adacore.com/libre/download/
Source0:        xmlada-gpl-2013-src.tgz 
#Source0:        xmlada-gpl-%{version}-src.tgz
## Fedora-specific
Patch2:         %{name}-%{version}-gpr.patch
Patch1:         %{name}-%{version}-gnatflags.patch
## Patch for use relocatable libs instead static 
## and add DESTDIR option for make install
Patch0:         %{name}-%{version}-destdir.patch
BuildRequires:  chrpath
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
%patch0 -p1
%patch1 -p1 
%patch2 -p1 

%build
%configure --disable-rpath --enable-shared --disable-static
make %{?_smp_mflags}  GNATFLAGS="%{GNAT_optflags}" ADA_PROJECT_PATH=%_GNAT_project_dir BUILDS_SHARED=yes 


%install
rm -rf %{buildroot}
export BUILDS_SHARED=yes
make install DESTDIR=%{buildroot}  ADA_PROJECT_PATH=%_GNAT_project_dir BUILDS_SHARED=yes  LIBDIR=%{_libdir}
## Revoke exec permissions
find %{buildroot} -name '*.gpr' -exec chmod -x {} \;
find %{buildroot}%{_docdir} -type f -exec chmod -x {} \;
## Delete old bash script (not needed now)
rm -f %{buildroot}%{_bindir}/xmlada-config
## delete rpath manually (#674793)
chrpath --delete %{buildroot}%{_libdir}/%{name}/relocatable/libxmlada*
install -d -m 0755 %{buildroot}/%{_libdir}/%{name}/static/
## There is not GNAT programming studio in Fedora
## To enable GPS plugin delete this string and create subpackage
rm -f %{buildroot}/%{_datadir}/gps/plug-ins/%{name}_gps.py*
rm -f %{buildroot}/%{_libdir}/%{name}/static/*
## only-non-binary-in-usr-lib

%files 
%defattr(-,root,root,-)
%doc README TODO AUTHORS COPYING*
%dir %{_libdir}/%{name}
%{_docdir}/%{name}
%dir %{_libdir}/%{name}/relocatable
%dir %{_libdir}/%{name}/static
%{_libdir}/lib%{name}_dom.so.*
%{_libdir}/lib%{name}_input_sources.so.*
%{_libdir}/lib%{name}_schema.so.*
%{_libdir}/lib%{name}_unicode.so.*
%{_libdir}/lib%{name}_sax.so.*
%{_libdir}/%{name}/relocatable/lib%{name}*.so.*



%files devel
%defattr(-,root,root,-)
%dir %{_includedir}/%{name}
%dir %{_GNAT_project_dir}/%{name}
%{_GNAT_project_dir}/%{name}.gpr
%{_GNAT_project_dir}/xmlada_shared.gpr
%{_GNAT_project_dir}/%{name}/xmlada_dom.lgpr
%{_GNAT_project_dir}/%{name}/xmlada_input_sources.lgpr
%{_GNAT_project_dir}/%{name}/xmlada_sax.lgpr
%{_GNAT_project_dir}/%{name}/xmlada_schema.lgpr
%{_GNAT_project_dir}/%{name}/xmlada_unicode.lgpr
%{_GNAT_project_dir}/%{name}_dom.gpr
%{_GNAT_project_dir}/%{name}_input.gpr
%{_GNAT_project_dir}/%{name}_sax.gpr
%{_GNAT_project_dir}/%{name}_schema.gpr
%{_GNAT_project_dir}/%{name}_unicode.gpr
%{_includedir}/%{name}/*.adb
%{_includedir}/%{name}/*.ads
%{_libdir}/%{name}/relocatable/*.ali
%{_libdir}/%{name}/relocatable/lib%{name}*.so



%changelog
* Wed Apr 29 2015 Peter Robinson <pbrobinson@fedoraproject.org> 2013-10
- rebuild (gcc / gnat 5)

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

* Tue Jan 10 2012 Pavel Zhukov <landgraf@fedoraproject.org> - 4.1-3
- Rebuild for new GCC-4.7

* Sat Jul 15 2011 Pavel Zhukov <landgraf@fedoraproject.org> - 4.1-2
- Update to new release GNAT-GPL-2011
- Fix permissions

* Wed Mar 30 2011 Pavel Zhukov <landgraf@fedoraproject.org> - 3.2.1-11
- Fix library type (add configure options)

* Tue Mar 01 2011 Pavel Zhukov <landgraf@fedoraproject.org> - 3.2.1-10
- fix path for fedora-gnat-project-common

* Tue Mar 01 2011 Pavel Zhukov <landgraf@fedoraproject.org> - 3.2.1-9
- use macros _GNAT_project_di
- fix hardcode includedir
- fix BuildRequires
- fix owned dir
- fix ?_isa

* Sun Feb 20 2011 Pavel Zhukov <landgraf@fedoraproject.com> - 3.2.1-8
- fix spec errors
- fix directories for rawhide
- fix gcc-4.6 issues
- fix libdir

* Fri Feb 11 2011 Pavel Zhukov <landgraf@fedoraproject.com> - 3.2.1-6
- move gpr to /usr/share/gpr(/xmlada)

* Mon Feb 7 2011 Pavel Zhukov <landgraf@fedoraproject.com> - 3.2.1-5
- move so to -devel package fix spec errors

* Sun Feb 6 2011 Pavel Zhukov <landgraf@fedoraproject.com> - 3.2.1-4
- fix dir owner

* Sat Feb 5 2011 Pavel Zhukov <landgraf@fedoraproject.com> - 3.2.1-3
- fix errors in Makefile
- fix files list 

* Fri Feb 4 2011 Pavel Zhukov <landgraf@fedoraproject.com> - 3.2.1-1
- Initial spec
