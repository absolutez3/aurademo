all: clean
	python2.7 setup.py bdist_wheel
	mkdir -p dist
	cp README.MD dist/
	$(eval VERSION:=$(shell python2.7 -c 'from aurademo import _version; print _version'))
	cd dist/ && tar cvzf ../aurademo-$(VERSION).tgz ./*.whl ./README.MD
	cp dist/*.whl .

clean:
	rm -rf ./dist

blast:
	git clean -dfx
