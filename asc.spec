Summary:	Advanced Strategic Command
Name:		asc
Version:	2.5.0.0
Release:	1
License:	GPLv2+
Group:		Games/Strategy
URL:		http://www.asc-hq.org/
Source0:	http://heanet.dl.sourceforge.net/sourceforge/asc-hq/%{name}-%{version}.tar.bz2
Source1:	%{name}-16x16.png
Source2:	%{name}-32x32.png
Source3:	%{name}-48x48.png
Patch0:		asc-2.5.0.0-gcc47.patch
BuildRequires:	boost-devel
BuildRequires:	bzip2-devel
BuildRequires:	jpeg-devel
BuildRequires:	libgii-devel
BuildRequires:	libphysfs-devel
BuildRequires:	SDL_image-devel
BuildRequires:	SDL_mixer-devel
BuildRequires:	SDL_sound-devel
BuildRequires:	wxgtku-devel
BuildRequires:	pkgconfig(expat)
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(lua)
BuildRequires:	pkgconfig(sigc++-1.2)
BuildRequires:	zip

%description
ASC is a free, turn based strategy game. It is designed in the tradition
of the Battle Isle series from Bluebyte.

%prep
%setup -q
%patch0 -p0
# there seems to be a conflict with libintl defines
# find . -type f -exec perl -pi -e 's/gettext/gettex_/g' {} \;

%build
%configure2_5x	--enable-genparse \
		--disable-paragui \
		--bindir=%{_gamesbindir} 
perl -pi -e 's|^SUBDIRS = (.*)music(.*)|SUBDIRS = $1 $2|' data/Makefile
%make

%install
%makeinstall bindir=%{buildroot}%{_gamesbindir}

install -d %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=%{summary}
Comment=%{summary}
Exec=%{_gamesbindir}/%{name}
Icon=%{name}
Terminal=false
Type=Application
Categories=Game;StrategyGame;
EOF

install %{SOURCE1} -D %{buildroot}%{_miconsdir}/%{name}.png
install %{SOURCE2} -D %{buildroot}%{_iconsdir}/%{name}.png
install %{SOURCE3} -D %{buildroot}%{_liconsdir}/%{name}.png

%files
%defattr(755,root,root,755)
%{_gamesbindir}/%{name}*
%defattr(644,root,root,755)
%doc README COPYING AUTHORS doc/
%{_gamesdatadir}/%{name}
%{_datadir}/applications/mandriva-%{name}.desktop
%{_miconsdir}/%{name}.png
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_mandir}/man6/*


