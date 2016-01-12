.PHONY: clean test

clean:
	rm -rf build dist *.egg-info

test-py:
	PYTHONPATH=. nosetests -w test/ -v

minify:
	cd yaml2pac/data && python minify.py cidr_match.js > cidr_match.min.js

test-js: minify
	./node_modules/mocha/bin/mocha

test: test-py test-js

publish:
	python setup.py sdist upload

publish-all:
	python setup.py sdist bdist_wheel upload
