Summary:	C grammar for tree-sitter
Summary(pl.UTF-8):	Gramatyka języka C dla tree-sittera
Name:		tree-sitter-c
Version:	0.24.1
Release:	1
License:	MIT
Group:		Libraries
#Source0Download: https://github.com/tree-sitter/tree-sitter-c/releases
Source0:	https://github.com/tree-sitter/tree-sitter-c/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	e399309a829fa3bcb09609c9de2472f2
URL:		https://github.com/tree-sitter/tree-sitter-c
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		soname_ver	0

%description
C grammar for tree-sitter.

%description -l pl.UTF-8
Gramatyka języka C dla tree-sittera.

%package -n neovim-parser-c
Summary:	C parser for Neovim
Summary(pl.UTF-8):	Analizator składni języka C dla Neovima
Group:		Applications/Editors
Requires:	%{name} = %{version}-%{release}

%description -n neovim-parser-c
C parser for Neovim.

%description -n neovim-parser-c -l pl.UTF-8
Analizator składni języka C dla Neovima.

%prep
%setup -q

%build
%{__cc} %{rpmldflags} %{rpmcppflags} %{rpmcflags} -fPIC -shared -Wl,-soname,libtree-sitter-c.so.%{soname_ver} src/parser.c -o libtree-sitter-c.so.%{version}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir},%{_libdir}/nvim/parser}

cp -p libtree-sitter-c.so.%{version} $RPM_BUILD_ROOT%{_libdir}
%{__ln_s} libtree-sitter-c.so.%{version} $RPM_BUILD_ROOT%{_libdir}/libtree-sitter-c.so.%{soname_ver}

%{__ln_s} %{_libdir}/libtree-sitter-c.so.%{soname_ver} $RPM_BUILD_ROOT%{_libdir}/nvim/parser/c.so

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc LICENSE README.md
%{_libdir}/libtree-sitter-c.so.*.*
%ghost %{_libdir}/libtree-sitter-c.so.%{soname_ver}

%files -n neovim-parser-c
%defattr(644,root,root,755)
%{_libdir}/nvim/parser/c.so
