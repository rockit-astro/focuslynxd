Name:      rasa-focuser-server
Version:   1.0.1
Release:   0
Url:       https://github.com/warwick-one-metre/rasa-focusd
Summary:   Focuser control client for the RASA prototype telescope.
License:   GPL-3.0
Group:     Unspecified
BuildArch: noarch

Requires:  python34, python34-Pyro4, python34-pyserial, python34-warwick-observatory-common, python34-warwick-rasa-focuser, observatory-log-client, %{?systemd_requires}


%description
Part of the observatory software for the RASA prototype telescope.

focusd interfaces with and wraps the Optec focusers and exposes them via Pyro.

%build
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_unitdir}
mkdir -p %{buildroot}%{_udevrulesdir}

%{__install} %{_sourcedir}/focusd %{buildroot}%{_bindir}
%{__install} %{_sourcedir}/rasa_focusd.service %{buildroot}%{_unitdir}
%{__install} %{_sourcedir}/10-rasa-focuser.rules %{buildroot}%{_udevrulesdir}

%post
%systemd_post rasa_focusd.service

%preun
%systemd_preun rasa_focusd.service

%postun
%systemd_postun_with_restart rasa_focusd.service

%files
%defattr(0755,root,root,-)
%{_bindir}/focusd
%defattr(0644,root,root,-)
%{_udevrulesdir}/10-rasa-focuser.rules
%{_unitdir}/rasa_focusd.service

%changelog
