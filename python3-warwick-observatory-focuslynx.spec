Name:           python3-warwick-observatory-focuslynx
Version:        20210612
Release:        0
License:        GPL3
Summary:        Common backend code for optec focuslynx daemon
Url:            https://github.com/warwick-one-metre/focuslynxd
BuildArch:      noarch

%description

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
