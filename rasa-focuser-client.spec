Name:      rasa-focuser-client
Version:   1.2.1
Release:   0
Url:       https://github.com/warwick-one-metre/rasa-focusd
Summary:   Focuser control client for the RASA prototype telescope.
License:   GPL-3.0
Group:     Unspecified
BuildArch: noarch
Requires:  python36, python36-Pyro4, python36-warwick-observatory-common, python36-warwick-rasa-focuser

%description
Part of the observatory software for the RASA prototype telescope.

focus is a commandline utility for controlling the focusers.

%build
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}/etc/bash_completion.d
%{__install} %{_sourcedir}/focus %{buildroot}%{_bindir}
%{__install} %{_sourcedir}/completion/focus %{buildroot}/etc/bash_completion.d/focus

%files
%defattr(0755,root,root,-)
%{_bindir}/focus
/etc/bash_completion.d/focus

%changelog
