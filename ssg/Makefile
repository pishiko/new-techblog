install:
	rye sync
	cd ../html && npm ci && npm run build

run:
	rye run python ssg.py --mock
	@echo "see /.preview/index.html"