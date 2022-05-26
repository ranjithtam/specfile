%bcond_without check
%define gobuild(o:) %{expand:
  # https://bugzilla.redhat.com/show_bug.cgi?id=995136#c12
  %global _dwz_low_mem_die_limit 0
  %ifnarch ppc64
  go build -buildmode pie -compiler gc -tags="rpm_crashtraceback ${BUILDTAGS:-}" -ldflags "${LDFLAGS:-}%{?currentgoldflags} -X 'main.version=v%{grpcurlver}' -B 0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \\n') -extldflags '%__global_ldflags %{?__golang_extldflags}' -compressdwarf=false" -a -v -x %{?**};
  %else
  go build                -compiler gc -tags="rpm_crashtraceback ${BUILDTAGS:-}" -ldflags "${LDFLAGS:-}%{?currentgoldflags} -B 0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \\n') -extldflags '%__global_ldflags %{?__golang_extldflags}' -compressdwarf=false" -a -v -x %{?**};
  %endif
}

# https://github.com/fullstorydev/grpcurl
%global goipath         github.com/fullstorydev/grpcurl
Version:                %{grpcurlver}

%global goname grpcurl

%global common_description %{expand:
Like cURL, but for gRPC: Command-line tool for interacting with gRPC servers.}

%global golicenses      LICENSE
%global godocs          README.md

Name:           %{goname}
Release:        0
Summary:        Like cURL, but for gRPC: Command-line tool for interacting with gRPC servers

License:        MIT
URL:            https://github.com/fullstorydev/grpcurl
Source0:        https://github.com/fullstorydev/grpcurl/archive/refs/tags/v%{grpcurlver}.tar.gz

# If go_compiler is not set to 1, there is no virtual provide. Use golang instead.
BuildRequires:  %{?go_compiler:compiler(go-compiler)}%{!?go_compiler:golang}

%description
%{common_description}

%prep
%autosetup -p1 -n %{name}-%{version}
%setup -q -T -D -n %{name}-%{version}

%build
export GO111MODULE=off
for cmd in cmd/* ; do
  %gobuild -o _bin/$(basename $cmd) ./$cmd
done

%install
install -m 0755 -vd                     %{buildroot}%{_bindir}
install -m 0755 -vp _bin/*              %{buildroot}%{_bindir}/

%files
%license LICENSE
%doc README.md
%{_bindir}/*
