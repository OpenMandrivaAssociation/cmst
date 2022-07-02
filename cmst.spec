Summary:	A Qt based GUI front end for the connman connection manager with systemtray icon
Name:		cmst
Version:	2022.05.01
Release:	1
License:	MIT
URL:		https://github.com/andrew-bibb/cmst
Source0:	https://github.com/andrew-bibb/cmst/releases/download/%{name}-%{version}/%{name}-%{version}.tar.xz
Source1:	%{name}.service
BuildRequires:	qmake5
BuildRequires:	pkgconfig(Qt5Core)
BuildRequires:	cmake(Qt5LinguistTools)
BuildRequires:	pkgconfig(Qt5Gui)
BuildRequires:	pkgconfig(Qt5DBus)
BuildRequires:	pkgconfig(Qt5Widgets)
BuildRequires:	pkgconfig(Qt5Network)
Requires:	connman
Requires:	hicolor-icon-theme
%{?systemd_requires}

%description
QT GUI for Connman with system tray icon.
The program provides graphical user interface to control the connman daemon.
The connman daemon must be started as you normally would, this program just
interfaces with that daemon. You can see what technologies and services
connman has found, and for wifi services an agent is registered to assist in
obtaining the information from you necessary to logon the wifi service.

%prep
%autosetup -p1

sed -i -e 's|Categories=Settings;System;Qt;Network;|Categories=Network;|g' misc/desktop/cmst.desktop
sed -i -e 's|CMST_LIB_PATH = "/usr/lib/cmst"|CMST_LIB_PATH = "%{_libexecdir}/%{name}"|g' cmst.pri

# change permission due rpmlint W: spurious-executable-perm
find . -type f  \( -name "*.cpp" -o -name "*.h" \) -exec chmod a-x {} \;

%build
# Create translation files.
lrelease translations/*.ts

%qmake_qt5
%make_build

%install
%make_install INSTALL_ROOT=%{buildroot}

install -d -m 0755 %{buildroot}%{_datadir}/%{name}/languages
install -m 0644 translations/*.qm %{buildroot}%{_datadir}/%{name}/languages

mkdir -p %{buildroot}%{_unitdir}
install -Dpm 644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service
install -d %{buildroot}%{_presetdir}
cat > %{buildroot}%{_presetdir}/86-%{name}.preset << EOF
enable %{name}.service
EOF

%find_lang %{name} --with-qt

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%files -f %{name}.lang
%doc README.md
%license text/LICENSE
%{_bindir}/%{name}
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/org.cmst.roothelper.conf
%{_presetdir}/86-%{name}.preset
%{_unitdir}/%{name}.service
%{_libexecdir}/%{name}/
%{_datadir}/applications/*.desktop
%{_datadir}/metainfo/org.cmst.cmst.appdata.xml
%{_datadir}/dbus-1/system-services/org.cmst.roothelper.service
%{_datadir}/icons/hicolor/*/apps/%{name}.*
%{_datadir}/%{name}/autostart/%{name}-autostart.desktop
%doc %{_mandir}/man1/*
