Name:		stringtemplate
Version:	3.2.1
Release:	10.3
Summary:	A Java template engine
Group:		Development/Java
License:	BSD
URL:		https://www.stringtemplate.org/
Source0:	https://repo1.maven.org/maven2/org/antlr/stringtemplate/%{version}/stringtemplate-%{version}-sources.jar
BuildArch:	noarch
BuildRequires:	python
BuildRequires:	maven
BuildRequires:	java-current-devel
BuildRequires:	antlr-tool
BuildSystem:	maven
BuildOption(install):	--file-name %{name}

%description
StringTemplate 3 is a template engine for generating source code and
other formatted text. ANTLR 3's runtime imports it from one tree class.

%prep
%setup -q -c -T
# The builders' rpmuncompress passes a sources jar to tar.
python - %{SOURCE0} <<'PY'
import sys
import zipfile
zipfile.ZipFile(sys.argv[1]).extractall(".")
PY
mkdir -p src/main/java
mv org src/main/java/
python - %{version} <<'PY'
import sys
from pathlib import Path
version = sys.argv[1]
Path("pom.xml").write_text(f"""<?xml version="1.0" encoding="UTF-8"?>
<project>
  <modelVersion>4.0.0</modelVersion>
  <groupId>org.antlr</groupId>
  <artifactId>stringtemplate</artifactId>
  <version>{version}</version>
  <packaging>jar</packaging>
  <name>StringTemplate</name>
  <dependencies>
    <dependency>
      <groupId>antlr</groupId>
      <artifactId>antlr</artifactId>
    </dependency>
  </dependencies>
</project>
""")
PY

%files -f .mfiles
