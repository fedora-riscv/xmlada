Name:           xmlada
Version:        4.1
Release:        3%{?dist}
Summary:        XML library for Ada
Group:          System Environment/Libraries
License:        GPLv2+
URL:            http://libre.adacore.com
## Direct download link is unavailable
## http://libre.adacore.com/libre/download/
Source0:        xmlada-gpl-%{version}-src.tgz
## Patch for use relocatable libs instead static 
## and add DESTDIR option for make install
Patch0:         %{name}-%{version}-destdir.patch
## Fedora-specific
Patch1:         %{name}-gpr.patch
Patch2:         %{name}-%{version}-gnatflags.patch
BuildRequires:  chrpath
BuildRequires:  gcc-gnat
BuildRequires:  fedora-gnat-project-common >= 2 

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
%setup -q -n xmlada-4.1-src
%patch0 -p1
%patch1 -p1 
%patch2 -p1 

%build
%configure --disable-rpath --enable-shared --disable-static
make %{?_smp_mflags}  GNATFLAGS="%{GNAT_optflags}" ADA_PROJECT_PATH=%_GNAT_project_dir


%install
rm -rf %{buildroot}
export BUILDS_SHARED=yes
make install DESTDIR=%{buildroot}  ADA_PROJECT_PATH=%_GNAT_project_dir BUILDS_SHARED=yes
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
%doc README TODO AUTHORS COPYING
%dir %{_libdir}/%{name}
%dir %{_docdir}/%{name}
%dir %{_libdir}/%{name}/relocatable
%dir %{_libdir}/%{name}/static
%{_libdir}/lib%{name}_dom.so.*
%{_libdir}/lib%{name}_input_sources.so.*
%{_libdir}/lib%{name}_schema.so.*
%{_libdir}/lib%{name}_unicode.so.*
%{_libdir}/lib%{name}_sax.so.*
%{_libdir}/%{name}/relocatable/lib%{name}*.so.*
%{_docdir}/%{name}/xml.html
%{_docdir}/%{name}/xml.info
%{_docdir}/%{name}/xml.pdf



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
