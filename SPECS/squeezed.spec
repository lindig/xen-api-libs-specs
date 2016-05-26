Name:           squeezed
Version:        0.12.1
Release:        2%{?dist}
Summary:        Memory ballooning daemon for the xapi toolstack
License:        LGPL
URL:            https://github.com/xapi-project/squeezed
Source0:        https://github.com/xapi-project/squeezed/archive/v%{version}/squeezed-%{version}.tar.gz
Source1:        squeezed-init
Source2:        squeezed-conf
BuildRequires:  ocaml
BuildRequires:  ocaml-findlib
BuildRequires:  ocaml-re-devel
BuildRequires:  ocaml-rpc-devel
BuildRequires:  ocaml-stdext-devel
BuildRequires:  ocaml-uuidm-devel
BuildRequires:  ocaml-xcp-idl-devel
BuildRequires:  xen-ocaml-devel
BuildRequires:  ocaml-xenstore-clients-devel
BuildRequires:  ocaml-xenstore-devel
BuildRequires:  xen-devel
BuildRequires:  xen-dom0-libs-devel
BuildRequires:  xen-dom0-libs
BuildRequires:  xen-libs-devel
BuildRequires:  xen-libs
BuildRequires:  ocaml-bisect-ppx-devel
#Requires:       redhat-lsb-core
Requires:       message-switch

Requires(post): /sbin/chkconfig
Requires(preun): /sbin/chkconfig
Requires(preun): /sbin/service

%description
Memory ballooning daemon for the xapi toolstack.

%prep
%setup -q
cp %{SOURCE1} squeezed-init
cp %{SOURCE2} squeezed-conf


# we have two builds (regular, coverage) and install binaries from both
# under different names

%build
./configure --prefix %{_prefix} --destdir %{_buildroot}
make
mv _build/src/squeezed.native squeezed.bin

make clean

./configure --prefix %{_prefix} --destdir %{_buildroot}
make coverage
make
mv _build/src/squeezed.native squeezed.cov


%install
# touch %ghost'ed files that are created during installation
mkdir -p %{buildroot}%{_sbindir}
touch %{buildroot}%{_sbindir}/squeezed

install -D -m 0755 squeezed.bin  %{buildroot}%{_sbindir}/squeezed.bin
install -D -m 0755 squeezed.cov  %{buildroot}%{_sbindir}/squeezed.cov
install -D -m 0755 squeezed-init %{buildroot}%{_sysconfdir}/init.d/squeezed
install -D -m 0644 squeezed-conf %{buildroot}%{_sysconfdir}/squeezed.conf


%files
%doc README.md
%doc LICENSE
%doc MAINTAINERS
%ghost %{_sbindir}/squeezed
%{_sbindir}/squeezed.bin
%{_sysconfdir}/init.d/squeezed
%config %{_sysconfdir}/squeezed.conf

%post
case $1 in
  1) # install
    rm -f %{_sbindir}/squeezed
    ln -s %{_sbindir}/squeezed.bin %{_sbindir}/squeezed
    /sbin/chkconfig --add squeezed
    ;;
  2) # upgrade
    rm -f %{_sbindir}/squeezed
    ln -s %{_sbindir}/squeezed.bin %{_sbindir}/squeezed
    /sbin/chkconfig --del squeezed
    /sbin/chkconfig --add squeezed
    ;;
esac

%preun
case $1 in
  0) # uninstall
    /sbin/service squeezed stop >/dev/null 2>&1 || :
    /sbin/chkconfig --del squeezed
    ;;
  1) # upgrade
    ;;
esac

# -- coverage

%package        coverage
Summary:        Enable coverage profiling for this package
Requires:       %{name} = %{version}-%{release}

%description    coverage
Memory ballooning daemon for the xapi toolstack with coverage profiling
enabled.

%files coverage
%ghost %{_sbindir}/squeezed
%{_sbindir}/squeezed.cov

%post coverage
case $1 in
  1) # install
    rm -f %{_sbindir}/squeezed
    ln -s %{_sbindir}/squeezed.cov %{_sbindir}/squeezed
    /sbin/chkconfig --add squeezed
    ;;
  2) # upgrade
    rm -f %{_sbindir}/squeezed
    ln -s %{_sbindir}/squeezed.cov %{_sbindir}/squeezed
    /sbin/chkconfig --del squeezed
    /sbin/chkconfig --add squeezed
    ;;
esac

%preun coverage
case $1 in
  0) # uninstall
    /sbin/service squeezed stop >/dev/null 2>&1 || :
    /sbin/chkconfig --del squeezed
    ;;
  1) # upgrade
    ;;
esac



%changelog
* Thu May 26 2016 Christian Lindig <christian.lindig@citrix.com> - 0.12.1-2
- Fix %post: rm existing symlink before installation

* Fri May 20 2016 Christian Lindig <christian.lindig@citrix.com> - 0.12.1-1
- New sub-package for coverage analysis (from new upstream release)

* Mon May 16 2016 Si Beaumont <simon.beaumont@citrix.com> - 0.11.0-2
- Re-run chkconfig on upgrade

* Thu Sep 4 2014 Jon Ludlam <jonathan.ludlam@citrix.com> - 0.10.6-2
- Remove dependency on xen-missing-headers

* Fri Jun  6 2014 Jonathan Ludlam <jonathan.ludlam@citrix.com> - 0.10.6-1
- Update to 0.10.6

* Fri Apr 11 2014 Euan Harris <euan.harris@citrix.com> - 0.10.5-1
- Switch build from obuild to oasis

* Wed Sep 25 2013 David Scott <dave.scott@eu.citrix.com> - 0.10.4-1
- Update to 0.10.4

* Fri Sep 20 2013 David Scott <dave.scott@eu.citrix.com> - 0.10.3-1
- Update to allow minimal operation without xen

* Tue Sep 10 2013 David Scott <dave.scott@eu.citrix.com> - 0.10.2-1
- Update to new xenstore interface in v1.2.3

* Wed Sep 04 2013 David Scott <dave.scott@eu.citrix.com> - 0.10.1-1
- Add get_domain_zero_palicy call required for domain 0 ballooning

* Mon Sep  2 2013 David Scott <dave.scott@eu.citrix.com> - 0.10.0-1
- Update to 0.10.0, with support for domain 0 ballooning

* Wed Jun  5 2013 David Scott <dave.scott@eu.citrix.com>
- Initial package

