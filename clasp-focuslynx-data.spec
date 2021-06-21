Name:      clasp-focuslynx-data
Version:   20210621
Release:   0
Url:       https://github.com/warwick-one-metre/focuslynxd
Summary:   Focuser configuration files.
License:   GPL-3.0
Group:     Unspecified
BuildArch: noarch

%description

%build
mkdir -p %{buildroot}%{_udevrulesdir}
mkdir -p %{buildroot}%{_sysconfdir}/focusd/

%{__install} %{_sourcedir}/10-clasp-focuser.rules %{buildroot}%{_udevrulesdir}
%{__install} %{_sourcedir}/clasp.json %{buildroot}%{_sysconfdir}/focusd/

%files
%defattr(0644,root,root,-)
%{_udevrulesdir}/10-clasp-focuser.rules
%{_sysconfdir}/focusd/clasp.json

%changelog
