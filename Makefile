.PHONY:	help
help:
	@echo "make [target]"
	@echo "available targets:"
	@echo "  check - run linters and unit tests"
	@echo "  test - run all automated tests"

.PHONY:	check
check:
	flake8 ipa_tokenizer test tools --ignore E266
	pylint ipa_tokenizer test tools --disable=duplicate-code
	mypy ipa_tokenizer test tools --strict
	pytest ipa_tokenizer test tools

.PHONY:	test
test:
	pytest ipa_tokenizer test --runslow -x
