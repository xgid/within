set -e

echo '---installing---'
python2.7 setup.py install
echo '---testing---'
nosetests-2.7 --with-coverage --cover-package within tests -v
