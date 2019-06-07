# fastBPE python wrapper

This is Python wrapper for a C++ implementation to produce BPE codes as explained in:
[Neural Machine Translation of Rare Words with Subword Units](https://arxiv.org/abs/1508.07909).

At the moment all C++ code resides in one file and is quite a mess but
kind of works for what is intended... A better packaging should be coming soon.

It is based on [fastBPE](https://github.com/glample/fastBPE)
modified to expose similar functions working using input strings
instead of files and accessible from a simple python interface.

More specifically exposes the following functions:

```python
from pypbe import pyBPE

# creates a vocab file sorted by frequency, one word per line
pyBPE.create_vocab_file(text: Text, output_path: Text) -> None

# Creates a BPE codes file
pyBPE.create_bpe_file(text: Text, n_codes: int, output_path: Text) -> None

# Given a string and the codes and vocab file paths applies the BPE encoding
bpe = pyBPE(codes_path: Text, vocab_path: Text)
bpe.load()
bpe.apply_bpe(text: Text) -> Text
```


Alternatively it is also possible to obtain a compiled executable from the C++
code, exposing similar functions:

```bash
# getvocab from an input string
./fast getvocabs "this test is a simple sample test"
# equivalent to:
echo "this is a sample simple test test" | ./fast getvocab -

# test learnbpe
./fast learnbpes 10 "this test is a simple sample test"
# equivalent to:
echo "this is a sample simple test test" | ./fast learnbpe 10 -

# apply bpe with OOV words (i.e.: simplest, example)
# with 'codes', 'vocab', 'input' and 'ouput' all being file paths to text files
./fast apply_bpe_from_files "this is the simplest example" codes vocab
# equivalent to:
./fast applybpe out input codes vocab
```



## Requirements

-   [Boost==1.69](http://www.boost.org/)
-   [CMake>=3.13](https://cmake.org/download/)
-   g++ compiler (>=5.4.0)
-   python (>=3.6)
-   [anaconda3](https://www.continuum.io/downloads)

## How to

### As a C++ executable

To compile the code without the python wrapper:

```bash
    # compile without python wrapper
    g++ -std=c++11 -pthread -O3 fast.cpp -o fast
```

### As a Python wrapper

1. Download and **install Boost**:
   (Here we assume we are using Anaconda in an environment called `testDL` with python 3.6)

```bash
    # download and extract
    cd Downloads
    wget https://dl.bintray.com/boostorg/release/1.69.0/source/boost_1_69_0.tar.bz2
    tar --bzip2 -xf boost_1_69_0.tar.bz2
    cd boost_1_69_0/

    # soft links to the names expected by boost
    ln -s ~/anaconda3/include/python3.6m/ ~/anaconda3/include/python3.6/
    ln -s ~/anaconda3/envs/testDL/include/python3.6m/ ~/anaconda3/envs/testDL/include/python3.6/

    python_root=`python -c "import sys; print(sys.prefix)"`
    CPLUS_INCLUDE_PATH="$CPLUS_INCLUDE_PATH:~/anaconda3/envs/testDL/include/python3.6"

    sudo ./bootstrap.sh \
        --with-python-root=$python_root \
        --with-python-version=3.6 \
        --prefix=/usr/include   # installs boost in /usr/include

    sudo ./b2 install
```

2. Clone the repository and compile:

```bash
    export PYTHON_INCLUDE=~/anaconda3/envs/testDL/include/python3.6/
    git clone https://github.com/jmrf/pyBPE
    cd pyBPE
    mkdir build
    cd build
    cmake ..
    make
```

## Run

## Troubleshooting

If a warning appears when running:
`....libstdc++.so.6: versionGLIBCXX_3.4.21' not found...`
you might need to install `libgcc`

```bash
    conda install libgcc
```

## misc

-   additional information on [building python - c++ wrappers with Boost](https://www.preney.ca/paul/archives/107)

-   [Boost](http://www.boost.org/users/history/version_1_64_0.html)

-   [c++ online shell](http://cpp.sh/) or [c++ online compiler](https://rextester.com/l/cpp_online_compiler_gcc)

-   [Interfacing c++ with python](https://flanusse.net/interfacing-c++-with-python.html)

-   [Boost <> Python object converters](https://sixty-north.com/blog/how-to-write-boost-python-type-converters.html)

-   [c++ pair to python](https://stackoverflow.com/questions/16497889/how-to-expose-stdpair-to-python-using-boostpython)
