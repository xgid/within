set -e

echo '---installing---'
python3.4 setup.py install
echo '---testing---'
nosetests-3.4 --with-coverage --cover-package within tests -v
