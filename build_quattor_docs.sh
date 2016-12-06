#!/bin/bash

VERSION="master"

# Create temporary working directory
mkdir -p /tmp/quattor-documentation/{src,output}
cd /tmp/quattor-documentation/src

# Clone required github repositories
for REPO in CAF configuration-modules-core configuration-modules-grid CCM ;  do
    git clone https://github.com/quattor/$REPO.git
    cd $REPO
    tag=`git tag -l | grep "$VERSION$"`
    git checkout -q $tag
    cd ..
done
cd ..

# Install required software
#sudo yum install python-pip python-devel perl-Pod-Markdown
#pip install --user --upgrade livereload vsc-utils mkdocs

# Get documentation build script
curl -k https://raw.githubusercontent.com/quattor/release/master/src/releasing/quattorpoddoc.py -o quattorpoddoc.py

# Start building the documentation
python quattorpoddoc.py -c -m src/ -o output/ --info

# Get required index which is not generated
curl https://raw.githubusercontent.com/quattor/documentation/master/docs/index.md -o output/docs/index.md

# Build site for testing
cd output
mkdocs build --clean

# Get the tests set up
#sudo yum install rubygem-bundler ruby-devel zlib-devel
curl https://raw.githubusercontent.com/quattor/documentation/master/Gemfile -o Gemfile
bundle install

# Run the tests
bundle exec htmlproofer  --check-html ./site/ --file-ignore ./site/base.html,./site/breadcrumbs.html,./site/footer.html,./site/toc.html,./site/versions.html || { echo 'build test errors detected. stopping.' ; exit 1 ; }

cd ..

# Cleanup

rm output/Gemfile.lock
rm -r output/site

# Setup target (GH)
git clone git@github.com:wdpypere/docs-test-comps.git
cd docs-test-comps
git branch docs-$VERSION
git checkout docs-$VERSION

# Out with the old (make sure deprecated/deleted pages no longer show up)
rm -r docs
rm mkdocs.yml

# In with the new
mv ../output/mkdocs.yml .
mv ../output/docs .

git status
