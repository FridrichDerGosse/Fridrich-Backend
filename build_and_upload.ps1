# ensure the newest versions of twine and build are is installed
python -m pip install twine build --upgrade

# create package
python -m build

# upload
python -m twine upload --skip-existing --config-file config.pypirc dist/*
