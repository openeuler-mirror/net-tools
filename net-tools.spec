Name:          net-tools
Version:       2.0
Release:       0.55
Summary:       Important Programs for Networking
License:       GPLv2+
URL:           https://sourceforge.net/projects/net-tools/
Source0:       net-tools-115f1af2494ded1fcd21c8419d5e289bc4df380f.tar.xz
Source1:       net-tools-config.h
Source2:       net-tools-config.make
Source3:       ether-wake.c
Source4:       ether-wake.8
Source5:       mii-diag.c
Source6:       mii-diag.8
Source7:       iptunnel.8
Source8:       ipmaddr.8
Source9:       arp-ethers.service

Patch1:        net-tools-cycle.patch
Patch2:        net-tools-man.patch
Patch3:        net-tools-linux48.patch
Patch20:       ether-wake-interfaces.patch
Patch21:       net-tools-ifconfig-EiB.patch
Patch22:       net-tools-timer-man.patch
Patch23:       net-tools-interface-name-len.patch
Patch24:       backport-interface-change-pointopoint-short-flag-from-P-to-p.patch

BuildRequires: bluez-libs-devel gettext, libselinux libselinux-devel systemd gcc
%{?systemd_requires}

%description
This package contains programs for network administration and maintenance.
Most of the utilities formerly contained in this package (netstat, arp,
ifconfig, rarp, route) are obsoleted by the tools from iproute2 package (ip, ss)
and have been moved to net-tools-deprecated.

%package_help

%prep
%setup -q -c
cp %SOURCE1 ./config.h
cp %SOURCE2 ./config.make
cp %SOURCE3 .
cp %SOURCE4 ./man/en_US
cp %SOURCE5 .
cp %SOURCE6 ./man/en_US
cp %SOURCE7 ./man/en_US
cp %SOURCE8 ./man/en_US
%patch1 -p1 -b .cycle
%patch2 -p1 -b .man
%patch3 -p1 -b .linux48
%patch20 -p1 -b .interfaces
%patch21 -p1 -b .ifconfig-EiB
%patch22 -p1 -b .timer-man
%patch23 -p1 -b .interface-name-len
%patch24 -p1
touch ./config.h

%build
export CFLAGS="${RPM_OPT_FLAGS} -fpie"
export LDFLAGS="${RPM_LD_FLAGS} -pie -Wl,-z,now"
make
make ether-wake
gcc ${RPM_OPT_FLAGS} ${RPM_LD_FLAGS} -o mii-diag mii-diag.c

%install
mv man/de_DE man/de
mv man/fr_FR man/fr
mv man/pt_BR man/pt
make BASEDIR=%{buildroot} BINDIR=%{_bindir} SBINDIR=%{_sbindir} install
cp %{buildroot}%{_bindir}/ifconfig %{buildroot}%{_sbindir}
rm -f %{buildroot}%{_bindir}/ifconfig
cp %{buildroot}%{_bindir}/route %{buildroot}%{_sbindir}
rm -f %{buildroot}%{_bindir}/route
cp -p  ether-wake %{buildroot}%{_sbindir}
chmod 755 %{buildroot}%{_sbindir}/ether-wake
cp -p  mii-diag %{buildroot}%{_sbindir}
chmod 755 %{buildroot}%{_sbindir}/mii-diag
mkdir -p %{buildroot}%{_unitdir}
cp %{SOURCE9} %{buildroot}%{_unitdir}
chmod 644 %{buildroot}%{_unitdir}/arp-ethers.service
touch %{buildroot}%{_unitdir}/arp-ethers.service

%post
%systemd_post arp-ethers.service

%files
%defattr(-,root,root)
%license COPYING
%{_bindir}/netstat
%{_prefix}/lib/systemd/system/arp-ethers.service
%{_sbindir}/*
%{_datadir}/locale/*
%exclude %{_sbindir}/rarp

%files help
%defattr(-,root,root)
%{_mandir}/de/man5/*.gz
%{_mandir}/de/man8/*.gz
%{_mandir}/fr/man5/*.gz
%{_mandir}/fr/man8/*.gz
%{_mandir}/man5/ethers.5.gz
%{_mandir}/man8/*.gz
%{_mandir}/pt/man8/*.gz

%exclude %{_mandir}/man8/rarp.8*
%exclude %{_mandir}/de/man8/rarp.8*
%exclude %{_mandir}/fr/man8/rarp.8*
%exclude %{_mandir}/pt/man8/rarp.8*
%exclude %{_mandir}/de/man1
%exclude %{_mandir}/fr/man1
%exclude %{_mandir}/man1
%exclude %{_mandir}/pt/man1
%exclude %{_mandir}/pt/man5

%changelog
* Thu Oct 20 2022 konglidong <konglidong@uniontech.com> - 2.0-0.55
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:interface: change pointopoint short flag from P to p

* Tue Dec 31 2019 openEuler Buildteam <buildteam@openeuler.org> - 2.0-0.54
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:optimization the spec

* Wed Sep 11 2019 openEuler Buildteam <buildteam@openeuler.org> - 2.0-0.53
- Package init

