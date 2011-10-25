Summary: A Java template engine
Name: stringtemplate
Version: 3.2.1
Release: 2
URL: http://www.stringtemplate.org/
Source0: http://www.stringtemplate.org/download/stringtemplate-%{version}.tar.gz
# Build jUnit tests + make the antlr2 generated code before preparing sources
Patch0: stringtemplate-3.1-build-junit.patch
License: BSD
Group: Development/Java
BuildArch: noarch
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: ant-antlr, ant-junit
BuildRequires: antlr
# Standard deps
BuildRequires: java-devel >= 0:1.6.0
BuildRequires: jpackage-utils
Requires: java >= 0:1.6.0
Requires: jpackage-utils

%description
StringTemplate is a java template engine (with ports for 
C# and Python) for generating source code, web pages,
emails, or any other formatted text output. StringTemplate
is particularly good at multi-targeted code generators,
multiple site skins, and internationalization/localization.

%package        javadoc
Summary:        API documentation for %{name}
Group:          Development/Java
Requires:       java-javadoc

%description    javadoc
API documentation for %{name}.

%prep
%setup -q
%patch0

%build
rm -rf lib target
ant jar
ant javadocs -Dpackages= -Djavadocs.additionalparam=

%install
rm -rf $RPM_BUILD_ROOT
install -D build/stringtemplate.jar $RPM_BUILD_ROOT%{_datadir}/java/stringtemplate.jar
(cd $RPM_BUILD_ROOT%{_datadir}/java/ && ln -s stringtemplate.jar stringtemplate-%{version}.jar)
install -dm 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}
cp -pR docs/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}

install -Dpm 644 pom.xml $RPM_BUILD_ROOT%{_mavenpomdir}/JPP-%{name}.pom
%add_to_maven_depmap org.antlr %{name} %{version} JPP %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_maven_depmap

%postun
%update_maven_depmap

%check
ant test

%files
%defattr(-,root,root)
%doc LICENSE.txt README.txt
%{_datadir}/java/*.jar
%{_mavenpomdir}/JPP-%{name}.pom
%config(noreplace) %{_mavendepmapfragdir}/%{name}

%files javadoc
%defattr(-,root,root)
%{_javadocdir}/%{name}

