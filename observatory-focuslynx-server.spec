Name:      observatory-focuslynx-server
Version:   20220727
Release:   0
Url:       https://github.com/warwick-one-metre/focuslynxd
Summary:   Focuser control server for Optec Focus Lynx hardware.
License:   GPL-3.0
Group:     Unspecified
BuildArch: noarch
Requires:  python3 python3-Pyro4 python3-pyserial python3-warwick-observatory-common python3-warwick-observatory-focuslynx

%description

%build
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_unitdir}
mkdir -p %{buildroot}%{_udevrulesdir}
mkdir -p %{buildroot}%{_sysconfdir}/focusd/

%{__install} %{_sourcedir}/focusd %{buildroot}%{_bindir}
%{__install} %{_sourcedir}/focusd@.service %{buildroot}%{_unitdir}

%files
%defattr(0755,root,root,-)
%{_bindir}/focusd
%defattr(0644,root,root,-)
%{_unitdir}/focusd@.service

%changelog
