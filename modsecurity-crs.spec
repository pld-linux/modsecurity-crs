#
# Conditional build:
%bcond_without	tests		# parse rules with libmodsecurity

Summary:	OWASP Core Rule Set (CRS) for ModSecurity-compatible WAF engines
Summary(pl.UTF-8):	Zestaw reguł OWASP CRS dla silników WAF zgodnych z ModSecurity
Name:		modsecurity-crs
Version:	4.30.0
Release:	1
License:	Apache v2.0
Group:		Networking/Daemons/HTTP
Source0:	https://github.com/coreruleset/coreruleset/archive/v%{version}/coreruleset-%{version}.tar.gz
# Source0-md5:	8a611e774ec674aac242e783d587243e
URL:		https://coreruleset.org/
%if %{with tests}
# for modsec-rules-check
BuildRequires:	libmodsecurity
%endif
BuildRequires:	rpmbuild(macros) >= 1.268
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The OWASP Core Rule Set (CRS) is a set of generic attack detection
rules for use with ModSecurity-compatible web application firewalls
(libmodsecurity v3, ModSecurity v2, Coraza). It aims to protect web
applications from a wide range of attacks, including the OWASP Top
Ten, with a minimum of false alerts.

%description -l pl.UTF-8
OWASP Core Rule Set (CRS) to zestaw ogólnych reguł wykrywania ataków
dla zapór aplikacyjnych zgodnych z ModSecurity (libmodsecurity v3,
ModSecurity v2, Coraza). Chroni aplikacje webowe przed szerokim
spektrum ataków, w tym OWASP Top Ten, przy minimalnej liczbie
fałszywych alarmów.

%prep
%setup -q -n coreruleset-%{version}

%build
%if %{with tests}
modsec-rules-check \
	crs-setup.conf.example \
	rules/*.conf
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_datadir}/%{name}/{rules,plugins}

cp -p crs-setup.conf.example $RPM_BUILD_ROOT%{_datadir}/%{name}
cp -p rules/*.conf rules/*.data $RPM_BUILD_ROOT%{_datadir}/%{name}/rules
# upstream placeholders keeping Include plugins/*-{config,before,after}.conf globs non-empty
cp -p plugins/empty-{config,before,after}.conf $RPM_BUILD_ROOT%{_datadir}/%{name}/plugins

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES.md INSTALL.md KNOWN_BUGS.md README.md SECURITY.md
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/plugins
%{_datadir}/%{name}/crs-setup.conf.example
%{_datadir}/%{name}/rules
%{_datadir}/%{name}/plugins/empty-config.conf
%{_datadir}/%{name}/plugins/empty-before.conf
%{_datadir}/%{name}/plugins/empty-after.conf
