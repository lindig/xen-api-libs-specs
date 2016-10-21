%global debug_package %{nil}

Name:           ocaml-xen-api-client
Version:        0.9.12
Release:        1%{?dist}
Summary:        XenServer XenAPI Client Library for OCaml
License:        LGPLv2
URL:            https://github.com/xapi-project/xen-api-client
Source0:        https://github.com/xapi-project/xen-api-client/archive/v%{version}/xen-api-client-%{version}.tar.gz
BuildRequires:  oasis
BuildRequires:  ocaml
BuildRequires:  ocaml-camlp4-devel
BuildRequires:  ocaml-cohttp-devel
BuildRequires:  ocaml-findlib
BuildRequires:  ocaml-lwt-devel
BuildRequires:  ocaml-ounit-devel
BuildRequires:  ocaml-rpc-devel
BuildRequires:  ocaml-uri-devel
BuildRequires:  ocaml-xmlm-devel
BuildRequires:  ocaml-cstruct-devel
BuildRequires:  ocaml-uuidm-devel
BuildRequires:  ocaml-xcp-rrd-devel

%description
XenAPI Client is an OCaml library implementing XenServer's XenAPI.
It is used for programmatically controlling a pool of XenServer
virtualization hosts.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}
Requires:       ocaml-xmlm-devel%{?_isa}
Requires:       ocaml-cohttp-devel%{?_isa}
Requires:       ocaml-rpc-devel%{?_isa}
Requires:       ocaml-lwt-devel%{?_isa}
Requires:       ocaml-uri-devel%{?_isa}
Requires:       ocaml-cstruct-devel%{?_isa}

%description    devel
XenAPI Client is an OCaml library implementing XenServer's XenAPI.
It is used for programmatically controlling a pool of XenServer
virtualization hosts.

%prep
%autosetup -n xen-api-client-%{version}

%build
make
make doc

%install
export OCAMLFIND_DESTDIR=%{buildroot}/%{_libdir}/ocaml
mkdir -p $OCAMLFIND_DESTDIR
make install


%files
%doc CHANGES
%doc README.md
%{_libdir}/ocaml/xen-api-client
%exclude %{_libdir}/ocaml/xen-api-client/*.a
%exclude %{_libdir}/ocaml/xen-api-client/*.cmxa
%exclude %{_libdir}/ocaml/xen-api-client/*.cmx
%exclude %{_libdir}/ocaml/xen-api-client/*.mli

%files devel
%{_libdir}/ocaml/xen-api-client/*.a
%{_libdir}/ocaml/xen-api-client/*.cmx
%{_libdir}/ocaml/xen-api-client/*.cmxa
%{_libdir}/ocaml/xen-api-client/*.mli

%changelog
* Mon Oct 17 2016 Euan Harris <euan.harris@citrix.com> - 0.9.12-1
- Update to 0.9.12

* Mon Jun 27 2016 Euan Harris <euan.harris@citrix.com> - 0.9.11-1
- Update to 0.9.11

* Thu Apr  2 2015 David Scott <dave.scott@citrix.com> - 0.9.8-1
- Update to 0.9.8

* Tue Oct 14 2014 David Scott <dave.scott@citrix.com> - 0.9.7-1
- Update to 0.9.7

* Wed Jun  4 2014 Jon Ludlam <jonathan.ludlam@citrix.com> - 0.9.6-1
- Update to 0.9.6

* Mon Jun  2 2014 Euan Harris <euan.harris@citrix.com> - 0.9.4-2
- Split files correctly between base and devel packages

* Wed Jun  5 2013 David Scott <dave.scott@eu.citrix.com> - 0.9.4-1
- Update to 0.9.3

* Wed May 29 2013 Mike McClurg <mike.mcclurg@citrix.com>
- Initial package
