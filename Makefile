run:
	mkdir -p --verbose vault/ROMS
	python3 vault/runner.py

clean:
	rm -R --verbose ./vault/ROMS/*

.PHONY: run