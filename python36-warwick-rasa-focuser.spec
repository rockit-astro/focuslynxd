Name:           python36-warwick-rasa-focuser
Version:        1.1.0
Release:        0
License:        GPL3
Summary:        Common backend code for the RASA prototype focuser daemon
Url:            https://github.com/warwick-one-metre/rasa-focusd
BuildArch:      noarch

%description
Part of the observatory software for the RASA prototype telescope.

python36-warwick-rasa-focuser holds the common focuser code.

%prep

rsync -av --exclude=build .. .

%build
%{__python3} setup.py build

%install
%{__python3} setup.py install --prefix=%{_prefix} --root=%{buildroot}

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
