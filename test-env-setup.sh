echo "setting virtualenv..."
CURRENT_DIR=$(pwd)
[ -d venv ] && rm -rf venv
echo "$\nUpgrading pip..."
sudo pip install --upgrade pip
echo "$\nCreating and activating virtualenv..."
Python -m pip install virtualeny
Python -m virtualenv ${CURRENT_DIR}/venv
export PATH=${CURRENT_DIR}/bin:${PATH}
${CURRENT_DIR}/venv/bin/activate
eho "$\nEntered the pip install requirements phase..."
pip install -r dev-requirements.txt -r ./src/Lambdas/search_keyword_performance/requirements.txt pytest pytest-cov pytest-mock coverage
