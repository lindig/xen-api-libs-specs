Name:           xcp-networkd
Version:        0.10.1
Release:        2%{?dist}
Summary:        Simple host network management service for the xapi toolstack
License:        LGPL
URL:            https://github.com/xapi-project/xcp-networkd
Source0:        https://github.com/xapi-project/xcp-networkd/archive/v%{version}/xcp-networkd-%{version}.tar.gz
Source1:        xcp-networkd-init
Source2:        xcp-networkd-conf
Source3:        xcp-networkd-network-conf
#Source4:        xcp-networkd-bridge-conf
BuildRequires:  ocaml
BuildRequires:  ocaml-findlib-devel
BuildRequires:  ocaml-obuild
BuildRequires:  ocaml-rpc-devel
BuildRequires:  ocaml-xcp-idl-devel
BuildRequires:  forkexecd-devel
BuildRequires:  ocaml-stdext-devel
BuildRequires:  ocaml-xen-api-libs-transitional-devel
BuildRequires:  ocaml-ounit-devel
BuildRequires:  ocaml-xcp-inventory-devel
BuildRequires:  ocaml-xen-api-client-devel
BuildRequires:  ocaml-netlink-devel
BuildRequires:  libffi-devel
BuildRequires:  ocaml-bisect-ppx-devel
Requires:       ethtool
Requires:       libnl3
#Requires:       redhat-lsb-core

Requires(post): /sbin/chkconfig
Requires(preun): /sbin/chkconfig
Requires(preun): /sbin/service

%description
Simple host networking management service for the xapi toolstack.

%prep
%setup -q
cp %{SOURCE1} xcp-networkd-init
cp %{SOURCE2} xcp-networkd-conf
cp %{SOURCE3} xcp-networkd-network-conf
#cp %{SOURCE4} xcp-networkd-bridge-conf

%build
mkdir build-bin build-cov
make
make install DESTDIR=$PWD/build-bin BINDIR=%{_bindir} SBINDIR=%{_sbindir}

make clean
make coverage
make
make install DESTDIR=$PWD/build-cov BINDIR=%{_bindir} SBINDIR=%{_sbindir}

%install
(cd $PWD/build-cov; tar cf - .) | (cd %{buildroot}; tar xf -)

# rename
mv    %{buildroot}%{_sbindir}/xcp-networkd %{buildroot}%{_sbindir}/xcp-networkd.cov
mv    %{buildroot}%{_bindir}/networkd_db   %{buildroot}%{_bindir}/networkd_db.cov

(cd $PWD/build-bin; tar cf - .) | (cd %{buildroot}; tar xf -)
mv    %{buildroot}%{_sbindir}/xcp-networkd %{buildroot}%{_sbindir}/xcp-networkd.bin
mv    %{buildroot}%{_bindir}/networkd_db   %{buildroot}%{_bindir}/networkd_db.bin

# touch %ghost'ed files; these are created dynamically during installation
touch %{buildroot}%{_sbindir}/xcp-networkd
touch %{buildroot}%{_bindir}/networkd_db

install -D -m 0755 xcp-networkd-init %{buildroot}%{_sysconfdir}/init.d/xcp-networkd
install -D -m 0644 xcp-networkd-network-conf %{buildroot}/etc/xensource/network.conf
install -D -m 0644 xcp-networkd-conf %{buildroot}/etc/xcp-networkd.conf


%files
%doc README.markdown LICENSE MAINTAINERS
%ghost %{_sbindir}/xcp-networkd
%ghost %{_bindir}/networkd_db
%{_sbindir}/xcp-networkd.bin
%{_bindir}/networkd_db.bin
%{_sysconfdir}/init.d/xcp-networkd
%{_mandir}/man1/xcp-networkd.1.gz
#/etc/modprobe.d/bridge.conf
%config(noreplace) /etc/xensource/network.conf
%config(noreplace) /etc/xcp-networkd.conf

%post
case $1 in
  1) # install
    ln -fs %{_sbindir}/xcp-networkd.bin  %{_sbindir}/xcp-networkd
    ln -fs %{_bindir}/networkd_db.bin    %{_bindir}/networkd_db
    /sbin/chkconfig --add xcp-networkd
    ;;
  2) # upgrade
    ln -fs %{_sbindir}/xcp-networkd.bin  %{_sbindir}/xcp-networkd
    ln -fs %{_bindir}/networkd_db.bin    %{_bindir}/networkd_db
    /sbin/chkconfig --del xcp-networkd
    /sbin/chkconfig --add xcp-networkd
    ;;
esac

%preun
case $1 in
  0) # uninstall
    /sbin/service xcp-networkd stop >/dev/null 2>&1 || :
    /sbin/chkconfig --del xcp-networkd
    ;;
  1) # upgrade
    ;;
esac

%package coverage
Summary: Simple host network management service for the xapi toolstack:
Requires:       %{name} = %{version}-%{release}

%description coverage
This package enables coverage profiling.

%files coverage
%ghost %{_sbindir}/xcp-networkd
%ghost %{_bindir}/networkd_db
%{_sbindir}/xcp-networkd.cov
%{_bindir}/networkd_db.cov

%post coverage
case $1 in
  1) # install
    ln -fs %{_sbindir}/xcp-networkd.cov  %{_sbindir}/xcp-networkd
    ln -fs %{_bindir}/networkd_db.cov    %{_bindir}/networkd_db
    /sbin/chkconfig --add xcp-networkd
    ;;
  2) # upgrade
    ln -fs %{_sbindir}/xcp-networkd.cov  %{_sbindir}/xcp-networkd
    ln -fs %{_bindir}/networkd_db.cov    %{_bindir}/networkd_db
    /sbin/chkconfig --del xcp-networkd
    /sbin/chkconfig --add xcp-networkd
    ;;
esac


%changelog
* Thu May 26 2016 Christian Lindig <christian.lindig@citrix.com> - 0.10.1-2
- fix %post coverage: remove existing symlink before creatign new one

* Fri May 20 2016 Christian Lindig <christian.lindig@citrix.com> - 0.10.1-1
- New upstream release that supports coverage profiling
- introduce subpackage for coverage profiling

* Mon May 16 2016 Si Beaumont <simon.beaumont@citrix.com> - 0.9.6-2
- Re-run chkconfig on upgrade

* Wed Jun 4 2014 Jon Ludlam <jonathan.ludlam@citrix.com> - 0.9.4-1
- Update to 0.9.4
- Add networkd_db CLI

* Wed Sep 25 2013 David Scott <dave.scott@eu.citrix.com> - 0.9.3-1
- Update to 0.9.3

* Wed Aug 28 2013 David Scott <dave.scott@eu.citrix.com>
- When loading the bridge module, prevent guest traffic being
  processed by the domain 0 firewall

* Sun Jun  9 2013 David Scott <dave.scott@eu.citrix.com>
- Update to 0.9.2

* Fri Jun  7 2013 David Scott <dave.scott@eu.citrix.com>
- Update to 0.9.1

* Wed Jun  5 2013 David Scott <dave.scott@eu.citrix.com>
- Initial package

# vim: set ts=2 sw=2 et:
