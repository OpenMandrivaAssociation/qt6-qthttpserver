#define beta rc
#define snapshot 20200627
%define major 6

%define _qtdir %{_libdir}/qt%{major}

Name:		qt6-qthttpserver
Version:	6.12.0
Release:	%{?beta:0.%{beta}.}%{?snapshot:0.%{snapshot}.}2
%if 0%{?snapshot:1}
# "git archive"-d from "dev" branch of git://code.qt.io/qt/qthttpserver.git
Source:		qthttpserver-%{?snapshot:%{snapshot}}%{!?snapshot:%{version}}.tar.zst
%else
Source:		https://download.qt.io/%{?beta:development}%{!?beta:official}_releases/qt/%(echo %{version}|cut -d. -f1-2)/%{version}%{?beta:-%{beta}}/submodules/qthttpserver-everywhere-src-%{version}%{?beta:-%{beta}}.tar.xz
%endif
Group:		System/Libraries
Summary:	Qt %{major} HTTP Server module
BuildRequires:	cmake
BuildRequires:	ninja
BuildRequires:	cmake(Qt%{major}Core)
BuildRequires:	cmake(Qt%{major}Network)
BuildRequires:	cmake(Qt%{major}Widgets)
BuildRequires:	qt%{major}-cmake
License:	LGPLv3/GPLv3/GPLv2

%patchlist
# CVE-2026-110944: a chunked request with an endless chunk-size line
# grew the fragment buffer without a ceiling, and a bad chunk size was
# parsed without checking conversion. Cap the line and reject a size
# that does not fit qsizetype. 6.12: d0b683915dd1, 3376ff1f1fde,
# QTBUG-150270
qthttpserver-6.12.0-cve-2026-110944-0001.patch
qthttpserver-6.12.0-cve-2026-110944-0002.patch

%description
Qt %{major} HTTP Server module

%global extra_devel_files_HttpServer \
%{_qtdir}/sbom/*

%qt6libs HttpServer

%package examples
Summary: Examples for the Qt %{major} Network Authentication module
Group: Development/KDE and Qt

%description examples
Examples for the Qt %{major} Network Authentication module

%files examples
%{_qtdir}/examples/httpserver

%prep
%autosetup -p1 -n qthttpserver%{!?snapshot:-everywhere-src-%{version}%{?beta:-%{beta}}}
%cmake -G Ninja \
	-DQT_BUILD_TESTS:BOOL=OFF \
	-DCMAKE_INSTALL_PREFIX=%{_qtdir} \
	-DQT_BUILD_EXAMPLES:BOOL=ON \
	-DQT_WILL_INSTALL:BOOL=ON

%build
export LD_LIBRARY_PATH="$(pwd)/build/lib:${LD_LIBRARY_PATH}"
%ninja_build -C build

%install
%ninja_install -C build
%qt6_postinstall
