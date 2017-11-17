BRANCH := "unspecified"

default: packer-ci

clean:
	@echo "Destroying possible vagrant machine..."
	@cd packer && vagrant destroy -f || true
	rm -rf ./frontend/dist ./frontend/node_modules ./frontend/nohup.out ./frontend/rm.log
	rm -rf ./backend/.eggs ./backend/awsaudits.egg-info ./backend/build ./backend/logs/* ./backend/nohup.out

dist-clean: clean
	git clean -d -x -i

packer-ci:
	@echo "If packer fails quickly, verify valid AWS credentials are available."
	cd packer && \
   	packer build -machine-readable -only ami-with-tests -var-file variables/ci.json -var "git_branch=$(BRANCH)" build.json

vagrant-up:
	@echo "Must be run in admin terminal to have SeCreateSymbolicLinkPrivilege."
	cd packer && \
	vagrant up

vagrant-e2e:
	cd packer && \
	vagrant ssh -c "cd /workspace/frontend/tests; bash ./test-e2e.sh"

.PHONY: default clean dist-clean packer-ci vagrant-up vagrant-e2e
