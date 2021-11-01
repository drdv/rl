PYTHON=python3
VENV_NAME=.venv
PYLINT=pylint --rcfile .pylintrc
HTML_DIR=docs/sphinx/build/html

.PHONY: all
all:
	@echo "Be reasonable, check available targets!"

# -----------------------------------------------------------------------------
# docs
# -----------------------------------------------------------------------------
.PHONY: docs
docs: lint test
	cd docs/sphinx && make html

.PHONY: open
open:
	open ${HTML_DIR}/index.html  # macos

# -----------------------------------------------------------------------------
# utest & lint
# -----------------------------------------------------------------------------
.PHONY: test
test:
	py.test \
	--report-log=.utest_reports/utest.log \
	--html=.utest_reports/utest_report.html \
	--cov=rl --cov-config=.coveragerc --cov-report html \
	-v rl/utest

	mkdir -p ${HTML_DIR}
	rm -rf ${HTML_DIR}/.htmlcov
	mv -f .htmlcov ${HTML_DIR}
	rm -rf ${HTML_DIR}/.utest_reports
	mv -f .utest_reports ${HTML_DIR}

.PHONY: lint
lint:
	-@$(PYLINT) rl > .pylint_report.json || exit 0
	-@pylint_report.py .pylint_report.json --html-file .pylint_report.html

	mkdir -p ${HTML_DIR}
	rm -rf ${HTML_DIR}/.pylint_report.html
	mv -f .pylint_report.html ${HTML_DIR}

# -----------------------------------------------------------------------------
# dependencies
# -----------------------------------------------------------------------------
.PHONY: setup-venv
setup-venv:
	${PYTHON} -m venv ${VENV_NAME} && \
	. ${VENV_NAME}/bin/activate && \
	pip install --upgrade pip && \
	pip install -r .requirements.txt

.PHONY: clean
clean:
	rm -rf docs/sphinx/build
	rm -rf .coverage
	rm -rf .pylint_report.json
