all: clean build

build:
	pdflatex documentation.tex
	biber documentation
	pdflatex documentation.tex

clean:
	@find . -maxdepth 1 -type f -not -name '*.tex' -not -name '*.bib' -not -name 'Makefile' | xargs rm -f
