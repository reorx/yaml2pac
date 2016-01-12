.PHONY: clean test

clean:
	rm -rf build dist *.egg-info

test:
	PYTHONPATH=. nosetests -w test/ -v

minify:
	cd yaml2pac/data && python minify.py cidr_match.js > cidr_match.min.js

publish:
	python setup.py sdist upload

publish-all:
	python setup.py sdist bdist_wheel upload
