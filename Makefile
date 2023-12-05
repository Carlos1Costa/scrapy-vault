run:
	mkdir -p --verbose vault/ROMS
	python3 vault/runner.py

clean:
	rm -R --verbose ./vault/ROMS/*

extract:
	python3 vault/extractor.py

.PHONY: run