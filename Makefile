
.PHONY: kuttl-test
kuttl-test: ## Run kattle tests against current cluster
	kubectl kuttl test --start-kind=false ./tests/e2e