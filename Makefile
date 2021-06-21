RPMBUILD = rpmbuild --define "_topdir %(pwd)/build" \
        --define "_builddir %{_topdir}" \
        --define "_rpmdir %{_topdir}" \
        --define "_srcrpmdir %{_topdir}" \
        --define "_sourcedir %(pwd)"

GIT_VERSION = $(shell git name-rev --name-only --tags --no-undefined HEAD 2>/dev/null || echo git-`git rev-parse --short HEAD`)
SERVER_VERSION=$(shell awk '/Version:/ { print $$2; }' rasa-focuser-server.spec)

all:
	mkdir -p build
	cp focusd focusd.bak
	awk '{sub("SOFTWARE_VERSION = .*$$","SOFTWARE_VERSION = \"$(SERVER_VERSION) ($(GIT_VERSION))\""); print $0}' focusd.bak > focusd
	${RPMBUILD} -ba observatory-focuslynx-server.spec
	${RPMBUILD} -ba observatory-focuslynx-client.spec
	${RPMBUILD} -ba python3-warwick-observatory-focuslynx.spec
	${RPMBUILD} -ba clasp-focuslynx-data.spec
	mv build/noarch/*.rpm .
	rm -rf build
	mv focusd.bak focusd
