Summary:	C grammar for tree-sitter
Name:		tree-sitter-c
Version:	0.23.5
Release:	1
License:	MIT
Group:		Libraries
Source0:	https://github.com/tree-sitter/tree-sitter-c/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	5f3abada8e5ae0d63bd2a2c6eb963583
URL:		https://github.com/tree-sitter/tree-sitter-c
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		ts_c_soname	libtree-sitter-c.so.0

%description
C grammar for tree-sitter.

%package -n neovim-parser-c
Summary:	C parser for Neovim
Group:		Applications/Editors
Requires:	%{name} = %{version}-%{release}

%description -n neovim-parser-c
C parser for Neovim.

%prep
%setup -q

%build
%{__cc} %{rpmcppflags} %{rpmcflags} -fPIC -shared -Wl,-soname,%{ts_c_soname} src/parser.c -o libtree-sitter-c.so.%{version} %{rpmldflags}

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_libdir},%{_libdir}/nvim/parser}

cp -p libtree-sitter-c.so.%{version} $RPM_BUILD_ROOT%{_libdir}
%{__ln_s} libtree-sitter-c.so.%{version} $RPM_BUILD_ROOT%{_libdir}/%{ts_c_soname}

%{__ln_s} %{_libdir}/%{ts_c_soname} $RPM_BUILD_ROOT%{_libdir}/nvim/parser/c.so

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc LICENSE README.md
%attr(755,root,root) %{_libdir}/libtree-sitter-c.so.*.*
%attr(755,root,root) %ghost %{_libdir}/%{ts_c_soname}

%files -n neovim-parser-c
%defattr(644,root,root,755)
%{_libdir}/nvim/parser/c.so
