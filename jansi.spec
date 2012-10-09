Name:             jansi
Version:          1.9
Release:          1%{?dist}
Summary:          Jansi is a java library for generating and interpreting ANSI escape sequences
Group:            Development/Libraries
License:          ASL 2.0
URL:              http://jansi.fusesource.org/

# git clone git://github.com/fusesource/jansi.git
# cd jansi && git archive --format=tar --prefix=jansi-1.9/ jansi-project-1.9 | xz > jansi-1.9.tar.xz
Source0:          jansi-%{version}.tar.xz

BuildArch:        noarch

BuildRequires:    jpackage-utils
BuildRequires:    java-devel
BuildRequires:    maven
BuildRequires:    maven-compiler-plugin
BuildRequires:    maven-install-plugin
BuildRequires:    maven-jar-plugin
BuildRequires:    maven-javadoc-plugin
BuildRequires:    maven-release-plugin
BuildRequires:    maven-surefire-plugin
BuildRequires:    jansi-native
BuildRequires:    maven-clean-plugin
BuildRequires:    maven-plugin-bundle
BuildRequires:    junit4
BuildRequires:    fusesource-pom
BuildRequires:    maven-surefire-provider-junit4

Requires:         java
Requires:         jpackage-utils
Requires:         jansi-native
Requires:         hawtjni

%description
Jansi is a small java library that allows you to use ANSI escape sequences
in your Java console applications. It implements ANSI support on platforms
which don't support it like Windows and provides graceful degradation for
when output is being sent to output devices which cannot support ANSI sequences. 

%package javadoc
Summary:          Javadocs for %{name}
Group:            Documentation
Requires:         jpackage-utils

%description javadoc
This package contains the API documentation for %{name}.

%prep
%setup -q

%pom_disable_module jansi-website
%pom_xpath_remove "pom:build/pom:extensions"

# No org.fusesource.mvnplugins:fuse-javadoc-skin available
%pom_remove_plugin "org.apache.maven.plugins:maven-dependency-plugin"

# No maven-uberize-plugin
%pom_xpath_remove "pom:build/pom:plugins/pom:plugin[pom:artifactId = 'maven-uberize-plugin']" jansi/pom.xml

%build
mvn-rpmbuild install javadoc:aggregate

%install
# JAR
mkdir -p $RPM_BUILD_ROOT%{_javadir}
cp -p %{name}/target/%{name}-%{version}.jar  $RPM_BUILD_ROOT%{_javadir}/%{name}.jar

# JAVADOC
mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/%{name}
cp -rp target/site/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}

# POM
install -d -m 755 $RPM_BUILD_ROOT%{_mavenpomdir}
install -pm 644 pom.xml $RPM_BUILD_ROOT%{_mavenpomdir}/JPP-%{name}-project.pom
install -pm 644 %{name}/pom.xml $RPM_BUILD_ROOT%{_mavenpomdir}/JPP-%{name}.pom

# DEPMAP
%add_maven_depmap JPP-%{name}-project.pom
%add_maven_depmap JPP-%{name}.pom %{name}.jar

%files
%{_mavenpomdir}/*
%{_mavendepmapfragdir}/*
%{_javadir}/*
%doc readme.md license.txt changelog.md

%files javadoc
%{_javadocdir}/%{name}
%doc license.txt

%changelog
* Tue Oct 09 2012 Marek Goldmann <mgoldman@redhat.com> - 1.9-1
- Upstream release 1.9, RHBZ#864490

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri May 04 2012 Tomas Radej <tradej@redhat.com> - 1.6-3
- Removed maven-license-plugin BR

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Aug 25 2011 Marek Goldmann <mgoldman@redhat.com> 1.6-1
- Upstream release 1.6
- Spec file cleanup

* Fri May 27 2011 Marek Goldmann <mgoldman@redhat.com> 1.5-1
- Initial packaging

